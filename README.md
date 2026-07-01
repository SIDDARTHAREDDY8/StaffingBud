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
### 🆕 16 new roles this update · 3833 tracked total · updated `2026-07-01T10:34:46+00:00`

| Firm | New roles |
| --- | ---: |
| Cynet Systems | 14 |
| TEKsystems | 2 |

| Role | Firm | Location | Found |
| --- | --- | --- | --- |
| [Individual Product Enrollment Specialist](https://careers.teksystems.com/us/en/job/JP-006127105/Individual-Product-Enrollment-Specialist) | TEKsystems | Virginia Beach, Virginia | 2026-07-01 |
| [Devops Engineer](https://careers.teksystems.com/us/en/job/JP-006127067/Devops-Engineer) | TEKsystems | Charlotte, North Carolina | 2026-07-01 |
| [Director - Forward Deployed Engineering](https://candidateportal.ceipal.com/job-details/NYfU_lPWq5BkXH_pOBzQke8ACJAIADVZLAwxNoMwf8o) | Cynet Systems | California | 2026-07-01 |
| [Conversational AI Data Analyst – Python](https://candidateportal.ceipal.com/job-details/M_Q1BLXW6N-ibszdMhaKw7Hf8kf95E-03N6doNWEJkE) | Cynet Systems | Texas | 2026-07-01 |
| [Java Developer](https://candidateportal.ceipal.com/job-details/-txPWatf3euSYI7nphYPUsOvk5YoZ1ovP23pAZV1Mqo) | Cynet Systems | Texas | 2026-07-01 |
| [Data Analytics & Observability/ Site Reliability Engineer](https://candidateportal.ceipal.com/job-details/UImmTTh2T1GkbXgxmDu2yiqxJC5ey35OHNGpkXqp6Yc) | Cynet Systems | North Carolina | 2026-07-01 |
| [Java Technical Architect](https://candidateportal.ceipal.com/job-details/dxJ6rOxWdoHK8jCdr2tTZ3BGFBK5ub22lOECvKdPelY) | Cynet Systems | Texas | 2026-07-01 |
| [AWS Lead Developer](https://candidateportal.ceipal.com/job-details/BMGf5jYaNm1-tCzQUbaGdWr4c8EbXcw4xm0-J91_oGA) | Cynet Systems | Texas | 2026-07-01 |
| [API Developer with AWS experience](https://candidateportal.ceipal.com/job-details/4HXWEVkKMfh6MZbMVQaQpse7Ct_FRf7hW4ut6yxFhgM) | Cynet Systems | Texas | 2026-07-01 |
| [Network Security DevOps Engineer](https://candidateportal.ceipal.com/job-details/54NVyuxT3r_TGmBDPq22kkRtJY1r9Ui6YS-MwkQW48Y) | Cynet Systems | Texas | 2026-07-01 |
| [Microservices Developers](https://candidateportal.ceipal.com/job-details/IrSs6stXTxte36uhauCgZN0iTgNb3rhaIxV7CnDsG28) | Cynet Systems | Pennsylvania | 2026-07-01 |
| [Android Developer [Triage Engineering]](https://candidateportal.ceipal.com/job-details/_Ch4WnGLvgNmzZfAA4Dh0tkuSjL5RCGrC-ZJ4VYkwCM) | Cynet Systems | California | 2026-07-01 |
| [Senior Cloud AI Architect](https://candidateportal.ceipal.com/job-details/pm3gsCnUHmRk-bO9if0wQPoBigf89Adh0G3d53XjHWA) | Cynet Systems | Georgia | 2026-07-01 |
| [Java Developer with AWS](https://candidateportal.ceipal.com/job-details/p4H7CoOFDgIRoBZHjbYq0k6BOX_AKjnc36dZ8St9WOU) | Cynet Systems | Texas | 2026-07-01 |
| [IOS Developer with Android Exp](https://candidateportal.ceipal.com/job-details/sOBPOFsCrRUo6eI3_74sUjDLT5DvZ_q6JF3pzeeyVgE) | Cynet Systems | New Jersey | 2026-07-01 |
| [Lead Mainframe Developer](https://candidateportal.ceipal.com/job-details/sC6gwXp_v4FIrUcPXFiVEG0VpVvxwnuAeChdnTz3ITc) | Cynet Systems | New Jersey | 2026-07-01 |
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
