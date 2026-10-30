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
### 🆕 12 new roles this update · 6247 tracked total · updated `2026-10-30T22:10:56+00:00`

| Firm | New roles |
| --- | ---: |
| TEKsystems | 3 |
| Robert Half | 2 |
| CornerStone TTS | 2 |
| Harnham | 2 |
| Beacon Hill | 2 |
| Kforce | 1 |

| Role | Firm | Location | Found |
| --- | --- | --- | --- |
| [Business/Data Analyst - Senior](http://www.kforce.com/Jobs/1696~TVT~2192972T1~99/) | Kforce | San Antonio, TX | 2026-10-30 |
| [Software Developer](https://careers.teksystems.com/us/en/job/JP-006388970/Software-Developer) | TEKsystems | Omaha, Nebraska | 2026-10-30 |
| [Data Architect](https://careers.teksystems.com/us/en/job/JP-006386537/Data-Architect) | TEKsystems | Rochester, New York | 2026-10-30 |
| [Data Platform Engineer](https://careers.teksystems.com/us/en/job/JP-006386739/Data-Platform-Engineer) | TEKsystems | Rochester, New York | 2026-10-30 |
| [Data Scientist](https://www.roberthalf.com/us/en/job/los-angeles-ca/data-scientist/00320-0013528081-usen) | Robert Half | Los Angeles, 00320 | 2026-10-30 |
| [Cyber Security Engineer](https://www.roberthalf.com/us/en/job/appleton-wi/cyber-security-engineer/04620-0013527493-usen) | Robert Half | Appleton, 04620 | 2026-10-30 |
| [Senior Data Integration Developer - Healthcare & Public Health](https://jobs.cornerstonetechtalent.com/jb/Senior-Data-Integration-Developer-Healthcare-Public-Health-Jobs-in-Austin-Texas/14384394) | CornerStone TTS | Austin Texas | 2026-10-30 |
| [Mainframe Developer (COBOL / Natural / Adabas)](https://jobs.cornerstonetechtalent.com/jb/Mainframe-Developer-COBOL-Natural-Adabas-Jobs-in-Columbia-South-Carolina/14384395) | CornerStone TTS | Columbia South Carolina | 2026-10-30 |
| [AI RESEARCHER](https://www.harnham.com/job/eb8cdd1a-d1d1-4f13-3bd8-08d5dc096ea6-ai-researcher-san-francisco-california-2/) | Harnham | San Francisco, California | 2026-10-30 |
| [LEAD SOFTWARE ENGINEER – FRONTEND](https://www.harnham.com/job/eb8cdd1a-d1d1-4f13-3bd8-08d5dc096ea6-lead-software-engineer-frontend-new-york/) | Harnham | New York | 2026-10-30 |
| [Senior UI Software Engineer,Angular,NestJS,AWS,Redis,Agile](https://bhsg.com/jobs/job/ns-uid-ns_1793391237-senior-ui-software-engineerangularnestjsawsredisagile-seattle-washington/) | Beacon Hill | — | 2026-10-30 |
| [Senior UI Software Engineer](https://bhsg.com/jobs/job/ns-uid-ns_1793390236-senior-ui-software-engineer-orlando-florida/) | Beacon Hill | — | 2026-10-30 |
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
