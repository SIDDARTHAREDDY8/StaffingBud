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
### 🆕 18 new roles this update · 3247 tracked total · updated `2026-11-24T09:13:07+00:00`

| Firm | New roles |
| --- | ---: |
| Apex Systems | 6 |
| Compunnel | 5 |
| Robert Half | 4 |
| Beacon Hill | 2 |
| TEKsystems | 1 |

| Role | Firm | Location | Found |
| --- | --- | --- | --- |
| [Research Engineer \| AI Data & Agent Systems](https://careers.teksystems.com/us/en/job/JP-006440156/Research-Engineer-AI-Data-Agent-Systems) | TEKsystems | Redmond, Washington | 2026-11-24 |
| [Platform Engineer](https://www.apexsystems.com/job/3054748_usa/platform-engineer) | Apex Systems | Mission, KS | 2026-11-24 |
| [Data Engineer](https://www.apexsystems.com/job/3055815_usa/data-engineer) | Apex Systems | Eagan, MN | 2026-11-24 |
| [SaaS Security Engineer](https://www.apexsystems.com/job/3060277_usa/saas-security-engineer) | Apex Systems | Columbus, OH | 2026-11-24 |
| [Cybersecurity Engineer - BAS](https://www.apexsystems.com/job/3059931_usa/cybersecurity-engineer---bas) | Apex Systems | York, SC | 2026-11-24 |
| [Sr. Developer (AI)](https://www.apexsystems.com/job/3059598_usa/sr-developer-ai) | Apex Systems | Greenwood Village, CO | 2026-11-24 |
| [AI Data Scientist](https://www.apexsystems.com/job/3059840_usa/ai-data-scientist) | Apex Systems | Milwaukee, WI | 2026-11-24 |
| [Senior Cloud Security Engineer](https://www.roberthalf.com/us/en/job/los-angeles-ca/senior-cloud-security-engineer/00320-0013509833-usen) | Robert Half | Los Angeles, 00320 | 2026-11-24 |
| [Security Engineer](https://www.roberthalf.com/us/en/job/los-angeles-ca/security-engineer/00320-0013425689-usen) | Robert Half | Los Angeles, 00320 | 2026-11-24 |
| [Senior Infrastructure Engineer](https://www.roberthalf.com/us/en/job/santa-barbara-ca/senior-infrastructure-engineer/00320-0013419297-usen) | Robert Half | Santa Barbara, 00320 | 2026-11-24 |
| [Sr Software Engineer](https://www.roberthalf.com/us/en/job/los-angeles-ca/sr-software-engineer/00320-0013516451-usen) | Robert Half | Los Angeles, 00320 | 2026-11-24 |
| [Duck Creek Policy Developer](https://jobs.compunnel.com/jobs/6174013) | Compunnel | Dallas, Texas, United States | 2026-11-24 |
| [Software Architect](https://jobs.compunnel.com/jobs/6222085) | Compunnel | Aliso Viejo, California, United States | 2026-11-24 |
| [Senior Data Analyst](https://jobs.compunnel.com/jobs/6205647) | Compunnel | New York, New York, United States | 2026-11-24 |
| [Senior Data Analyst](https://jobs.compunnel.com/jobs/6174324) | Compunnel | Omaha, Nebraska, United States | 2026-11-24 |
| [Oracle PL/SQL Developer](https://jobs.compunnel.com/jobs/6174148) | Compunnel | Mount Laurel, New Jersey, United States | 2026-11-24 |
| [Infrastructure Engineer](https://bhsg.com/jobs/job/pbmad11232026_1795453223-infrastructure-engineer-green-bay-wisconsin/) | Beacon Hill | — | 2026-11-24 |
| [Senior Backend Software Developer, Applied AI & Data](https://bhsg.com/jobs/job/mke1476121aj_1795446451-senior-backend-software-developer-applied-ai-data-milwaukee-wisconsin/) | Beacon Hill | — | 2026-11-24 |
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
