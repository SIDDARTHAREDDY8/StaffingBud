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
### 🆕 18 new roles this update · 8180 tracked total · updated `2026-07-22T03:04:10+00:00`

| Firm | New roles |
| --- | ---: |
| Compunnel | 7 |
| TEKsystems | 4 |
| Motion Recruitment | 3 |
| Vaco | 2 |
| Insight Global | 1 |
| Njoyn (CGI) | 1 |

| Role | Firm | Location | Found |
| --- | --- | --- | --- |
| [Senior Cloud Data Architect](https://careers.teksystems.com/us/en/job/JP-006171937/Senior-Cloud-Data-Architect) | TEKsystems | San Jose, California | 2026-07-22 |
| [Lead MDM Analyst -Developer](https://careers.teksystems.com/us/en/job/JP-006171666/Lead-MDM-Analyst-Developer) | TEKsystems | San Diego, California | 2026-07-22 |
| [AI Engineer](https://careers.teksystems.com/us/en/job/JP-006171733/AI-Engineer) | TEKsystems | Round Rock, Texas | 2026-07-22 |
| [Senior Software Engineer (Python/BigQuery/ SQL)](https://careers.teksystems.com/us/en/job/JP-006171855/Senior-Software-Engineer-Python-BigQuery-SQL) | TEKsystems | Chicago, Illinois | 2026-07-22 |
| [Data Engineering Manager](https://jobs.insightglobal.com/jobs/find_a_job/washington/seattle/data-engineering-manager/job-554773/) | Insight Global | Seattle, WA | 2026-07-22 |
| [Back End Developer Java](https://jobs.vaco.com/job/19016/back_end_developer_java/en) | Vaco | Carlsbad, California | 2026-07-22 |
| [Staff Android Developer](https://jobs.vaco.com/job/19017/staff_android_developer/en) | Vaco | Carlsbad, California | 2026-07-22 |
| [Senior Technical Solutions Architect](https://motionrecruitment.com/tech-jobs/boston/contract/senior-technical-solutions-architect/883197) | Motion Recruitment | Boston, MA | 2026-07-22 |
| [Fullstack Engineer / React / Golang](https://motionrecruitment.com/tech-jobs/tampa/direct-hire/fullstack-engineer-react-golang/883193) | Motion Recruitment | tampa, Florida | 2026-07-22 |
| [Cloud Platform Engineer / Mid Level / Remote](https://motionrecruitment.com/tech-jobs/phoenix/direct-hire/cloud-platform-engineer-mid-level-remote/883191) | Motion Recruitment | PHOENIX, Arizona | 2026-07-22 |
| [Full Stack Engineer](https://jobs.compunnel.com/jobs/5837052) | Compunnel | Durham, North Carolina, United States | 2026-07-22 |
| [Power BI Developer](https://jobs.compunnel.com/jobs/5837184) | Compunnel | Westlake, Texas, United States | 2026-07-22 |
| [Lead Data Engineer](https://jobs.compunnel.com/jobs/5837116) | Compunnel | Montvale, New Jersey, United States | 2026-07-22 |
| [Senior AI Architect](https://jobs.compunnel.com/jobs/5837123) | Compunnel | Columbus, Ohio, United States | 2026-07-22 |
| [Software Developer](https://jobs.compunnel.com/jobs/5837326) | Compunnel | Sunnyvale, California, United States | 2026-07-22 |
| [Ui Full Stack Engineer](https://jobs.compunnel.com/jobs/5837109) | Compunnel | Durham, North Carolina, United States | 2026-07-22 |
| [Product Data Analyst](https://jobs.compunnel.com/jobs/5837171) | Compunnel | Westlake, Texas, United States | 2026-07-22 |
| [Sr. Java Backend Engineer](https://cgi.njoyn.com/CORP/xweb/xweb.asp?NTKN=c&clid=21001&Page=JobDetails&Jobid=J0726-1468&BRID=1318391&lang=1) | Njoyn (CGI) | Westlake, United States | 2026-07-22 |
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
