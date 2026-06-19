#!/usr/bin/env python3
"""Inject NEW jobs from data/jobs.json into README.md between markers.

"Show once" rule: a job is listed in the README only on the run it is first
discovered. After it's posted we set `readme_posted: true` on it (persisted back
into data/jobs.json), so it never appears in the README again — the README is a
feed of *new* roles, while site/index.html stays the full browsable archive.
"""
import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "jobs.json"
README = ROOT / "README.md"

START = "<!-- JOBS:START -->"
END = "<!-- JOBS:END -->"
MAX_ROWS = 400


def md_escape(text: str) -> str:
    return (text or "").replace("|", "\\|").strip()


def render(new_jobs: list[dict], total: int, updated: str) -> str:
    BOARD = "https://siddarthareddy8.github.io/StaffingBud/"
    lines = []
    if not new_jobs:
        lines.append(f"### 🟢 No new roles this update · **{total}** roles open total · updated `{updated}`")
        lines.append("")
        lines.append(f"Nothing new since the last run — [browse all {total} open roles on the board »]({BOARD})")
        return "\n".join(lines)

    by_firm = collections.Counter(j["firm"] for j in new_jobs)
    lines.append(f"### 🆕 {len(new_jobs)} new roles this update · {total} tracked total · updated `{updated}`")
    lines.append("")
    lines.append("| Firm | New roles |")
    lines.append("| --- | ---: |")
    for firm, n in by_firm.most_common():
        lines.append(f"| {md_escape(firm)} | {n} |")
    lines.append("")

    new_sorted = sorted(new_jobs, key=lambda j: j.get("first_seen", ""), reverse=True)
    lines.append("| Role | Firm | Location | Found |")
    lines.append("| --- | --- | --- | --- |")
    for j in new_sorted[:MAX_ROWS]:
        role = md_escape(j["title"])
        url = j.get("url", "")
        role_cell = f"[{role}]({url})" if url else role
        loc = md_escape(j.get("location", "")) or "—"
        seen = (j.get("first_seen", "") or "")[:10]
        lines.append(f"| {role_cell} | {md_escape(j['firm'])} | {loc} | {seen} |")
    if len(new_sorted) > MAX_ROWS:
        lines.append("")
        lines.append(f"_…and {len(new_sorted) - MAX_ROWS} more new roles in [`data/jobs.json`](data/jobs.json)._")
    return "\n".join(lines)


def main():
    payload = json.loads(DATA.read_text()) if DATA.exists() else {"jobs": [], "count": 0, "updated": "never"}
    jobs = payload.get("jobs", [])

    new_jobs = [j for j in jobs if not j.get("readme_posted")]
    jobs_md = render(new_jobs, len(jobs), payload.get("updated", "never"))

    # README injection
    text = README.read_text() if README.exists() else ""
    block = f"{START}\n{jobs_md}\n{END}"
    if START in text and END in text:
        text = text.split(START)[0] + block + text.split(END, 1)[1]
    else:
        text = text.rstrip() + "\n\n## Live Jobs\n\n" + block + "\n"
    README.write_text(text)

    # Mark posted + persist so they never show again
    for j in new_jobs:
        j["readme_posted"] = True
    DATA.write_text(json.dumps(payload, indent=2))

    print(f"README updated: {len(new_jobs)} new roles posted (of {len(jobs)} tracked)")


if __name__ == "__main__":
    main()
