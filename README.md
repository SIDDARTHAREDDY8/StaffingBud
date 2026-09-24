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
### 🆕 13 new roles this update · 14495 tracked total · updated `2026-09-24T04:05:32+00:00`

| Firm | New roles |
| --- | ---: |
| Motion Recruitment | 4 |
| Robert Half | 2 |
| TEKsystems | 1 |
| ProFocus | 1 |
| Artech | 1 |
| Net2Source | 1 |
| Pinnacle Group | 1 |
| Harnham | 1 |
| Njoyn (CGI) | 1 |

| Role | Firm | Location | Found |
| --- | --- | --- | --- |
| [Senior Software Developer](https://careers.teksystems.com/us/en/job/JP-006305631/Senior-Software-Developer) | TEKsystems | Hanover, Maryland | 2026-09-24 |
| [Bi Developer](https://www.roberthalf.com/us/en/job/santa-clara-ca/bi-developer/04410-0013503316-usen) | Robert Half | Santa Clara, 00420 | 2026-09-24 |
| [Software Engineering Manager](https://www.roberthalf.com/us/en/job/chicago-il/software-engineering-manager/01300-0013445151-usen) | Robert Half | Chicago, 01300 | 2026-09-24 |
| [Itsm Platform Engineer Ivanti](https://www.profocustechnology.com/echojobs/itsm-platform-engineer-ivanti-3614/) | ProFocus | — | 2026-09-24 |
| [Full Stack AI Engineer](https://motionrecruitment.com/tech-jobs/cedar-rapids/direct-hire/full-stack-ai-engineer/888305) | Motion Recruitment | Cedar Rapids, Iowa | 2026-09-24 |
| [Senior Software Engineer / React / Python / AI Infrastructure](https://motionrecruitment.com/tech-jobs/sunnyvale/direct-hire/senior-software-engineer-react-python-ai-infrastructure/888304) | Motion Recruitment | Sunnyvale, California | 2026-09-24 |
| [Fullstack Software Engineer / TypeScript / Golang / AI Security](https://motionrecruitment.com/tech-jobs/sunnyvale/direct-hire/fullstack-software-engineer-typescript-golang-ai-security/888298) | Motion Recruitment | Sunnyvale, California | 2026-09-24 |
| [.NET Developer Job in Boston](https://motionrecruitment.com/tech-jobs/boston/contract/dot-net-developer-job-in-boston/888299) | Motion Recruitment | Boston, MA | 2026-09-24 |
| [.NET Developer](https://www1.jobdiva.com/portal/?a=kvjdnwtsxgckrpsoozx5qc0oueybw1005779v7x6soig8eyqqmzaubfdl9tcx21s&compid=0&jobid=33140987#/jobs/33140987) | Artech | Boston, MA | 2026-09-24 |
| [Software Engineer - I](https://www2.jobdiva.com/portal/?a=fyjdnwkqny26xqof9rceu6y6gam6750308agqi8uui1cmk3v9j6duy26aoewnusi&compid=0&jobid=29353419#/jobs/29353419) | Net2Source | Austin, TX | 2026-09-24 |
| [Client Fulfillment Coordinator](https://pinnaclegroup.wd1.myworkdayjobs.com/en-US/PinnacleGroup/job/Headquarters/Client-Fulfillment-Coordinator_JR1262) | Pinnacle Group | Headquarters | 2026-09-24 |
| [DATA ENGINEER](https://www.harnham.com/job/eb8cdd1a-d1d1-4f13-3bd8-08d5dc096ea6-data-engineer-miami-florida/) | Harnham | Miami, Florida | 2026-09-24 |
| [SQL Developer](https://cgi.njoyn.com/CORP/xweb/xweb.asp?NTKN=c&clid=21001&Page=JobDetails&Jobid=J0926-1963&BRID=1335655&lang=1) | Njoyn (CGI) | Fairfax, Lafayette, United States | 2026-09-24 |
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
