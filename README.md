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
### 🆕 8 new roles this update · 4257 tracked total · updated `2026-11-12T06:34:49+00:00`

| Firm | New roles |
| --- | ---: |
| Robert Half | 4 |
| TEKsystems | 1 |
| Apex Systems | 1 |
| Compunnel | 1 |
| Beacon Hill | 1 |

| Role | Firm | Location | Found |
| --- | --- | --- | --- |
| [Enterprise Data Analytics Manager](https://careers.teksystems.com/us/en/job/JP-006410835/Enterprise-Data-Analytics-Manager) | TEKsystems | Rochester, New York | 2026-11-12 |
| [Principal AI Platform Engineer](https://www.apexsystems.com/job/3058816_usa/principal-ai-platform-engineer) | Apex Systems | Seattle, WA | 2026-11-12 |
| [Inventory Data Analyst](https://www.roberthalf.com/us/en/job/bloomington-mn/inventory-data-analyst/02340-0013528124-usen) | Robert Half | Bloomington, 02340 | 2026-11-12 |
| [Site Reliability Engineer](https://www.roberthalf.com/us/en/job/austin-tx/site-reliability-engineer/04160-9504426428-usen) | Robert Half | Austin, 04160 | 2026-11-12 |
| [Ai Sourcer Human Resources](https://www.roberthalf.com/us/en/job/san-mateo-ca/ai-sourcer-human-resources/00430-9504426399-usen) | Robert Half | San Mateo, 00430 | 2026-11-12 |
| [Devops Engineer](https://www.roberthalf.com/us/en/job/austin-tx/devops-engineer/04160-9504426425-usen) | Robert Half | Austin, 04160 | 2026-11-12 |
| [Agentic AI Developer](https://jobs.compunnel.com/jobs/6104877) | Compunnel | New York City, New York, United States | 2026-11-12 |
| [Solutions/Platform Engineer](https://bhsg.com/jobs/job/san-tt-1479543_1794440676-solutions-platform-engineer-san-diego-california/) | Beacon Hill | — | 2026-11-12 |
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
