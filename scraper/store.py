"""JSON storage with dedupe + first-seen tracking."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "jobs.json"


def _job_id(job: dict) -> str:
    raw = f"{job['firm']}|{job['title']}|{job['location']}".lower()
    return hashlib.sha1(raw.encode()).hexdigest()[:12]


def load() -> dict[str, dict]:
    if DATA_FILE.exists():
        return {j["id"]: j for j in json.loads(DATA_FILE.read_text()).get("jobs", [])}
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
            existing[jid]["last_seen"] = now
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
