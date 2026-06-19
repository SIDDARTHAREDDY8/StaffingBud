#!/usr/bin/env python3
"""Inject the current jobs from data/jobs.json into README.md between markers.

Keeps everything outside the <!-- JOBS:START --> / <!-- JOBS:END --> markers intact,
so the project description and docs stay put while the job list refreshes each run.
"""
import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "jobs.json"
README = ROOT / "README.md"

START = "<!-- JOBS:START -->"
END = "<!-- JOBS:END -->"
MAX_ROWS = 250  # keep the README readable


def md_escape(text: str) -> str:
    return (text or "").replace("|", "\\|").strip()


def build_jobs_md() -> str:
    data = json.loads(DATA.read_text()) if DATA.exists() else {"jobs": [], "count": 0, "updated": "never"}
    jobs = data.get("jobs", [])
    updated = data.get("updated", "never")
    by_firm = collections.Counter(j["firm"] for j in jobs)

    lines = []
    lines.append(f"### 📊 {len(jobs)} open contract roles · {len(by_firm)} firms · updated `{updated}`")
    lines.append("")

    # Per-firm summary
    lines.append("| Firm | Open roles |")
    lines.append("| --- | ---: |")
    for firm, n in by_firm.most_common():
        lines.append(f"| {md_escape(firm)} | {n} |")
    lines.append("")

    # Newest jobs first
    jobs_sorted = sorted(jobs, key=lambda j: j.get("first_seen", ""), reverse=True)
    shown = jobs_sorted[:MAX_ROWS]

    lines.append("| Role | Firm | Location | First seen |")
    lines.append("| --- | --- | --- | --- |")
    for j in shown:
        role = md_escape(j["title"])
        url = j.get("url", "")
        role_cell = f"[{role}]({url})" if url else role
        loc = md_escape(j.get("location", "")) or "—"
        seen = (j.get("first_seen", "") or "")[:10]
        lines.append(f"| {role_cell} | {md_escape(j['firm'])} | {loc} | {seen} |")

    if len(jobs_sorted) > MAX_ROWS:
        lines.append("")
        lines.append(f"_…and {len(jobs_sorted) - MAX_ROWS} more. See [`data/jobs.json`](data/jobs.json) for the full list._")

    return "\n".join(lines)


def main():
    jobs_md = build_jobs_md()
    text = README.read_text() if README.exists() else ""

    block = f"{START}\n{jobs_md}\n{END}"
    if START in text and END in text:
        pre = text.split(START)[0]
        post = text.split(END, 1)[1]
        text = pre + block + post
    else:
        # markers missing — append a Live Jobs section
        text = text.rstrip() + "\n\n## Live Jobs\n\n" + block + "\n"

    README.write_text(text)
    print(f"README updated with jobs ({jobs_md.splitlines()[0]})")


if __name__ == "__main__":
    main()
