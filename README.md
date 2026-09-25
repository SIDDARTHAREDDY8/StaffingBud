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
### 🆕 9 new roles this update · 14564 tracked total · updated `2026-09-25T04:20:24+00:00`

| Firm | New roles |
| --- | ---: |
| Robert Half | 4 |
| Artech | 3 |
| Russell Tobin | 1 |
| Harnham | 1 |

| Role | Firm | Location | Found |
| --- | --- | --- | --- |
| [Data Scientist](https://www.roberthalf.com/us/en/job/jacksonville-fl/data-scientist/00920-0013501637-usen) | Robert Half | Jacksonville, 00920 | 2026-09-25 |
| [Ai Solution Engineer](https://www.roberthalf.com/us/en/job/nashville-tn/ai-solution-engineer/03930-0013468814-usen) | Robert Half | Nashville, 03930 | 2026-09-25 |
| [Firmware Engineer](https://www.roberthalf.com/us/en/job/largo-fl/firmware-engineer/01070-0013429268-usen) | Robert Half | Largo, 01070 | 2026-09-25 |
| [Senior Oracle Developer](https://www.roberthalf.com/us/en/job/ogden-ut/senior-oracle-developer/04820-0013506126-usen) | Robert Half | Ogden, 04820 | 2026-09-25 |
| [Site Reliability Engineer - Remote](https://www2.jobdiva.com/portal/?a=nyjdnw8rs3eurnjvdink7d2fl4mnyy0b22tjlzi328snknlo1pzpk0ue533mvm7r&compid=2&jobid=29359273#/jobs/29359273) | Russell Tobin | Santa Clara, CA | 2026-09-25 |
| [ASP.NET Developer](https://www1.jobdiva.com/portal/?a=kvjdnwtsxgckrpsoozx5qc0oueybw1005779v7x6soig8eyqqmzaubfdl9tcx21s&compid=0&jobid=33146978#/jobs/33146978) | Artech | Raleigh, NC | 2026-09-25 |
| [Customer Identity & Access Management (CIAM) Developer](https://www1.jobdiva.com/portal/?a=kvjdnwtsxgckrpsoozx5qc0oueybw1005779v7x6soig8eyqqmzaubfdl9tcx21s&compid=0&jobid=33148640#/jobs/33148640) | Artech | Phoenix, AZ | 2026-09-25 |
| [Gaming - Embedded Software Engineer II](https://www1.jobdiva.com/portal/?a=kvjdnwtsxgckrpsoozx5qc0oueybw1005779v7x6soig8eyqqmzaubfdl9tcx21s&compid=0&jobid=33148141#/jobs/33148141) | Artech | Sunnyvale, CA | 2026-09-25 |
| [SENIOR DATA SCIENTIST](https://www.harnham.com/job/eb8cdd1a-d1d1-4f13-3bd8-08d5dc096ea6-senior-data-scientist-nashville-tennessee/) | Harnham | Nashville, Tennessee | 2026-09-25 |
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
