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
### 🆕 11 new roles this update · 4507 tracked total · updated `2026-11-10T16:59:02+00:00`

| Firm | New roles |
| --- | ---: |
| Compunnel | 5 |
| TEKsystems | 1 |
| Robert Half | 1 |
| Motion Recruitment | 1 |
| Agility Connect | 1 |
| Brooksource | 1 |
| Beacon Hill | 1 |

| Role | Firm | Location | Found |
| --- | --- | --- | --- |
| [Applied Computer Vision Data Scientist](https://careers.teksystems.com/us/en/job/JP-006411207/Applied-Computer-Vision-Data-Scientist) | TEKsystems | Bentonville, Arkansas | 2026-11-10 |
| [Staff Database Engineer](https://www.roberthalf.com/us/en/job/salt-lake-city-ut/staff-database-engineer/04820-0013467136-usen) | Robert Half | Salt Lake City, 04820 | 2026-11-10 |
| [Full Stack Software Engineer / AI Platform / NYC](https://motionrecruitment.com/tech-jobs/new-york/direct-hire/full-stack-software-engineer-ai-platform-nyc/894595) | Motion Recruitment | New York, New York | 2026-11-10 |
| [Full Stack Engineer](https://jobs.compunnel.com/jobs/5836017) | Compunnel | Westlake, Texas, United States | 2026-11-10 |
| [Staff Engineer AI](https://jobs.compunnel.com/jobs/5960944) | Compunnel | Denver, Colorado, United States | 2026-11-10 |
| [Facet extension Developer](https://jobs.compunnel.com/jobs/6104868) | Compunnel | Richmond, Virginia, United States | 2026-11-10 |
| [Power Platform Developer](https://jobs.compunnel.com/jobs/6114476) | Compunnel | Westminster, Colorado, United States | 2026-11-10 |
| [ETRM Developer](https://jobs.compunnel.com/jobs/6062951) | Compunnel | Houston, Texas, United States | 2026-11-10 |
| [Software Engineer](https://agilityconnect.io/jobs/8556) | Agility Connect | Columbus, OH | 2026-11-10 |
| [AI Program Lead](https://jobs.brooksource.com/jobs/job/a1wcv000001ctdleao-ai-program-lead-new-york-new-york/) | Brooksource | New York, New York | 2026-11-10 |
| [Sr. ServiceNow Developer](https://bhsg.com/jobs/job/1481217sn_1794321903-sr-servicenow-developer-raleigh-north-carolina/) | Beacon Hill | — | 2026-11-10 |
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
