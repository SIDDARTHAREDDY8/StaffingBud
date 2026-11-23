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
### 🆕 16 new roles this update · 3302 tracked total · updated `2026-11-23T23:54:45+00:00`

| Firm | New roles |
| --- | ---: |
| Robert Half | 8 |
| Motion Recruitment | 3 |
| TEKsystems | 2 |
| Kforce | 1 |
| Vaco | 1 |
| Brooksource | 1 |

| Role | Firm | Location | Found |
| --- | --- | --- | --- |
| [Software Engineer](http://www.kforce.com/Jobs/1696~AQG~2195043T1~99/) | Kforce | Shelton, CT | 2026-11-23 |
| [Mid- Senior ServiceNow Developer](https://careers.teksystems.com/us/en/job/JP-006440031/Mid-Senior-ServiceNow-Developer) | TEKsystems | Ogden, Utah | 2026-11-23 |
| [Robotics Application Engineer](https://careers.teksystems.com/us/en/job/JP-006437477/Robotics-Application-Engineer) | TEKsystems | Mountain View, California | 2026-11-23 |
| [Platform Engineer](https://www.roberthalf.com/us/en/job/wayzata-mn/platform-engineer/04838-0013528443-usen) | Robert Half | Wayzata, 04838 | 2026-11-23 |
| [Senior Data Engineer](https://www.roberthalf.com/us/en/job/santa-monica-ca/senior-data-engineer/04838-0013540293-usen) | Robert Half | Santa Monica, 04838 | 2026-11-23 |
| [Full Stack Net Developer](https://www.roberthalf.com/us/en/job/ankeny-ia/full-stack-net-developer/01500-0013520076-usen) | Robert Half | Ankeny, 01500 | 2026-11-23 |
| [Data Engineer](https://www.roberthalf.com/us/en/job/st-paul-mn/data-engineer/02310-0013511415-usen) | Robert Half | St. Paul, 02310 | 2026-11-23 |
| [Aws Senior Data Engineer](https://www.roberthalf.com/us/en/job/torrance-ca/aws-senior-data-engineer/04837-0013541205-usen) | Robert Half | Torrance, 04837 | 2026-11-23 |
| [Junior Data Analyst](https://www.roberthalf.com/us/en/job/peachtree-corners-ga/junior-data-analyst/00900-0013539246-usen) | Robert Half | Peachtree Corners, 00900 | 2026-11-23 |
| [Staff Data Engineer](https://www.roberthalf.com/us/en/job/brookfield-wi/staff-data-engineer/04600-0013541184-usen) | Robert Half | Brookfield, 04600 | 2026-11-23 |
| [Ai Consultant](https://www.roberthalf.com/us/en/job/lansdale-pa/ai-consultant/03720-0013539810-usen) | Robert Half | Lansdale, 03720 | 2026-11-23 |
| [Senior Developer Ms Dynamics](https://jobs.vaco.com/job/3306/senior_developer_ms_dynamics/en) | Vaco | Louisville, Kentucky | 2026-11-23 |
| [Senior AI Security Engineer](https://motionrecruitment.com/tech-jobs/plano/contract/senior-ai-security-engineer/892944) | Motion Recruitment | PLANO, Texas | 2026-11-23 |
| [Cybersecurity Engineer / Contract / Remote](https://motionrecruitment.com/tech-jobs/new-york/contract/cybersecurity-engineer-contract-remote/895397) | Motion Recruitment | New York, NY | 2026-11-23 |
| [Lead Software Engineer / Node / Okta](https://motionrecruitment.com/tech-jobs/chicago/contract/lead-software-engineer-node-okta/895500) | Motion Recruitment | Chicago, Illinois | 2026-11-23 |
| [Data Analyst](https://jobs.brooksource.com/jobs/job/a1wcv000001elg1eac-data-analyst-morris-plains-new-jersey/) | Brooksource | Morris Plains, New Jersey | 2026-11-23 |
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
