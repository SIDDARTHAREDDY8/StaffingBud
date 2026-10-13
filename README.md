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
### 🆕 17 new roles this update · 9494 tracked total · updated `2026-10-13T06:18:15+00:00`

| Firm | New roles |
| --- | ---: |
| Artech | 5 |
| Robert Half | 4 |
| TEKsystems | 2 |
| Compunnel | 2 |
| Kforce | 1 |
| Mindlance | 1 |
| Harnham | 1 |
| Brooksource | 1 |

| Role | Firm | Location | Found |
| --- | --- | --- | --- |
| [VP of Data Analytics and AI](http://www.kforce.com/Jobs/1696~WQG~2191184P1~99/) | Kforce | Kansas City, MO | 2026-10-13 |
| [Operations Data Analyst](https://careers.teksystems.com/us/en/job/JP-006347379/Operations-Data-Analyst) | TEKsystems | Rosemead, California | 2026-10-13 |
| [Arc Gis Web Developer](https://careers.teksystems.com/us/en/job/JP-006347068/Arc-Gis-Web-Developer) | TEKsystems | Austin, Texas | 2026-10-13 |
| [Site Reliability Engineer](https://www.roberthalf.com/us/en/job/austin-tx/site-reliability-engineer/04160-9504410365-usen) | Robert Half | Austin, 04160 | 2026-10-13 |
| [Software Developer](https://www.roberthalf.com/us/en/job/san-antonio-tx/software-developer/04080-0013478756-usen) | Robert Half | San Antonio, 04080 | 2026-10-13 |
| [Ai Consultant](https://www.roberthalf.com/us/en/job/edison-nj/ai-consultant/02720-0013432154-usen) | Robert Half | Edison, 02720 | 2026-10-13 |
| [Software Engineer](https://www.roberthalf.com/us/en/job/sinton-tx/software-engineer/04080-0013491854-usen) | Robert Half | Sinton, 04080 | 2026-10-13 |
| [Azure Lead /Senior Developer](https://www1.jobdiva.com/portal/?a=kvjdnwtsxgckrpsoozx5qc0oueybw1005779v7x6soig8eyqqmzaubfdl9tcx21s&compid=0&jobid=33234763#/jobs/33234763) | Artech | San Francisco, CA | 2026-10-13 |
| [AI Platform Optimization Lead Engineer](https://www1.jobdiva.com/portal/?a=kvjdnwtsxgckrpsoozx5qc0oueybw1005779v7x6soig8eyqqmzaubfdl9tcx21s&compid=0&jobid=33234980#/jobs/33234980) | Artech | Austin, TX | 2026-10-13 |
| [Product Design and Development - COLOR DEVELOPER II](https://www1.jobdiva.com/portal/?a=kvjdnwtsxgckrpsoozx5qc0oueybw1005779v7x6soig8eyqqmzaubfdl9tcx21s&compid=0&jobid=33235109#/jobs/33235109) | Artech | Beaverton, OR | 2026-10-13 |
| [Application Architect III](https://www1.jobdiva.com/portal/?a=kvjdnwtsxgckrpsoozx5qc0oueybw1005779v7x6soig8eyqqmzaubfdl9tcx21s&compid=0&jobid=33230913#/jobs/33230913) | Artech | Jersey City, NJ | 2026-10-13 |
| [Ruby on Rails Software Engineer](https://www1.jobdiva.com/portal/?a=kvjdnwtsxgckrpsoozx5qc0oueybw1005779v7x6soig8eyqqmzaubfdl9tcx21s&compid=0&jobid=33233880#/jobs/33233880) | Artech | Austin, TX, TX | 2026-10-13 |
| [Software Engineer](https://www2.jobdiva.com/portal/?a=7fjdnw91pq69jlvngz1gp518iugamw00c66623tmx447r7e3lkr3gqqpqjhpy8mo&compid=0&jobid=29454438#/jobs/29454438) | Mindlance | Union, NJ | 2026-10-13 |
| [Full Stack Java API + React Developer](https://jobs.compunnel.com/jobs/5950572) | Compunnel | Aliso Viejo, California, United States | 2026-10-13 |
| [Senior Data Engineer](https://jobs.compunnel.com/jobs/5836323) | Compunnel | Durham, North Carolina, United States | 2026-10-13 |
| [DATA ENGINEER](https://www.harnham.com/job/eb8cdd1a-d1d1-4f13-3bd8-08d5dc096ea6-data-engineer-colorado/) | Harnham | Colorado | 2026-10-13 |
| [Technical Lead – Data Science/GCP Architect](https://jobs.brooksource.com/jobs/job/a1wcv000000vnmtea2-technical-lead-data-science-gcp-architect-denver-colorado/) | Brooksource | Denver, Colorado | 2026-10-13 |
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
