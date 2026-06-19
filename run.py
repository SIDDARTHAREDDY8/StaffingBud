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
    needs_http = any(f["mode"] in ("api", "apify_search", "api_html") for f in firms)
    apify_token = os.environ.get("APIFY_TOKEN")

    all_jobs: list[dict] = []
    browser = http = pw = None

    if needs_http:
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
                else:
                    raw = engine.scrape_api(firm, http)
            except Exception as e:  # one firm failing must not kill the run
                print(f"  ! {firm['name']} failed: {e}")
                continue

            kept = filters.apply_filters(raw, firm)
            print(f"  scraped {len(raw)}, kept {len(kept)} after filters")
            all_jobs.extend(kept)
    finally:
        if browser:
            browser.close()
        if pw:
            pw.stop()

    summary = store.merge_and_save(all_jobs)
    print(f"\n✅ done — +{summary['added']} new, {summary['total']} total in data/jobs.json")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help="only scrape these firm names")
    ap.add_argument("--headful", action="store_true", help="show the browser")
    args = ap.parse_args()
    run(only=args.only, headful=args.headful)
