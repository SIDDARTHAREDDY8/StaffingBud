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
### 🆕 13 new roles this update · 6430 tracked total · updated `2026-10-27T15:27:18+00:00`

| Firm | New roles |
| --- | ---: |
| CornerStone TTS | 5 |
| Kforce | 2 |
| Beacon Hill | 2 |
| Apex Systems | 1 |
| Robert Half | 1 |
| Alldus | 1 |
| Motion Recruitment | 1 |

| Role | Firm | Location | Found |
| --- | --- | --- | --- |
| [Data Scientist](http://www.kforce.com/Jobs/1696~EQG~2192372T1~99/) | Kforce | Miami, FL | 2026-10-27 |
| [Senior Data Engineer](http://www.kforce.com/Jobs/1696~TVT~2192501T1~99/) | Kforce | Sandy Springs, GA | 2026-10-27 |
| [Sr. Fabric Developer](https://www.apexsystems.com/job/3055075_usa/sr-fabric-developer) | Apex Systems | Houston, TX | 2026-10-27 |
| [Software Engineering Manager](https://www.roberthalf.com/us/en/job/greater-cleveland-oh/software-engineering-manager/03340-0013481844-usen) | Robert Half | — | 2026-10-27 |
| [Forward Deployed Engineer Ai New York](https://alldus.com/job/59382-forward-deployed-engineer-ai-new-york/) | Alldus | New York | 2026-10-27 |
| [Senior Infrastructure Engineer](https://jobs.cornerstonetechtalent.com/jb/Senior-Infrastructure-Engineer-Jobs-in-Denton-Texas/14376705) | CornerStone TTS | Denton Texas | 2026-10-27 |
| [Senior Platform Engineer â AWS/Azure Cloud & DevOps](https://jobs.cornerstonetechtalent.com/jb/Senior-Platform-Engineer-AWS-Azure-Cloud-DevOps-Jobs-in-Richardson-Texas/14376692) | CornerStone TTS | Richardson Texas | 2026-10-27 |
| [Senior Infrastructure Engineer](https://jobs.cornerstonetechtalent.com/jb/Senior-Infrastructure-Engineer-Jobs-in-Dallas-Texas/14376673) | CornerStone TTS | Dallas Texas | 2026-10-27 |
| [Sr. PBM Data Analyst](https://jobs.cornerstonetechtalent.com/jb/Sr-PBM-Data-Analyst-Jobs-in-Dallas-Texas/14376543) | CornerStone TTS | Dallas Texas | 2026-10-27 |
| [Senior Java Developer](https://jobs.cornerstonetechtalent.com/jb/Senior-Java-Developer-Jobs-in-Atlanta-GA-Georgia/14376434) | CornerStone TTS | Atlanta GA Georgia | 2026-10-27 |
| [Software Engineer, Test Automation](https://motionrecruitment.com/tech-jobs/boston/contract/software-engineer-test-automation/893434) | Motion Recruitment | Boston, MA | 2026-10-27 |
| [OpenShift AI Senior Consultant (part time)](https://bhsg.com/jobs/job/1478946_1793109934-openshift-ai-senior-consultant-part-time-raleigh-north-carolina/) | Beacon Hill | — | 2026-10-27 |
| [ServiceNow Developer](https://bhsg.com/jobs/job/t1479514-phi_1793105971-servicenow-developer-malvern-pennsylvania/) | Beacon Hill | — | 2026-10-27 |
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
