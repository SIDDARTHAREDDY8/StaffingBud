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
<title>StaffingBuddy — Contract IT Roles</title>
<style>
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font:14px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
         background:#fff; color:#000; }}
  header {{ padding:22px 20px 14px; border-bottom:2px solid #000; }}
  h1 {{ margin:0; font-size:22px; letter-spacing:-.5px; }}
  .meta {{ color:#555; font-size:12px; margin-top:4px; }}
  .controls {{ padding:14px 20px; display:flex; gap:10px; flex-wrap:wrap;
              border-bottom:1px solid #ccc; position:sticky; top:0; background:#fff; }}
  input, select {{ background:#fff; border:1px solid #000; color:#000; padding:8px 10px;
                  font-size:13px; border-radius:0; }}
  input {{ flex:1; min-width:200px; }}
  .wrap {{ padding:0 20px 60px; }}
  table {{ width:100%; border-collapse:collapse; }}
  th {{ text-align:left; font-size:11px; text-transform:uppercase; letter-spacing:.5px;
       color:#000; border-bottom:2px solid #000; padding:10px 12px 8px; position:sticky; top:55px; background:#fff; }}
  td {{ border-bottom:1px solid #ddd; padding:11px 12px; vertical-align:top; }}
  tr:hover td {{ background:#f4f4f4; }}
  .firm {{ font-weight:700; white-space:nowrap; }}
  .pos {{ font-weight:500; }}
  .date {{ color:#555; white-space:nowrap; font-variant-numeric:tabular-nums; }}
  .new {{ display:inline-block; background:#000; color:#fff; font-size:10px; font-weight:700;
         letter-spacing:.5px; padding:1px 5px; margin-right:6px; vertical-align:1px; }}
  .freshlbl {{ display:flex; align-items:center; gap:6px; font-size:13px; border:1px solid #000;
              padding:7px 10px; white-space:nowrap; cursor:pointer; user-select:none; }}
  .freshlbl input {{ width:auto; min-width:0; margin:0; accent-color:#000; }}
  .apply {{ display:inline-block; border:1px solid #000; padding:4px 12px; text-decoration:none;
           color:#000; font-weight:600; font-size:12px; white-space:nowrap; }}
  .apply:hover {{ background:#000; color:#fff; }}
  .empty {{ padding:50px 20px; text-align:center; color:#555; }}
  @media (max-width:640px) {{ .hide-sm {{ display:none; }} th,td {{ padding:9px 8px; }} }}
</style>
</head>
<body>
<header>
  <h1>StaffingBuddy</h1>
  <div class="meta">Contract IT roles from staffing firms &amp; vendors · <span id="shown">{count}</span> of {count} roles · updated {updated}</div>
</header>
<div class="controls">
  <input id="q" placeholder="Search position…">
  <select id="firm"><option value="">All firms</option>{firm_opts}</select>
  <label class="freshlbl"><input type="checkbox" id="fresh"> Fresh only (7 days)</label>
</div>
<div class="wrap">
  <table>
    <thead><tr>
      <th>Firm</th><th>Position</th><th class="hide-sm">Posted</th><th>Apply</th>
    </tr></thead>
    <tbody id="rows"></tbody>
  </table>
  <div class="empty" id="empty" style="display:none">No matching roles.</div>
</div>
<script>
const JOBS = {jobs_json};
const rowsEl = document.getElementById('rows');
const emptyEl = document.getElementById('empty');
const shownEl = document.getElementById('shown');
const q = document.getElementById('q');
const firmSel = document.getElementById('firm');
const freshChk = document.getElementById('fresh');
function esc(s) {{ return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }}
// Freshness age. Prefer the firm's REAL posted date when it parses and is recent
// (≤200d — ignores evergreen/lying dates like SmartRecruiters' 2017); else fall
// back to first_seen (when we found it). Recomputed on view.
function ageDays(j) {{
  const p = Date.parse(j.posted || '');
  if (!isNaN(p)) {{
    const pd = (Date.now() - p) / 86400000;
    if (pd >= -3 && pd <= 200) return pd;
  }}
  const f = Date.parse(j.first_seen || '');
  return isNaN(f) ? 9999 : (Date.now() - f) / 86400000;
}}
function ageLabel(d) {{
  if (d >= 9999) return '—';
  if (d < 1) return 'Today';
  if (d < 2) return 'Yesterday';
  if (d < 7) return Math.floor(d) + 'd ago';
  if (d < 14) return '1w ago';
  if (d < 30) return Math.floor(d/7) + 'w ago';
  return Math.floor(d/30) + 'mo ago';
}}
function render() {{
  const term = q.value.toLowerCase();
  const firm = firmSel.value;
  const freshOnly = freshChk.checked;
  const rows = JOBS.filter(j =>
    (!firm || j.firm === firm) &&
    (!term || (j.title + ' ' + (j.location||'')).toLowerCase().includes(term)) &&
    (!freshOnly || ageDays(j) <= 7)
  );
  shownEl.textContent = rows.length;
  emptyEl.style.display = rows.length ? 'none' : 'block';
  rowsEl.innerHTML = rows.map(j => {{
    const loc = j.location ? ` <span style="color:#777">· ${{esc(j.location)}}</span>` : '';
    const d = ageDays(j);
    const pill = d < 1 ? '<span class="new">NEW</span>' : '';
    return `<tr>
      <td class="firm">${{esc(j.firm)}}</td>
      <td class="pos">${{esc(j.title)}}${{loc}}</td>
      <td class="date hide-sm">${{pill}}${{ageLabel(d)}}</td>
      <td><a class="apply" href="${{j.url}}" target="_blank" rel="noopener">Apply →</a></td>
    </tr>`;
  }}).join('');
}}
q.addEventListener('input', render);
firmSel.addEventListener('change', render);
freshChk.addEventListener('change', render);
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
