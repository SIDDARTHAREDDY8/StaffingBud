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
### 🆕 13 new roles this update · 5071 tracked total · updated `2026-11-05T19:49:23+00:00`

| Firm | New roles |
| --- | ---: |
| TEKsystems | 3 |
| Robert Half | 3 |
| Kforce | 2 |
| Apex Systems | 2 |
| Talent Groups | 1 |
| Harnham | 1 |
| Beacon Hill | 1 |

| Role | Firm | Location | Found |
| --- | --- | --- | --- |
| [Data Scientist](http://www.kforce.com/Jobs/1696~EQG~2191544T1~99/) | Kforce | Lansing, MI | 2026-11-05 |
| [Snowflake Platform Engineer](http://www.kforce.com/Jobs/1696~TVT~2193437T1~99/) | Kforce | Minneapolis, MN | 2026-11-05 |
| [Infrastructure Engineer](https://careers.teksystems.com/us/en/job/JP-006399236/Infrastructure-Engineer) | TEKsystems | Reston, Virginia | 2026-11-05 |
| [Entry Level Analytics Developer](https://careers.teksystems.com/us/en/job/JP-006400817/Entry-Level-Analytics-Developer) | TEKsystems | Virginia Beach, Virginia | 2026-11-05 |
| [AI Analyst/Trainer](https://careers.teksystems.com/us/en/job/JP-006399946/AI-Analyst-Trainer) | TEKsystems | Winston Salem, North Carolina | 2026-11-05 |
| [Senior Analytics Engineer](https://www.apexsystems.com/job/3058404_usa/senior-analytics-engineer) | Apex Systems | Tampa, FL | 2026-11-05 |
| [Power Bi Developer](https://www.apexsystems.com/job/3058458_usa/power-bi-developer) | Apex Systems | Saint Paul, MN | 2026-11-05 |
| [Cyber Security Engineer](https://www.roberthalf.com/us/en/job/memphis-tn/cyber-security-engineer/03900-9504421878-usen) | Robert Half | Memphis, 03900 | 2026-11-05 |
| [Full Stack Engineer](https://www.roberthalf.com/us/en/job/jacksonville-fl/full-stack-engineer/01120-9504420148-usen) | Robert Half | Jacksonville, 01120 | 2026-11-05 |
| [Ai Engineer](https://www.roberthalf.com/us/en/job/memphis-tn/ai-engineer/03900-9504421800-usen) | Robert Half | Memphis, 03900 | 2026-11-05 |
| [Oracle Fusion Financial Report Developer](https://www.talentgroups.com/job-details/oracle-fusion-financial-report-developer-in-other-jobs-1787571) | Talent Groups | Houston, TX | 2026-11-05 |
| [DIRECTOR OF AI](https://www.harnham.com/job/eb8cdd1a-d1d1-4f13-3bd8-08d5dc096ea6-director-of-ai-usa/) | Harnham | USA | 2026-11-05 |
| [AI Product Lead (Conversational AI)](https://bhsg.com/jobs/job/1477648_1793897438-ai-product-lead-conversational-ai-raleigh-north-carolina/) | Beacon Hill | — | 2026-11-05 |
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
