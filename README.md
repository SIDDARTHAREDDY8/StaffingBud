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
### 🆕 20 new roles this update · 4274 tracked total · updated `2026-11-12T17:33:20+00:00`

| Firm | New roles |
| --- | ---: |
| Kforce | 5 |
| TEKsystems | 3 |
| Robert Half | 3 |
| Goodwin Recruiting | 3 |
| Apex Systems | 1 |
| CornerStone TTS | 1 |
| CRG | 1 |
| Motion Recruitment | 1 |
| ASK Consulting | 1 |
| Compunnel | 1 |

| Role | Firm | Location | Found |
| --- | --- | --- | --- |
| [Data Analyst](http://www.kforce.com/Jobs/1696~AQG~2194148T1~99/) | Kforce | Durham, NC | 2026-11-12 |
| [Data Analyst](http://www.kforce.com/Jobs/1696~WQG~2194126T1~99/) | Kforce | Foster City, CA | 2026-11-12 |
| [Data Scientist](http://www.kforce.com/Jobs/1696~AQG~2186181P1~99/) | Kforce | Mediacom Park, NY | 2026-11-12 |
| [Data Platform Engineer](http://www.kforce.com/Jobs/1696~AQG~2193012P1~99/) | Kforce | Conshohocken, PA | 2026-11-12 |
| [Business Data Analyst IV](http://www.kforce.com/Jobs/1696~WQG~2194156T1~99/) | Kforce | Mountain View, CA | 2026-11-12 |
| [Programmer Analyst-Rhapsody & HL7-100% Remote](https://careers.teksystems.com/us/en/job/JP-006414588/Programmer-Analyst-Rhapsody-HL7-100-Remote) | TEKsystems | Boise, Idaho | 2026-11-12 |
| [Lead Developer](https://careers.teksystems.com/us/en/job/JP-006416747/Lead-Developer) | TEKsystems | Las Vegas, Nevada | 2026-11-12 |
| [Report Developer / Business Intelligence Developer](https://careers.teksystems.com/us/en/job/JP-006416907/Report-Developer-Business-Intelligence-Developer) | TEKsystems | San Diego, California | 2026-11-12 |
| [Senior Java API Engineer](https://www.apexsystems.com/job/3058157_usa/senior-java-api-engineer) | Apex Systems | Raleigh, NC | 2026-11-12 |
| [Senior Cloud Security Engineer](https://www.roberthalf.com/us/en/job/los-angeles-ca/senior-cloud-security-engineer/00320-0013509833-usen) | Robert Half | Los Angeles, 00320 | 2026-11-12 |
| [Senior Software Engineer](https://www.roberthalf.com/us/en/job/jacksonville-fl/senior-software-engineer/01120-9504425777-usen) | Robert Half | Jacksonville, 01120 | 2026-11-12 |
| [Cyber Security Engineer](https://www.roberthalf.com/us/en/job/huntersville-nc/cyber-security-engineer/03200-0013505146-usen) | Robert Half | Huntersville, 03200 | 2026-11-12 |
| [Principal Data Engineer](https://jobs.cornerstonetechtalent.com/jb/Principal-Data-Engineer-Jobs-in-/14409939) | CornerStone TTS | — | 2026-11-12 |
| [Senior Data Engineer](https://jobs.getcrg.com/jobs/16858) | CRG | Salisbury, North Carolina | 2026-11-12 |
| [Principal Open Source Developer - TypeScript/Node/Angular/React/.NET](https://motionrecruitment.com/tech-jobs/boston/direct-hire/principal-open-source-developer-typescript-node-angular-react-dot-net/894788) | Motion Recruitment | Boston, MA | 2026-11-12 |
| [Full-Stack Web Application Developer (.Net)](https://careers.curately.ai/careers/jobs/askconsulting/apply-jobs/133284/Full-Stack Web Application Developer (.Net)) | ASK Consulting | — | 2026-11-12 |
| [Lead Software Engineer](https://jobs.compunnel.com/jobs/6172894) | Compunnel | Issaquah, Washington, United States | 2026-11-12 |
| [Data Engineer](https://www.goodwinrecruiting.com/job/a0wr7000003jpatmaw-data-engineer-atlanta-georgia) | Goodwin Recruiting | — | 2026-11-12 |
| [Software Engineer (Mobile Focus)](https://www.goodwinrecruiting.com/job/a0wr7000003jpxfma4-software-engineer-mobile-focus-atlanta-georgia) | Goodwin Recruiting | — | 2026-11-12 |
| [Software Engineer (Full Stack, React & TypeScript)](https://www.goodwinrecruiting.com/job/a0wr7000003jpu1mao-software-engineer-full-stack-react-typescript-atlanta-georgia) | Goodwin Recruiting | — | 2026-11-12 |
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
