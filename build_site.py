#!/usr/bin/env python3
"""Render data/jobs.json into docs/index.html (static, no backend).

Output lives in docs/ so GitHub Pages can serve it directly
(Settings → Pages → Deploy from branch → main → /docs).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "jobs.json"
OUT = ROOT / "docs" / "index.html"

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>StaffingBuddy — Contract Roles</title>
<style>
  :root {{ --bg:#0f1115; --card:#1a1d24; --fg:#e6e9ef; --mut:#8b93a7; --acc:#4f8cff; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font:15px/1.5 -apple-system,Segoe UI,Roboto,sans-serif; background:var(--bg); color:var(--fg); }}
  header {{ padding:24px 20px; border-bottom:1px solid #252a33; }}
  h1 {{ margin:0; font-size:20px; }}
  .meta {{ color:var(--mut); font-size:13px; margin-top:4px; }}
  .controls {{ padding:16px 20px; display:flex; gap:10px; flex-wrap:wrap; }}
  input,select {{ background:var(--card); border:1px solid #2b313c; color:var(--fg); padding:8px 12px; border-radius:8px; font-size:14px; }}
  input {{ flex:1; min-width:200px; }}
  .list {{ padding:0 20px 40px; display:grid; gap:10px; }}
  .job {{ background:var(--card); border:1px solid #232834; border-radius:10px; padding:14px 16px; }}
  .job a {{ color:var(--fg); text-decoration:none; font-weight:600; }}
  .job a:hover {{ color:var(--acc); }}
  .row {{ display:flex; gap:10px; flex-wrap:wrap; color:var(--mut); font-size:13px; margin-top:6px; }}
  .firm {{ color:var(--acc); }}
  .new {{ background:#10331f; color:#5bd98a; font-size:11px; padding:1px 7px; border-radius:20px; margin-left:8px; }}
  .empty {{ color:var(--mut); padding:40px 20px; text-align:center; }}
</style>
</head>
<body>
<header>
  <h1>StaffingBuddy</h1>
  <div class="meta">Contract roles from staffing firms &amp; IT vendors · {count} jobs · updated {updated}</div>
</header>
<div class="controls">
  <input id="q" placeholder="Filter by title or location…">
  <select id="firm"><option value="">All firms</option>{firm_opts}</select>
</div>
<div class="list" id="list"></div>
<script>
const JOBS = {jobs_json};
const list = document.getElementById('list');
const q = document.getElementById('q');
const firmSel = document.getElementById('firm');
function render() {{
  const term = q.value.toLowerCase();
  const firm = firmSel.value;
  const rows = JOBS.filter(j =>
    (!firm || j.firm === firm) &&
    (!term || (j.title + ' ' + j.location).toLowerCase().includes(term))
  );
  if (!rows.length) {{ list.innerHTML = '<div class="empty">No matching jobs.</div>'; return; }}
  list.innerHTML = rows.map(j => `
    <div class="job">
      <a href="${{j.url}}" target="_blank" rel="noopener">${{j.title}}</a>
      <div class="row">
        <span class="firm">${{j.firm}}</span>
        <span>${{j.location || '—'}}</span>
        <span>first seen ${{(j.first_seen||'').slice(0,10)}}</span>
      </div>
    </div>`).join('');
}}
q.addEventListener('input', render);
firmSel.addEventListener('change', render);
render();
</script>
</body>
</html>
"""


def main():
    data = json.loads(DATA.read_text()) if DATA.exists() else {"jobs": [], "count": 0, "updated": "never"}
    jobs = data.get("jobs", [])
    firms = sorted({j["firm"] for j in jobs})
    firm_opts = "".join(f'<option value="{f}">{f}</option>' for f in firms)
    html = TEMPLATE.format(
        count=data.get("count", len(jobs)),
        updated=data.get("updated", "never"),
        firm_opts=firm_opts,
        jobs_json=json.dumps(jobs),
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html)
    (OUT.parent / ".nojekyll").write_text("")  # serve raw HTML, skip Jekyll
    print(f"built {OUT} with {len(jobs)} jobs")


if __name__ == "__main__":
    main()
