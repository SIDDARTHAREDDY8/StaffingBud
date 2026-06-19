"""JSON storage with dedupe + first-seen tracking."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "jobs.json"


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


def merge_and_save(new_jobs: list[dict]) -> dict:
    """Merge freshly scraped jobs into the store. Returns a small run summary."""
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
            # refresh derived/volatile fields so URL-logic changes propagate
            existing[jid]["url"] = job.get("url", existing[jid].get("url"))
            existing[jid]["posted"] = job.get("posted", existing[jid].get("posted"))
        else:
            job["id"] = jid
            job["first_seen"] = now
            job["last_seen"] = now
            existing[jid] = job
            added += 1

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "updated": now,
        "count": len(existing),
        "jobs": sorted(existing.values(), key=lambda j: j.get("first_seen", ""), reverse=True),
    }
    DATA_FILE.write_text(json.dumps(payload, indent=2))
    return {"added": added, "total": len(existing), "scraped": len(new_jobs)}
