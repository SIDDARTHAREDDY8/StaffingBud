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
### 🆕 10 new roles this update · 5099 tracked total · updated `2026-11-07T00:53:37+00:00`

| Firm | New roles |
| --- | ---: |
| Kforce | 3 |
| Robert Half | 2 |
| Motion Recruitment | 2 |
| TEKsystems | 1 |
| Apex Systems | 1 |
| CornerStone TTS | 1 |

| Role | Firm | Location | Found |
| --- | --- | --- | --- |
| [Boston Preferred - Data Engineer](http://www.kforce.com/Jobs/1696~TVT~2193666T1~99/) | Kforce | Armonk, NY | 2026-11-07 |
| [FinTech Systems Architect / AI Lead](http://www.kforce.com/Jobs/1696~EQG~2192724P1~99/) | Kforce | Fort Lauderdale, FL | 2026-11-07 |
| [Principal AI Engineer](http://www.kforce.com/Jobs/1696~AQG~2187554T1~99/) | Kforce | Covington, KY | 2026-11-07 |
| [Embedded Software Engineer III - Tactical Communications & Waveform Systems](https://careers.teksystems.com/us/en/job/JP-006404439/Embedded-Software-Engineer-III-Tactical-Communications-Waveform-Systems) | TEKsystems | San Diego, California | 2026-11-07 |
| [API Developer](https://www.apexsystems.com/job/3058609_usa/api-developer) | Apex Systems | Atlanta, GA | 2026-11-07 |
| [Software Engineer](https://www.roberthalf.com/us/en/job/memphis-tn/software-engineer/03900-9504424237-usen) | Robert Half | Memphis, 03900 | 2026-11-07 |
| [Data Scientist B2C Consumer Trends](https://www.roberthalf.com/us/en/job/richmond-va/data-scientist-b2c-consumer-trends/04836-9504424154-usen) | Robert Half | Richmond, 04836 | 2026-11-07 |
| [Senior Healthcare Integration Developer - HL7/FHIR](https://jobs.cornerstonetechtalent.com/jb/Senior-Healthcare-Integration-Developer-HL7-FHIR-Jobs-in-Austin-Texas/14400021) | CornerStone TTS | Austin Texas | 2026-11-07 |
| [Programmer](https://motionrecruitment.com/tech-jobs/chanhassen/contract/programmer/894385) | Motion Recruitment | Chanhassen, Minnesota | 2026-11-07 |
| [Principal Cloud Architect // C#.NET // Boston](https://motionrecruitment.com/tech-jobs/boston/direct-hire/principal-cloud-architect-c-sharpdot-net-boston/894384) | Motion Recruitment | Boston, Massachusetts | 2026-11-07 |
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
