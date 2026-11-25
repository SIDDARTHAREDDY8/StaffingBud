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
### 🆕 13 new roles this update · 3223 tracked total · updated `2026-11-25T19:08:09+00:00`

| Firm | New roles |
| --- | ---: |
| Robert Half | 6 |
| Agility Connect | 2 |
| Harnham | 2 |
| Kforce | 1 |
| TEKsystems | 1 |
| Motion Recruitment | 1 |

| Role | Firm | Location | Found |
| --- | --- | --- | --- |
| [AI Automation Engineer DevOps](http://www.kforce.com/Jobs/1696~EQG~2195308T1~99/) | Kforce | Altamonte Springs, FL | 2026-11-25 |
| [Infrastructure Engineer](https://careers.teksystems.com/us/en/job/JP-006441583/Infrastructure-Engineer) | TEKsystems | Napa, California | 2026-11-25 |
| [Data Engineer](https://www.roberthalf.com/us/en/job/chicago-il/data-engineer/01300-0013433936-usen) | Robert Half | Chicago, 01300 | 2026-11-25 |
| [Data Analyst](https://www.roberthalf.com/us/en/job/avon-oh/data-analyst/03340-0013539287-usen) | Robert Half | Avon, 03340 | 2026-11-25 |
| [Data Analyst](https://www.roberthalf.com/us/en/job/nashville-tn/data-analyst/03930-9504432314-usen) | Robert Half | Nashville, 03930 | 2026-11-25 |
| [Software Developer](https://www.roberthalf.com/us/en/job/houston-tx/software-developer/04130-9504432796-usen) | Robert Half | Houston, 04130 | 2026-11-25 |
| [Solutions Architect](https://www.roberthalf.com/us/en/job/atlanta-ga/solutions-architect/00920-9504430877-usen) | Robert Half | Atlanta, 00920 | 2026-11-25 |
| [Net Developer](https://www.roberthalf.com/us/en/job/nashville-tn/net-developer/03930-9504432318-usen) | Robert Half | Nashville, 03930 | 2026-11-25 |
| [Sr. Software Engineer](https://motionrecruitment.com/tech-jobs/x/direct-hire/srdot-software-engineer/895611) | Motion Recruitment | Georgia | 2026-11-25 |
| [SaaS Security Engineer](https://agilityconnect.io/jobs/8645) | Agility Connect | OH | 2026-11-25 |
| [Sr Data Scientist](https://agilityconnect.io/jobs/8646) | Agility Connect | OH | 2026-11-25 |
| [STAFF AI SOFTWARE ENGINEER](https://www.harnham.com/job/eb8cdd1a-d1d1-4f13-3bd8-08d5dc096ea6-staff-ai-software-engineer-frisco-texas/) | Harnham | Frisco, Texas | 2026-11-25 |
| [LEAD DATA ENGINEER](https://www.harnham.com/job/e1aeb1da-8723-4ba1-d23d-08d5948a7341-lead-data-engineer-reading-berkshire/) | Harnham | Reading, Berkshire | 2026-11-25 |
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
