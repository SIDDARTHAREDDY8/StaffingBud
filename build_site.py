#!/usr/bin/env python3
"""Render data/jobs.json into docs/index.html — "plugd", a modern static job board.

Output lives in docs/ so GitHub Pages serves it directly
(Settings → Pages → Deploy from branch → main → /docs). No backend, no build step:
jobs are embedded as JSON and filtered/rendered client-side. National (US) scope —
the location filter is built dynamically from the data (states + Remote).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "jobs.json"
CONFIG = ROOT / "config" / "firms.yaml"
OUT = ROOT / "docs" / "index.html"

BRAND = "plugd"
REPO = "https://github.com/SIDDARTHAREDDY8/StaffingBud"

TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>plugd — fresh contract tech jobs, scanned hourly</title>
<meta name="description" content="plugd is a free, auto-updating board of US contract tech roles — software, data, AI/ML, cloud & full-stack — pulled straight from 60+ staffing firms & IT vendors and refreshed every few hours.">
<meta property="og:title" content="plugd — your plug for fresh contract tech roles">
<meta property="og:description" content="Software, data, AI/ML & cloud contract roles from 60+ staffing firms — one feed, newest first, no login.">
<style>
  :root{
    --bg:#0a0b0f; --bg-2:#0e1016; --card:#13151d; --card-2:#171a23;
    --ink:#f3f5f8; --muted:#9aa3b2; --faint:#6b7280; --line:#22252f; --line-2:#2c3140;
    --lime:#c8f560; --lime-2:#a6e22e; --lime-ink:#0a0b0f;
    --violet:#a78bfa; --blue:#60a5fa; --pink:#f472b6;
  }
  *{box-sizing:border-box}
  html,body{margin:0}
  body{font:15px/1.55 ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;
       background:var(--bg); color:var(--ink); -webkit-font-smoothing:antialiased; overflow-x:hidden}
  a{color:inherit}
  ::selection{background:var(--lime); color:var(--lime-ink)}

  /* ---------- hero ---------- */
  .hero{position:relative; overflow:hidden; padding:46px 20px 40px;
        background:radial-gradient(1100px 420px at 12% -10%, rgba(200,245,96,.16), transparent 60%),
                   radial-gradient(900px 500px at 92% 0%, rgba(167,139,250,.16), transparent 55%),
                   linear-gradient(180deg,#0c0e14 0%, var(--bg) 100%)}
  .hero::after{content:""; position:absolute; inset:0; pointer-events:none;
        background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);
        background-size:46px 46px; mask-image:radial-gradient(700px 360px at 30% 0%, #000 0%, transparent 75%);
        -webkit-mask-image:radial-gradient(700px 360px at 30% 0%, #000 0%, transparent 75%); opacity:.5}
  .hero-in{position:relative; z-index:1; max-width:1040px; margin:0 auto}
  .brandrow{display:flex; align-items:center; gap:10px; margin-bottom:22px}
  .mark{font-weight:900; font-size:23px; letter-spacing:-1.2px}
  .mark .b{color:var(--lime)}
  .dot{width:8px; height:8px; border-radius:50%; background:var(--lime); box-shadow:0 0 0 4px rgba(200,245,96,.18);
       animation:pulse 2.4s infinite}
  @keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
  .live{font-size:12px; color:var(--muted); font-weight:600; letter-spacing:.2px}
  .ghub{margin-left:auto; font-size:13px; color:var(--muted); text-decoration:none; border:1px solid var(--line-2);
        padding:7px 13px; border-radius:999px; transition:.15s}
  .ghub:hover{color:var(--ink); border-color:var(--faint)}
  h1{margin:0 0 12px; font-size:46px; line-height:1.02; letter-spacing:-2px; font-weight:900; max-width:760px}
  h1 .g{background:linear-gradient(92deg,var(--lime),#e9ffb0); -webkit-background-clip:text; background-clip:text; color:transparent}
  .tag{margin:0; max-width:600px; font-size:16px; color:var(--muted)}
  .tag b{color:var(--ink); font-weight:600}
  .stats{display:flex; gap:12px; flex-wrap:wrap; margin-top:26px}
  .stat{background:rgba(255,255,255,.025); border:1px solid var(--line); border-radius:14px; padding:13px 18px; min-width:110px}
  .stat .n{font-size:25px; font-weight:850; line-height:1; letter-spacing:-.5px}
  .stat .n.lime{color:var(--lime)}
  .stat .l{font-size:11px; text-transform:uppercase; letter-spacing:.7px; color:var(--faint); margin-top:6px; font-weight:600}

  /* ---------- controls ---------- */
  .bar{position:sticky; top:0; z-index:30; background:rgba(10,11,15,.72); backdrop-filter:blur(14px) saturate(140%);
       border-bottom:1px solid var(--line); padding:12px 20px}
  .bar-in{max-width:1040px; margin:0 auto; display:flex; gap:9px; flex-wrap:wrap; align-items:center}
  .search{position:relative; flex:1; min-width:230px}
  .search svg{position:absolute; left:13px; top:50%; transform:translateY(-50%); color:var(--faint)}
  input[type=search]{width:100%; padding:11px 12px 11px 40px; font-size:14px; border:1px solid var(--line-2);
       border-radius:11px; background:var(--card); color:var(--ink)}
  input[type=search]::placeholder{color:var(--faint)}
  select{padding:11px 30px 11px 13px; font-size:13.5px; border:1px solid var(--line-2); border-radius:11px;
       background:var(--card) url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12' fill='none' stroke='%239aa3b2' stroke-width='2'><path d='M2 4l4 4 4-4'/></svg>") no-repeat right 11px center;
       color:var(--ink); cursor:pointer; -webkit-appearance:none; appearance:none}
  input:focus,select:focus{outline:none; border-color:var(--lime); box-shadow:0 0 0 3px rgba(200,245,96,.15)}
  .toggle{display:inline-flex; align-items:center; gap:7px; font-size:13px; color:var(--muted);
          border:1px solid var(--line-2); border-radius:11px; padding:10px 13px; cursor:pointer; user-select:none;
          white-space:nowrap; background:var(--card); transition:.15s}
  .toggle:hover{border-color:var(--faint)}
  .toggle input{accent-color:var(--lime); width:15px; height:15px}
  .toggle.on{border-color:var(--lime); color:var(--lime)}

  /* ---------- list ---------- */
  .wrap{max-width:1040px; margin:0 auto; padding:20px 20px 90px}
  .count{font-size:13px; color:var(--muted); margin:2px 2px 16px}
  .count b{color:var(--ink)}
  .card{position:relative; display:flex; gap:15px; align-items:center; background:var(--card);
        border:1px solid var(--line); border-radius:16px; padding:15px 17px; margin-bottom:11px;
        transition:transform .14s, border-color .14s, background .14s}
  .card:hover{transform:translateY(-2px); border-color:var(--line-2); background:var(--card-2)}
  .card.isnew{border-color:rgba(200,245,96,.28)}
  .card.isnew::before{content:""; position:absolute; left:0; top:14px; bottom:14px; width:3px; border-radius:3px;
        background:var(--lime); box-shadow:0 0 12px rgba(200,245,96,.5)}
  .logo{flex:none; width:48px; height:48px; border-radius:13px; display:grid; place-items:center;
        font-weight:850; font-size:17px; color:#0a0b0f; letter-spacing:-.5px}
  .body{flex:1; min-width:0}
  .ttl{font-size:16.5px; font-weight:700; letter-spacing:-.3px; margin:0 0 3px; color:var(--ink)}
  .co{font-size:13px; color:var(--muted); font-weight:600}
  .metarow{display:flex; gap:7px; flex-wrap:wrap; margin-top:11px}
  .chip{display:inline-flex; align-items:center; gap:5px; font-size:11.5px; color:#c7cdd8;
        background:rgba(255,255,255,.04); border:1px solid var(--line-2); border-radius:999px; padding:4px 10px; white-space:nowrap}
  .chip.remote{color:var(--blue); border-color:rgba(96,165,250,.3)}
  .chip.staff{color:var(--violet); border-color:rgba(167,139,250,.28)}
  .chip.emp{color:#34d399; border-color:rgba(52,211,153,.28)}
  .chip.new{background:var(--lime); color:var(--lime-ink); font-weight:800; letter-spacing:.5px; border-color:var(--lime)}
  .right{flex:none; display:flex; flex-direction:column; align-items:flex-end; gap:11px}
  .posted{font-size:12px; color:var(--faint); white-space:nowrap; font-variant-numeric:tabular-nums; font-weight:600}
  .apply{display:inline-flex; align-items:center; gap:5px; background:var(--lime); color:var(--lime-ink); text-decoration:none;
         font-weight:800; font-size:13px; padding:9px 16px; border-radius:10px; white-space:nowrap; transition:.15s}
  .apply:hover{filter:brightness(1.08); transform:translateX(1px)}
  .empty{text-align:center; color:var(--muted); padding:70px 20px}
  .empty .big{font-size:18px; color:var(--ink); font-weight:700; margin-bottom:6px}
  .empty button{margin-top:14px; background:var(--card); color:var(--ink); border:1px solid var(--line-2);
        padding:9px 16px; border-radius:10px; cursor:pointer; font-weight:600}

  footer{border-top:1px solid var(--line); background:var(--bg-2)}
  .foot{max-width:1040px; margin:0 auto; padding:30px 20px 48px; color:var(--muted); font-size:13.5px}
  .foot .fbrand{font-weight:900; font-size:18px; letter-spacing:-.8px; color:var(--ink); margin-bottom:10px}
  .foot .fbrand .b{color:var(--lime)}
  .foot b{color:var(--ink)} .foot a{color:var(--lime); text-decoration:none; font-weight:600}

  @media (max-width:620px){
    .hero{padding:34px 18px 30px} h1{font-size:33px; letter-spacing:-1.3px}
    .card{padding:14px; gap:12px} .logo{width:42px; height:42px; font-size:15px}
    .right{flex-direction:row; align-items:center; gap:12px}
    .posted{display:none}
    .stat{flex:1; min-width:calc(50% - 6px)}
  }
</style>
</head>
<body>
<header class="hero">
  <div class="hero-in">
    <div class="brandrow">
      <span class="dot"></span>
      <span class="mark"><span class="b">{</span>plugd<span class="b">}</span></span>
      <span class="live">live &middot; auto-updates every few hours</span>
      <a class="ghub" href="__REPO__" target="_blank" rel="noopener">&#9733; GitHub</a>
    </div>
    <h1>your <span class="g">plug</span> for fresh contract tech roles.</h1>
    <p class="tag">Software, data, AI/ML, cloud &amp; full-stack contract gigs — pulled straight from <b>__COMPANIES__ staffing firms &amp; IT vendors</b> across the US, into one feed. Newest first. No login, no fluff.</p>
    <div class="stats">
      <div class="stat"><div class="n">__COUNT__</div><div class="l">Open roles</div></div>
      <div class="stat"><div class="n lime" id="newcount">·</div><div class="l">New today</div></div>
      <div class="stat"><div class="n">__COMPANIES__</div><div class="l">Sources</div></div>
      <div class="stat"><div class="n" style="font-size:15px;font-weight:700" id="ago">·</div><div class="l">Last refresh</div></div>
    </div>
  </div>
</header>

<div class="bar">
  <div class="bar-in">
    <div class="search">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
      <input type="search" id="q" placeholder="Search role, company, skill…">
    </div>
    <select id="loc"><option value="">📍 All locations</option></select>
    <select id="kind">
      <option value="">All sources</option>
      <option value="staff">🤝 Staffing / vendor</option>
      <option value="emp">🏢 Direct employer</option>
    </select>
    <select id="firm"><option value="">All companies</option>__FIRM_OPTS__</select>
    <label class="toggle" id="freshL"><input type="checkbox" id="fresh"> ✦ Fresh (7d)</label>
  </div>
</div>

<div class="wrap">
  <div class="count" id="count"></div>
  <div id="list"></div>
  <div class="empty" id="empty" style="display:none">
    <div class="big">Nothing matches that 😕</div>
    <div>Try a different search or widen the filters.</div>
    <button onclick="resetAll()">Clear filters</button>
  </div>
</div>

<footer>
  <div class="foot">
    <div class="fbrand"><span class="b">{</span>plugd<span class="b">}</span></div>
    <b>The vibe:</b> hunting contract tech work means tabbing through dozens of staffing-firm career pages, most showing stale reqs. plugd watches them for you and surfaces only fresh US software / data / AI&nbsp;/ ML / cloud roles — each one links straight to the real job description, and brand-new posts get the ✦ NEW tag.
    <br><br>
    Built for new grads, OPT/CPT students, career switchers &amp; C2C contractors. Free &amp; open-source · <a href="__REPO__" target="_blank" rel="noopener">github.com/SIDDARTHAREDDY8/StaffingBud</a> · secure the bag 💰
  </div>
</footer>

<script>
const JOBS = __JOBS_JSON__;
const KIND = __FIRMKIND_JSON__;   // firm name -> "emp" | "staff"
const $ = id => document.getElementById(id);
const listEl=$('list'), emptyEl=$('empty'), countEl=$('count');
const q=$('q'), locSel=$('loc'), kindSel=$('kind'), firmSel=$('firm'), fresh=$('fresh');

function esc(s){return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function cleanLoc(l){return (l||'').replace(/[\[\]"']/g,'').replace(/\s*[;|]\s*/g,'; ').replace(/\s+/g,' ').trim();}

const STATES={alabama:'AL',alaska:'AK',arizona:'AZ',arkansas:'AR',california:'CA',colorado:'CO',connecticut:'CT',delaware:'DE',florida:'FL',georgia:'GA',hawaii:'HI',idaho:'ID',illinois:'IL',indiana:'IN',iowa:'IA',kansas:'KS',kentucky:'KY',louisiana:'LA',maine:'ME',maryland:'MD',massachusetts:'MA',michigan:'MI',minnesota:'MN',mississippi:'MS',missouri:'MO',montana:'MT',nebraska:'NE',nevada:'NV','new hampshire':'NH','new jersey':'NJ','new mexico':'NM','new york':'NY','north carolina':'NC','north dakota':'ND',ohio:'OH',oklahoma:'OK',oregon:'OR',pennsylvania:'PA','rhode island':'RI','south carolina':'SC','south dakota':'SD',tennessee:'TN',texas:'TX',utah:'UT',vermont:'VT',virginia:'VA',washington:'WA','west virginia':'WV',wisconsin:'WI',wyoming:'WY','district of columbia':'DC'};
const ABBR=new Set(Object.values(STATES));
// Pull a US state code (or "Remote") out of a freeform location string.
function stateOf(loc){
  const l=cleanLoc(loc); const low=l.toLowerCase();
  if(!l) return '';
  if(/\b(remote|anywhere|virtual|telework|wfh)\b/.test(low)) return 'Remote';
  let m=l.match(/\b([A-Z]{2})\b/g); if(m){for(const c of m.reverse()){if(ABBR.has(c))return c;}}
  for(const name in STATES){ if(low.includes(name)) return STATES[name]; }
  return '';
}

function ageDays(j){
  const p=Date.parse(j.posted||'');
  if(!isNaN(p)){const d=(Date.now()-p)/864e5; if(d>=-3&&d<=200) return d;}
  const f=Date.parse(j.first_seen||''); return isNaN(f)?9999:(Date.now()-f)/864e5;
}
function ageLabel(d){
  if(d>=9999) return '';
  if(d<1) return 'today'; if(d<2) return '1d ago';
  if(d<7) return Math.floor(d)+'d ago'; if(d<14) return '1w ago';
  if(d<31) return Math.floor(d/7)+'w ago'; return Math.floor(d/30)+'mo ago';
}
const PALETTE=['#c8f560','#a78bfa','#60a5fa','#f472b6','#34d399','#fbbf24','#f87171','#22d3ee','#fb923c','#818cf8','#2dd4bf','#e879f9'];
function color(name){let h=0; for(let i=0;i<name.length;i++) h=(h*31+name.charCodeAt(i))>>>0; return PALETTE[h%PALETTE.length];}
function monogram(name){return (name||'?').replace(/[^A-Za-z0-9]/g,'').slice(0,2).toUpperCase()||'?';}

// build the location dropdown from data (states + Remote), most-common first
(function buildLoc(){
  const c={}; JOBS.forEach(j=>{const s=stateOf(j.location); if(s) c[s]=(c[s]||0)+1;});
  const order=Object.keys(c).sort((a,b)=> (a==='Remote'?-1:b==='Remote'?1: c[b]-c[a]));
  order.forEach(s=>{const o=document.createElement('option'); o.value=s; o.textContent=(s==='Remote'?'🌐 Remote':s)+' ('+c[s]+')'; locSel.appendChild(o);});
})();

function render(){
  const term=q.value.toLowerCase().trim();
  const loc=locSel.value, kind=kindSel.value, firm=firmSel.value, fo=fresh.checked;
  $('freshL').classList.toggle('on', fo);
  const rows=JOBS.filter(j=>
    (!firm || j.firm===firm) &&
    (!kind || (KIND[j.firm]||'staff')===kind) &&
    (!loc || stateOf(j.location)===loc) &&
    (!term || (j.title+' '+j.firm+' '+(j.location||'')).toLowerCase().includes(term)) &&
    (!fo || ageDays(j)<=7)
  ).sort((a,b)=>ageDays(a)-ageDays(b));

  countEl.innerHTML = `<b>${rows.length.toLocaleString()}</b> role${rows.length===1?'':'s'}` +
                      (rows.length!==JOBS.length?` &middot; filtered from ${JOBS.length.toLocaleString()}`:` &middot; newest first`);
  emptyEl.style.display = rows.length?'none':'block';
  listEl.innerHTML = rows.map(j=>{
    const d=ageDays(j), isNew=d<1;
    const k=(KIND[j.firm]||'staff');
    const kindChip = k==='emp'
      ? '<span class="chip emp">🏢 Direct employer</span>'
      : '<span class="chip staff">🤝 Staffing / vendor</span>';
    const lc=cleanLoc(j.location), isRemote=/\b(remote|anywhere|virtual|telework|wfh)\b/i.test(lc);
    const locChip = lc ? `<span class="chip ${isRemote?'remote':''}">${isRemote?'🌐':'📍'} ${esc(lc)}</span>` : '';
    const newChip = isNew ? '<span class="chip new">✦ NEW</span>' : '';
    const al=ageLabel(d);
    return `<div class="card${isNew?' isnew':''}">
      <div class="logo" style="background:${color(j.firm)}">${esc(monogram(j.firm))}</div>
      <div class="body">
        <h3 class="ttl">${esc(j.title)}</h3>
        <div class="co">${esc(j.firm)}</div>
        <div class="metarow">${newChip}${locChip}${kindChip}</div>
      </div>
      <div class="right">
        ${al?`<span class="posted">${al}</span>`:''}
        <a class="apply" href="${esc(j.url)}" target="_blank" rel="noopener">Apply →</a>
      </div>
    </div>`;
  }).join('');
}
function resetAll(){q.value='';locSel.value='';kindSel.value='';firmSel.value='';fresh.checked=false;render();}

// headline numbers
$('newcount').textContent = JOBS.filter(j=>ageDays(j)<1).length;
(function freshness(){
  const t=Date.parse('__UPDATED_ISO__'); if(isNaN(t)){$('ago').textContent='—';return;}
  const m=Math.round((Date.now()-t)/6e4);
  $('ago').textContent = m<60?`${m}m ago` : m<1440?`${Math.round(m/60)}h ago` : `${Math.round(m/1440)}d ago`;
})();
[q,locSel,kindSel,firmSel,fresh].forEach(el=>el.addEventListener('input',render));
render();
</script>
</body>
</html>
"""


