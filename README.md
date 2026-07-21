# StaffingBuddy 💼

**A free, auto-updating job board for contract IT roles from staffing firms & IT vendors.**

Most contract software/IT work flows through staffing vendors — and checking each one's
career page by hand is tedious. StaffingBuddy watches **16+ firms** (TEKsystems, Kforce,
Collabera, Insight Global, Belcan, Agility, KellyMitchell, Harnham, …) and pulls every new
**IT contract role** — software & full-stack engineers, web developers, data/ML/AI,
cloud/DevOps, QA, and more — into one place, refreshed **every 3 hours**. No login, no cost.

### 👉 [Browse the live job board »](https://siddarthareddy8.github.io/StaffingBud/)

*(Searchable, filterable webpage — enable once via Settings → Pages → main → /docs.)*

**For job seekers** hunting contract/C2C IT roles: skip the 16-tab ritual. The list below
is a **feed of newly-found roles** — each job appears once (the run it's discovered), with a
direct apply link, so you only ever see what's new since you last looked.

| | |
| --- | --- |
| 🔄 **Refresh** | every 3 hours via GitHub Actions |
| 🎯 **Scope** | contract / contract-to-hire IT roles, US-wide |
| 🧹 **Filtered** | keeps IT; drops sales, nursing, warehouse, clearance, non-IT analyst/engineer roles |
| 📦 **Archive** | full searchable board at [`docs/index.html`](docs/index.html) · raw data in [`data/jobs.json`](data/jobs.json) |
| 🧭 **Sibling** | [JobsBuddy](https://github.com/SIDDARTHAREDDY8/JobsBuddy) does the same for full-time, H1B-sponsor roles |

## 🆕 Live Jobs

<!-- JOBS:START -->
### 🆕 13 new roles this update · 8261 tracked total · updated `2026-07-21T22:14:20+00:00`

| Firm | New roles |
| --- | ---: |
| Artech | 6 |
| Insight Global | 2 |
| CRG | 1 |
| Motion Recruitment | 1 |
| Net2Source | 1 |
| Brooksource | 1 |
| Njoyn (CGI) | 1 |

| Role | Firm | Location | Found |
| --- | --- | --- | --- |
| [Data Engineer - INTL India](https://jobs.insightglobal.com/jobs/find_a_job/washington/seattle/data-engineer-intl-india/job-554959/) | Insight Global | Seattle, WA | 2026-07-21 |
| [Actuarial Developer](https://jobs.insightglobal.com/jobs/find_a_job/oregon/portland/actuarial-developer/job-551983/) | Insight Global | Portland, OR | 2026-07-21 |
| [S4 HANA ABAP Developer](https://jobs.getcrg.com/jobs/16596) | CRG | Charlotte, North Carolina | 2026-07-21 |
| [Technical Solutions Architect - EPIC](https://motionrecruitment.com/tech-jobs/boston/contract/technical-solutions-architect-epic/883189) | Motion Recruitment | Boston, MA | 2026-07-21 |
| [Principal or Senior Principal Software Engineer - Navigation](https://www1.jobdiva.com/portal/?a=kvjdnwtsxgckrpsoozx5qc0oueybw1005779v7x6soig8eyqqmzaubfdl9tcx21s&compid=0&jobid=32733913#/jobs/32733913) | Artech | Woodland Hills, CA | 2026-07-21 |
| [Data Engineer](https://www1.jobdiva.com/portal/?a=kvjdnwtsxgckrpsoozx5qc0oueybw1005779v7x6soig8eyqqmzaubfdl9tcx21s&compid=0&jobid=32734514#/jobs/32734514) | Artech | San Jose, CA | 2026-07-21 |
| [Java with Cloud Developer](https://www1.jobdiva.com/portal/?a=kvjdnwtsxgckrpsoozx5qc0oueybw1005779v7x6soig8eyqqmzaubfdl9tcx21s&compid=0&jobid=32734013#/jobs/32734013) | Artech | Princeton, NJ | 2026-07-21 |
| [Data Architect](https://www1.jobdiva.com/portal/?a=kvjdnwtsxgckrpsoozx5qc0oueybw1005779v7x6soig8eyqqmzaubfdl9tcx21s&compid=0&jobid=32733938#/jobs/32733938) | Artech | San Jose, CA | 2026-07-21 |
| [JAVA Springboot developer](https://www1.jobdiva.com/portal/?a=kvjdnwtsxgckrpsoozx5qc0oueybw1005779v7x6soig8eyqqmzaubfdl9tcx21s&compid=0&jobid=32732700#/jobs/32732700) | Artech | Plano, TX | 2026-07-21 |
| [Data Analyst II](https://www1.jobdiva.com/portal/?a=kvjdnwtsxgckrpsoozx5qc0oueybw1005779v7x6soig8eyqqmzaubfdl9tcx21s&compid=0&jobid=32733457#/jobs/32733457) | Artech | St. Paul, MN | 2026-07-21 |
| [Software Engineer 3](https://www2.jobdiva.com/portal/?a=fyjdnwkqny26xqof9rceu6y6gam6750308agqi8uui1cmk3v9j6duy26aoewnusi&compid=0&jobid=28763779#/jobs/28763779) | Net2Source | Chillicothe, IL | 2026-07-21 |
| [Information Security Engineer- Cisco SWA](https://jobs.brooksource.com/jobs/job/a1wcv000000qd1beau-information-security-engineer-cisco-swa-chicago-illinois/) | Brooksource | Chicago, Illinois | 2026-07-21 |
| [Mid Level Angular Developer](https://cgi.njoyn.com/CORP/xweb/xweb.asp?NTKN=c&clid=21001&Page=JobDetails&Jobid=J0726-1773&BRID=1318318&lang=1) | Njoyn (CGI) | Huntsville, United States | 2026-07-21 |
<!-- JOBS:END -->

## How it works

```
config/firms.yaml   →  one entry per firm (URL + how to read its job cards)
scraper/engine.py   →  fetch each firm (api / api_html / dom / apify_search)
scraper/filters.py  →  keep IT roles, drop non-IT; US/Cincinnati/remote locations
scraper/store.py    →  dedupe + first-seen tracking into data/jobs.json
build_site.py       →  render data/jobs.json into docs/index.html (GitHub Pages)
build_readme.py     →  inject newly-found roles into this README (JOBS markers)
.github/workflows   →  run every 3 hours, commit fresh jobs + site + README
```

Each firm can run in one of two modes:

- **`dom`** — Playwright renders the page and reads job cards via CSS selectors.
  Works on any site. Breaks if the firm redesigns (just re-fix the selectors).
- **`api`** — call the JSON endpoint the page itself calls (DevTools → Network → XHR).
  Faster and more stable. Use it when you can find the endpoint.

## Setup

```bash
cd staffing-buddy
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
```

## Run

```bash
python run.py                      # all firms
python run.py --only "TEKsystems"  # one firm
python run.py --headful            # watch the browser (debug selectors)
python build_site.py               # rebuild the HTML board
open site/index.html
```

## Calibrating a firm  (the one manual step)

Career pages differ, so each firm needs its selectors confirmed once:

1. Open the firm's job-search URL in Chrome.
2. Right-click a job listing → **Inspect**.
3. Find the repeating container element → that's your `card` selector.
4. Inside it, find the title / location / link elements → fill those selectors.
5. Run `python run.py --only "<Firm>" --headful` and watch it pull jobs.

**Tip:** before writing selectors, check the **Network → XHR** tab. If you see a
clean JSON request returning the jobs, switch that firm to `mode: api` instead —
it's far more reliable than scraping rendered HTML.

## Adding more firms

Append to `config/firms.yaml`. Your Desktop already has
`Comprehensive_List_of_US_Tech_Staffing_&_Vendor_Companies.pdf` — pull names from there.

## Notes / honesty

- These firms **want** their jobs found (that's how they fill reqs), so listings are
  public — no login wall.
- Be polite: the 6-hour cron is plenty. Don't hammer.
- Some firms use anti-bot (Cloudflare). If a firm returns nothing in `dom` mode,
  it may need `mode: api` or an Apify Actor.
- Selectors in `firms.yaml` are **starting points** and must be confirmed live.
