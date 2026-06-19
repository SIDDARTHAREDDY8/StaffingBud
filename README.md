# StaffingBuddy

Scrapes the **career pages of staffing firms & IT vendors** (TEKsystems, Insight Global,
Kforce, Belcan, Agility, …) for **contract / contract-to-hire IT roles** —
software engineers, full-stack & web developers, data/ML/AI, cloud/DevOps, QA, and all
other IT positions. It reads each firm's own job-search page/API directly.

Inspired by [JobsBuddy](https://github.com/SIDDARTHAREDDY8/JobsBuddy), but pointed at
staffing vendors (high contract-role volume) instead of direct employers.

**The list below is a feed of *newly found* roles** — each job is posted once, the run it's
first discovered, then never repeated. Refreshes every 3 hours via GitHub Actions. The full
browsable archive lives in [`site/index.html`](site/index.html) and [`data/jobs.json`](data/jobs.json).

## Live Jobs

<!-- JOBS:START -->
### 🟢 No new roles since last update · 602 tracked total · updated `2026-06-19T18:42:14+00:00`
<!-- JOBS:END -->

## How it works

```
config/firms.yaml   →  one entry per firm (URL + how to read its job cards)
scraper/engine.py   →  Playwright renders the page, reads jobs via CSS selectors
scraper/filters.py  →  keep data/ML/AI titles, US/Cincinnati/remote locations
scraper/store.py    →  dedupe + first-seen tracking into data/jobs.json
build_site.py       →  render data/jobs.json into a static site/index.html
build_readme.py     →  inject the job list into this README (between JOBS markers)
.github/workflows   →  run every 3 hours, commit fresh jobs + README
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