def load_firm_kind() -> dict:
    """Map firm name -> 'emp' (direct employer) | 'staff' (staffing/vendor) from config."""
    kind = {}
    try:
        import yaml
        for f in yaml.safe_load(CONFIG.read_text())["firms"]:
            kind[f["name"]] = "emp" if f.get("employer") else "staff"
    except Exception:
        pass
    return kind


def main():
    data = json.loads(DATA.read_text()) if DATA.exists() else {"jobs": [], "count": 0, "updated": "never"}
    jobs = data.get("jobs", [])
    kind = load_firm_kind()
    firms = sorted({j["firm"] for j in jobs}, key=str.lower)
    firm_opts = "".join(f'<option value="{f}">{f}</option>' for f in firms)
    updated_iso = data.get("updated", "") or ""

    html = (TEMPLATE
            .replace("__COUNT__", f"{data.get('count', len(jobs)):,}")
            .replace("__COMPANIES__", str(len(firms)))
            .replace("__REPO__", REPO)
            .replace("__UPDATED_ISO__", updated_iso)
            .replace("__FIRM_OPTS__", firm_opts)
            .replace("__JOBS_JSON__", json.dumps(jobs))
            .replace("__FIRMKIND_JSON__", json.dumps(kind)))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html)
    (OUT.parent / ".nojekyll").write_text("")  # serve raw HTML, skip Jekyll
    print(f"built {OUT} — {BRAND} with {len(jobs)} jobs from {len(firms)} companies")


if __name__ == "__main__":
    main()
