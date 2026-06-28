"""JSON storage with dedupe + first-seen tracking."""
from __future__ import annotations

import hashlib
import json
from datetime import date, datetime, timezone
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "jobs.json"

# A "fresh contract jobs" board shouldn't hoard months-old reqs. Any stored job
# whose REAL posted date is older than this is pruned every save — so high-volume
# vendors (e.g. Cynet/Ceipal) can't pile up stale listings forever.
STALE_AFTER_DAYS = 60
# Firms whose `posted` is an unreliable original-release date (SmartRecruiters
# releasedDate, KellyMitchell epoch, Harnham none) — never prune them by it.
_UNRELIABLE_DATE_FIRMS = {"Collabera", "Mastech Digital", "Synechron",
                          "KellyMitchell", "Harnham"}


def _is_stale(job: dict) -> bool:
    posted = (job.get("posted") or "")[:10]
    if not posted or job.get("firm") in _UNRELIABLE_DATE_FIRMS:
        return False
    try:
        return (date.today() - date.fromisoformat(posted)).days > STALE_AFTER_DAYS
    except ValueError:
        return False


def _job_id(job: dict) -> str:
    """A job's identity is its URL — every firm's job URL carries a unique job id.

    This is what lets us tell a genuinely fresh posting from an old one: a new URL
    (new id) = a new job, an URL we've seen before = the same (already-tracked) job.
    Title is NOT identity — two different roles can share a title+location.
    We normalize (drop #fragment, trailing slash, case) so trivial variants don't
    fork identity. Falls back to firm|title|location only if a URL is missing.
    """
    url = (job.get("url") or "").split("#")[0].rstrip("/").strip().lower()
    raw = url or f"{job['firm']}|{job['title']}|{job['location']}".lower()
    return hashlib.sha1(raw.encode()).hexdigest()[:12]


def load() -> dict[str, dict]:
    # Key by the RECOMPUTED id (from URL), not the stored one — this self-migrates
    # any jobs saved under the old title-based scheme while preserving first_seen.
    if DATA_FILE.exists():
        return {_job_id(j): j for j in json.loads(DATA_FILE.read_text()).get("jobs", [])}
    return {}


def merge_and_save(new_jobs: list[dict], refresh_firms: set | None = None) -> dict:
    """Merge freshly scraped jobs into the store. Returns a small run summary.

    refresh_firms: firms that return their COMPLETE current job set each run — any
    stored job of theirs not seen this run is dropped (so expired/dead jobs leave
    the board immediately instead of lingering forever).
    """
    existing = load()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    added = 0

    seen_ids = set()
    for job in new_jobs:
        jid = _job_id(job)
        seen_ids.add(jid)
        if jid in existing:
            existing[jid]["id"] = jid
            existing[jid]["last_seen"] = now
            # refresh derived fields so URL-logic changes propagate; never overwrite
            # a known posted date with an empty one (listing scrapes lack the date)
            existing[jid]["url"] = job.get("url") or existing[jid].get("url")
            if job.get("posted"):
                existing[jid]["posted"] = job["posted"]
        else:
            job["id"] = jid
            job["first_seen"] = now
            job["last_seen"] = now
            existing[jid] = job
            added += 1

    # full-refresh firms: drop their stored jobs not seen in this run (expired)
    removed = 0
    if refresh_firms:
        for jid in [k for k, v in existing.items()
                    if v.get("firm") in refresh_firms and k not in seen_ids]:
            del existing[jid]
            removed += 1

    # perpetual freshness: prune anything past STALE_AFTER_DAYS by real posted date
    pruned = 0
    for jid in [k for k, v in existing.items() if _is_stale(v)]:
        del existing[jid]
        pruned += 1

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "updated": now,
        "count": len(existing),
        "jobs": sorted(existing.values(), key=lambda j: j.get("first_seen", ""), reverse=True),
    }
    DATA_FILE.write_text(json.dumps(payload, indent=2))
    return {"added": added, "removed": removed, "pruned": pruned,
            "total": len(existing), "scraped": len(new_jobs)}
