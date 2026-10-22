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
### 🆕 18 new roles this update · 7487 tracked total · updated `2026-10-22T11:33:27+00:00`

| Firm | New roles |
| --- | ---: |
| TEKsystems | 5 |
| Alldus | 5 |
| Mindlance | 2 |
| Agility Connect | 2 |
| Harnham | 2 |
| Robert Half | 1 |
| Net2Source | 1 |

| Role | Firm | Location | Found |
| --- | --- | --- | --- |
| [Data Architect - Databricks (W2 Only / No C2C)](https://careers.teksystems.com/us/en/job/JP-006368552/Data-Architect-Databricks-W2-Only-No-C2C) | TEKsystems | Long Island City, New York | 2026-10-22 |
| [AI Architect (W2 Only / No C2C)](https://careers.teksystems.com/us/en/job/JP-006368521/AI-Architect-W2-Only-No-C2C) | TEKsystems | Long Island City, New York | 2026-10-22 |
| [Micro Focus Cobol Developer](https://careers.teksystems.com/us/en/job/JP-006367058/Micro-Focus-Cobol-Developer) | TEKsystems | Greensboro, North Carolina | 2026-10-22 |
| [AI Governance Lead Program Consultant](https://careers.teksystems.com/us/en/job/JP-006366512/AI-Governance-Lead-Program-Consultant) | TEKsystems | Rochester, New York | 2026-10-22 |
| [Sr. .NET Developer](https://careers.teksystems.com/us/en/job/JP-006363877/Sr-NET-Developer) | TEKsystems | Charlotte, North Carolina | 2026-10-22 |
| [Software Developer](https://www.roberthalf.com/us/en/job/norman-ok/software-developer/03500-0013516129-usen) | Robert Half | Norman, 03500 | 2026-10-22 |
| [Ai Engineer New York](https://alldus.com/job/59268-ai-engineer-new-york/) | Alldus | New York | 2026-10-22 |
| [Member Of Technical Staff Backend Ai New York City New York](https://alldus.com/job/59269-member-of-technical-staff-backend-ai-new-york-city-new-york/) | Alldus | New York City, New York | 2026-10-22 |
| [Forward Deployed Engineer Deployment Strategist New York City New York](https://alldus.com/job/59270-forward-deployed-engineer-deployment-strategist-new-york-city-new-york/) | Alldus | New York City, New York | 2026-10-22 |
| [Servicenow Developer Nsapoly Maryland](https://alldus.com/job/59288-servicenow-developer-nsapoly-maryland/) | Alldus | Maryland | 2026-10-22 |
| [Senior Backend Engineer Platform New York New York](https://alldus.com/job/59305-senior-backend-engineer-platform-new-york-new-york/) | Alldus | New York, New York | 2026-10-22 |
| [Snowflake Data Engineer](https://www2.jobdiva.com/portal/?a=7fjdnw91pq69jlvngz1gp518iugamw00c66623tmx447r7e3lkr3gqqpqjhpy8mo&compid=0&jobid=29501788#/jobs/29501788) | Mindlance | Coppell, TX | 2026-10-22 |
| [MS Access Developer / Analyst](https://www2.jobdiva.com/portal/?a=7fjdnw91pq69jlvngz1gp518iugamw00c66623tmx447r7e3lkr3gqqpqjhpy8mo&compid=0&jobid=29500532#/jobs/29500532) | Mindlance | Washington, DC | 2026-10-22 |
| [Senior Data Engineer & BI Developer](https://www2.jobdiva.com/portal/?a=fyjdnwkqny26xqof9rceu6y6gam6750308agqi8uui1cmk3v9j6duy26aoewnusi&compid=0&jobid=29504693#/jobs/29504693) | Net2Source | Foster City, CA | 2026-10-22 |
| [MLOps Engineer](https://agilityconnect.io/jobs/8565) | Agility Connect | Cincinnati, OH | 2026-10-22 |
| [Sr Solutions Architect](https://agilityconnect.io/jobs/8563) | Agility Connect | OH | 2026-10-22 |
| [DATA SCIENTIST/DATA ANALYST](https://www.harnham.com/job/e1aeb1da-8723-4ba1-d23d-08d5948a7341-data-scientist-data-analyst-windsor-and-maidenhead-berkshire/) | Harnham | Windsor and Maidenhead, Berkshire | 2026-10-22 |
| [DATA SCIENTIST](https://www.harnham.com/job/e1aeb1da-8723-4ba1-d23d-08d5948a7341-data-scientist-windsor-berkshire-2/) | Harnham | Windsor, Berkshire | 2026-10-22 |
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
