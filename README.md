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
### 🆕 17 new roles this update · 4756 tracked total · updated `2026-11-09T22:11:48+00:00`

| Firm | New roles |
| --- | ---: |
| Kforce | 4 |
| TEKsystems | 4 |
| Brooksource | 3 |
| Apex Systems | 2 |
| Vaco | 2 |
| Robert Half | 1 |
| Motion Recruitment | 1 |

| Role | Firm | Location | Found |
| --- | --- | --- | --- |
| [Data Analyst](http://www.kforce.com/Jobs/1696~AQG~2193732T1~99/) | Kforce | Hoboken, NJ | 2026-11-09 |
| [Senior Ignition Application Engineer](http://www.kforce.com/Jobs/1696~TVT~2193787T1~99/) | Kforce | Maiden, NC | 2026-11-09 |
| [ELSUR Collection Systems Database Engineer Mid](http://www.kforce.com/Jobs/1696~AQG~2193708T1~99/) | Kforce | Mc Lean, VA | 2026-11-09 |
| [Program Tooling & Analytics Developer](http://www.kforce.com/Jobs/1696~WQG~2193718T1~99/) | Kforce | Foster City, CA | 2026-11-09 |
| [HL7 FHIR Data Engineer (W2 ONLY)](https://careers.teksystems.com/us/en/job/JP-006409259/HL7-FHIR-Data-Engineer-W2-ONLY) | TEKsystems | Phoenix, Arizona | 2026-11-09 |
| [Principal Software Architect](https://careers.teksystems.com/us/en/job/JP-006408913/Principal-Software-Architect) | TEKsystems | Irvine, California | 2026-11-09 |
| [HL7 FHIR Data Engineer (W2 ONLY)](https://careers.teksystems.com/us/en/job/JP-006409252/HL7-FHIR-Data-Engineer-W2-ONLY) | TEKsystems | Dallas, Texas | 2026-11-09 |
| [Principal AI Architect](https://careers.teksystems.com/us/en/job/JP-006409572/Principal-AI-Architect) | TEKsystems | Dallas, Texas | 2026-11-09 |
| [ServiceNow Developer](https://www.apexsystems.com/job/3058578_usa/servicenow-developer) | Apex Systems | Richmond, VA | 2026-11-09 |
| [Workday Developer](https://www.apexsystems.com/job/3058702_usa/workday-developer) | Apex Systems | Atlanta, GA | 2026-11-09 |
| [Data Scientist B2C Consumer Trends](https://www.roberthalf.com/us/en/job/richmond-va/data-scientist-b2c-consumer-trends/04836-9504424154-usen) | Robert Half | Richmond, 04836 | 2026-11-09 |
| [Principal Ai Software Architect](https://jobs.vaco.com/job/2985/principal_ai_software_architect/en) | Vaco | St. Louis, Missouri | 2026-11-09 |
| [Data Engineer Snowflake](https://jobs.vaco.com/job/2993/data_engineer_snowflake/en) | Vaco | Nashville, Tennessee | 2026-11-09 |
| [Android Developer](https://motionrecruitment.com/tech-jobs/irving/contract/android-developer/893318) | Motion Recruitment | Irving, Texas | 2026-11-09 |
| [AI Engineer](https://jobs.brooksource.com/jobs/job/a1wcv000001c1pneas-ai-engineer-sunrise-florida/) | Brooksource | Sunrise, Florida | 2026-11-09 |
| [Senior Frontend Developer](https://jobs.brooksource.com/jobs/job/a1wcv000001cq9reaw-senior-frontend-developer-new-york-new-york/) | Brooksource | New York, New York | 2026-11-09 |
| [AI Engineer – DHS](https://jobs.brooksource.com/jobs/job/a1wcv000001csubeao-ai-engineer-dhs-nashville-tennessee/) | Brooksource | Nashville, Tennessee | 2026-11-09 |
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
