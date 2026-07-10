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
### 🆕 16 new roles this update · 5913 tracked total · updated `2026-07-10T03:54:41+00:00`

| Firm | New roles |
| --- | ---: |
| Cynet Systems | 12 |
| Apex Systems | 1 |
| Robert Half | 1 |
| ProFocus | 1 |
| Njoyn (CGI) | 1 |

| Role | Firm | Location | Found |
| --- | --- | --- | --- |
| [Network Security Engineer 2](https://www.apexsystems.com/job/3041286_usa/network-security-engineer-2) | Apex Systems | St. Louis, MO | 2026-07-10 |
| [Aws Cloud Architect](https://www.roberthalf.com/us/en/job/doral-fl/aws-cloud-architect/01020-9504359609-usen) | Robert Half | Miami, 01020 | 2026-07-10 |
| [Platform Engineer](https://www.profocustechnology.com/echojobs/platform-engineer-3563/) | ProFocus | — | 2026-07-10 |
| [React Native Developer](https://candidateportal.ceipal.com/job-details/VgQ04U2dcv_LciYP5QnydoutBNKtSTii8CoPg039QXk) | Cynet Systems | Missouri | 2026-07-10 |
| [Full Stack Software Engineer/Machine Learning Engineer](https://candidateportal.ceipal.com/job-details/OvmYw7NfXTAqbEZx8599uvIcjVhRGopKtEcMagpYHSo) | Cynet Systems | New York | 2026-07-10 |
| [Devops Engineer](https://candidateportal.ceipal.com/job-details/vmWFyWX42CQVq2AgzkpnG1ZC2G39OLGNIvIFNmzmSQ4) | Cynet Systems | Texas | 2026-07-10 |
| [Software Development Engineer](https://candidateportal.ceipal.com/job-details/V5NlQ6LTq9sgBSY-qRiJ71dF4E9HlTJKbbNpZ1rJKPk) | Cynet Systems | California | 2026-07-10 |
| [Data Automation and Analytics Developer](https://candidateportal.ceipal.com/job-details/o9feUVeaxh-y0PT8avdiT01gRAZtC6iu9uj9moL5vgQ) | Cynet Systems | California | 2026-07-10 |
| [Azure Cloud Architect](https://candidateportal.ceipal.com/job-details/BZfAsaIANT0Q05v3YFLXE17_me9yOSb1OwNhh7eFXdc) | Cynet Systems | Texas | 2026-07-10 |
| [OpenShift/Cloud Engineer](https://candidateportal.ceipal.com/job-details/nbp25lOl6rOK2KWi_k5IXJpDsiMLcgJZtTue6oi875g) | Cynet Systems | Texas | 2026-07-10 |
| [DevOps Tools Administrator](https://candidateportal.ceipal.com/job-details/rG93vg9v1GtPmn3Xv7c3X_3OxLiALOAwOOEpEwa43_w) | Cynet Systems | Texas | 2026-07-10 |
| [ServiceNow SecOps Developer](https://candidateportal.ceipal.com/job-details/AJ5t5VjaK37U4mddc2C7SnZesRYsvPkgs8EKfVD3N9A) | Cynet Systems | California | 2026-07-10 |
| [AWS Cloud Engineer](https://candidateportal.ceipal.com/job-details/RyFA0pQKVWjNdJGpoqLrgiPasW17tFSuqPiJWxBFE1o) | Cynet Systems | New Jersey | 2026-07-10 |
| [DevOps Architect](https://candidateportal.ceipal.com/job-details/85Fl4-I-7LV3AUVEtbJCWUL8CofNazqgICbQ3Yx18Fo) | Cynet Systems | Texas | 2026-07-10 |
| [Full Stack Developer (Microsoft Visual Studio/.Net & SQL)](https://candidateportal.ceipal.com/job-details/zfke7ybU_Bq_TysPArXLF14fyrQtZnveqVrL26OgGCU) | Cynet Systems | Florida | 2026-07-10 |
| [AWS DevOps Engineer](https://cgi.njoyn.com/CORP/xweb/xweb.asp?NTKN=c&clid=21001&Page=JobDetails&Jobid=J0726-0775&BRID=1315377&lang=1) | Njoyn (CGI) | Raleigh, United States | 2026-07-10 |
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
