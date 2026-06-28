#!/usr/bin/env python3
"""
StaffingBuddy — scrape staffing-firm / IT-vendor career pages for contract roles.

Usage:
    python run.py                # scrape all firms in config/firms.yaml
    python run.py --only "TEKsystems" "Kforce"
    python run.py --headful      # watch the browser (debugging selectors)
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import yaml

from scraper import engine, filters, store

CONFIG = Path(__file__).resolve().parent / "config" / "firms.yaml"


def load_firms(only: list[str] | None) -> list[dict]:
    firms = yaml.safe_load(CONFIG.read_text())["firms"]
    if only:
        wanted = {n.lower() for n in only}
        firms = [f for f in firms if f["name"].lower() in wanted]
    else:
        # skip firms explicitly disabled (e.g. not yet calibrated)
        firms = [f for f in firms if f.get("enabled", True)]
    return firms


def run(only=None, headful=False):
    firms = load_firms(only)
    if not firms:
        print("No matching firms in config.")
        return

    needs_browser = any(f["mode"] == "dom" for f in firms)
    # http client is needed for API-type modes AND for detail-date enrichment
    needs_http = any(
        f["mode"] in ("api", "apify_search", "api_html", "sitemap", "html", "rss") or f.get("detail_date")
        for f in firms
    )
    apify_token = os.environ.get("APIFY_TOKEN")

    all_jobs: list[dict] = []
    refresh_firms: set[str] = set()
    browser = http = pw = None

    if needs_http:
        # curl_cffi impersonates a real Chrome TLS fingerprint, which slips past
        # Cloudflare / Radware bot-walls (Beacon Hill, Njoyn). Falls back to plain
        # requests if unavailable. API-compatible: .get/.post/.json/.text/.content.
        try:
            from curl_cffi import requests as _cf
            http = _cf.Session(impersonate="chrome120")
        except ImportError:
            import requests
            http = requests.Session()
            http.headers.update({"User-Agent": "Mozilla/5.0 StaffingBuddy"})

    if needs_browser:
        from playwright.sync_api import sync_playwright
        pw = sync_playwright().start()
        browser = pw.chromium.launch(headless=not headful)

    try:
        for firm in firms:
            print(f"→ {firm['name']} ({firm['mode']}) …", flush=True)
            try:
                if firm["mode"] == "dom":
                    page = browser.new_page()
                    raw = engine.scrape_dom(firm, page)
                    page.close()
                elif firm["mode"] == "apify_search":
                    if not apify_token:
                        print(f"  ! {firm['name']} skipped: APIFY_TOKEN not set")
                        continue
                    raw = engine.scrape_apify_search(firm, http, apify_token)
                elif firm["mode"] == "api_html":
                    raw = engine.scrape_api_html(firm, http)
                elif firm["mode"] == "sitemap":
                    raw = engine.scrape_sitemap(firm, http)
                elif firm["mode"] == "rss":
                    raw = engine.scrape_rss(firm, http)
                elif firm["mode"] == "html":
                    raw = engine.scrape_html(firm, http)
                elif firm["mode"] == "ceipal":
                    raw = engine.scrape_ceipal(firm)
                elif firm["mode"] == "jobdiva":
                    raw = engine.scrape_jobdiva(firm)
                else:
                    raw = engine.scrape_api(firm, http)
            except Exception as e:  # one firm failing must not kill the run
                print(f"  ! {firm['name']} failed: {e}")
                continue

            kept = filters.apply_filters(raw, firm)
            for j in kept:                       # 'Posted 7 Days Ago' -> ISO date
                j["posted"] = engine.normalize_posted(j.get("posted", ""))
            # firms that expose a real posted date directly (e.g. RSS pubDate) but
            # aren't detail-enriched: apply the same recency cap so stale reqs drop
            if firm.get("max_age_days") and not firm.get("detail_date"):
                kept = [j for j in kept if engine.within_age(j.get("posted", ""), firm["max_age_days"])]
            # firms that only expose the posting date on the detail page: fetch it
            # for NEW jobs so freshness reflects the true posted date, not first_seen
            if firm.get("detail_date") and http:
                known = store.load()
                got = engine.enrich_posted_dates(kept, http, known, store._job_id)
                if got:
                    print(f"  enriched {got} posted-dates from detail pages", flush=True)
                # enrichment writes the raw detail-page date (e.g. "May 29, 2026") —
                # normalize to ISO so the recency filter + board freshness work
                for j in kept:
                    j["posted"] = engine.normalize_posted(j.get("posted", ""))
                # locations/dates are now populated — re-apply US + recency filters.
                # date-enriched firms have RELIABLE post dates, so drop genuinely-old
                # jobs (default 60d) — firms keep stale listings up for months/years.
                before = len(kept)
                kept = [j for j in kept if not filters.is_non_us(j.get("location", ""))]
                max_age = firm.get("max_age_days", 60)
                kept = [j for j in kept if engine.within_age(j.get("posted", ""), max_age)]
                if len(kept) != before:
                    print(f"  dropped {before - len(kept)} non-US/stale after enrichment", flush=True)
            # verify each job is still live (drop expired sitemap entries e.g. Robert Half)
            if firm.get("verify_live") and http:
                before = len(kept)
                kept = engine.verify_live_jobs(kept, http, firm["verify_live"])
                refresh_firms.add(firm["name"])     # complete set -> prune dead from store
                if len(kept) != before:
                    print(f"  dropped {before - len(kept)} dead/expired jobs", flush=True)
            print(f"  scraped {len(raw)}, kept {len(kept)} after filters")
            all_jobs.extend(kept)
    finally:
        if browser:
            browser.close()
        if pw:
            pw.stop()

    summary = store.merge_and_save(all_jobs, refresh_firms=refresh_firms)
    print(f"\n✅ done — +{summary['added']} new, -{summary.get('removed', 0)} expired, "
          f"-{summary.get('pruned', 0)} stale, {summary['total']} total in data/jobs.json")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help="only scrape these firm names")
    ap.add_argument("--headful", action="store_true", help="show the browser")
    args = ap.parse_args()
    run(only=args.only, headful=args.headful)
