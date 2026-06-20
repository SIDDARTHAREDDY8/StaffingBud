"""
Scraper engine. One engine, two modes:

  - dom : Playwright renders the page, reads job cards via CSS selectors.
  - api : plain HTTP GET against the JSON endpoint the page calls behind the scenes.

Both return a list of normalized job dicts:
    { "firm", "title", "location", "url", "posted" }
"""
from __future__ import annotations

import re
from urllib.parse import urljoin


def _clean(text: str | None) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def scrape_dom(firm: dict, page) -> list[dict]:
    """Render `firm['search_url']` and pull job cards via CSS selectors."""
    sel = firm["selectors"]
    url = firm["search_url"]
    jobs: list[dict] = []

    page.goto(url, wait_until="networkidle", timeout=45_000)

    # Give lazy/JS lists a beat, then try to surface every card.
    try:
        page.wait_for_selector(sel["card"], timeout=15_000)
    except Exception:
        # Some lists only render cards after the user scrolls. Nudge and retry once.
        for _ in range(4):
            page.mouse.wheel(0, 15_000)
            page.wait_for_timeout(1_500)
        if not page.query_selector_all(sel["card"]):
            return jobs  # genuinely nothing — selectors likely need calibration

    # Some SPAs (Phenom/Aurelia) render the card shell first and fill in
    # location/details a beat later — let it settle before we read.
    page.wait_for_timeout(2_500)

    # Many job lists lazy-load on scroll (Phenom, etc.). Scroll until the card
    # count stops growing so we capture the full first page, not just the top few.
    prev = -1
    for _ in range(firm.get("scroll_passes", 8)):
        count = len(page.query_selector_all(sel["card"]))
        if count == prev:
            break
        prev = count
        page.mouse.wheel(0, 20_000)
        page.wait_for_timeout(1_200)

    cards = page.query_selector_all(sel["card"])
    for card in cards:
        title_el = card.query_selector(sel["title"])
        loc_el = card.query_selector(sel.get("location", "")) if sel.get("location") else None
        link_el = card.query_selector(sel.get("link", "a"))

        title = _clean(title_el.inner_text() if title_el else None)
        if not title:
            continue
        location = _clean(loc_el.inner_text() if loc_el else "")
        # Some cards pack location into a wider field like "Austin, TX | Perm | $120k".
        # location_split keeps only the first segment.
        split = firm.get("location_split")
        if split and location:
            location = _clean(location.split(split)[0])
        href = link_el.get_attribute("href") if link_el else None
        job_url = urljoin(url, href) if href else url

        jobs.append({
            "firm": firm["name"],
            "title": title,
            "location": location,
            "url": job_url,
            "posted": "",
        })
    return jobs


def scrape_api(firm: dict, http) -> list[dict]:
    """Call a JSON endpoint and map fields via a small path spec in firm['api'].

    Supports GET (params) and POST (json_body). Many staffing firms back their
    job search with a search service (Azure Search, Algolia, etc.) that takes a
    POST with a JSON query body — set `method: POST` and `json_body:` in config.
    """
    api = firm["api"]
    # Optional pagination: walk an offset param across pages until a short page.
    #   paginate: { in: json_body|params, param: from|skip, size: 100, max_pages: 5 }
    pg = api.get("paginate")
    if not pg:
        return _fetch_page(firm, http, api)

    size = pg.get("size", 50)
    jobs: list[dict] = []
    for page in range(pg.get("max_pages", 5)):
        offset = page * size
        page_jobs = _fetch_page(firm, http, api, _offset(pg, offset))
        jobs.extend(page_jobs)
        if len(page_jobs) < size:
            break  # last page reached
    return jobs


def _offset(pg: dict, value: int) -> dict:
    """Build an override dict that injects the offset into json_body or params."""
    return {"where": pg.get("in", "params"), "param": pg["param"], "value": value}


def _fetch_page(firm: dict, http, api: dict, override: dict | None = None) -> list[dict]:
    method = api.get("method", "GET").upper()
    body = dict(api.get("json_body") or {})
    params = dict(api.get("params") or {})
    if override:
        if override["where"] == "json_body":
            body[override["param"]] = override["value"]
        else:
            params[override["param"]] = override["value"]

    if method == "POST":
        resp = http.post(api["url"], json=body or None, params=params or None,
                         headers=api.get("headers"), timeout=30)
    else:
        resp = http.get(api["url"], params=params or None, headers=api.get("headers"), timeout=30)
    resp.raise_for_status()
    data = resp.json()

    node = data
    for key in api["list_path"].split("."):
        if key:
            node = node.get(key, []) if isinstance(node, dict) else []

    fields = api["fields"]
    jobs: list[dict] = []
    for item in node:
        title = _clean(_dig(item, fields["title"]))
        if not title:
            continue
        url = _dig(item, fields["url"]) or firm.get("search_url", "")
        if url and api.get("url_prefix") and not str(url).startswith("http"):
            url = api["url_prefix"].rstrip("/") + "/" + str(url).lstrip("/")
        url = _apply_url_transforms(str(url), item, api)
        jobs.append({
            "firm": firm["name"],
            "title": title,
            "location": _location(item, fields.get("location", "")),
            "url": url,
            "posted": _clean(str(_dig(item, fields.get("posted", "")))),
        })
    return jobs


def scrape_api_html(firm: dict, http) -> list[dict]:
    """For endpoints that return rendered HTML inside a JSON field (e.g. WordPress
    'WP Job Manager' jm-ajax/get_listings returns {found_jobs, html}). We fetch the
    JSON, pull the html field, and parse job cards with CSS selectors via BeautifulSoup.
    """
    api = firm["api"]
    pages = api.get("pages", 1)
    jobs: list[dict] = []
    for page in range(1, pages + 1):
        form = dict(api.get("form") or {})
        if pages > 1:
            form[api.get("page_param", "page")] = page
        if api.get("method", "POST").upper() == "POST":
            resp = http.post(api["url"], data=form or None, json=api.get("json_body"),
                             headers=api.get("headers"), timeout=30)
        else:
            resp = http.get(api["url"], params=api.get("params"), headers=api.get("headers"), timeout=30)
        resp.raise_for_status()
        html = resp.json().get(api.get("html_field", "html"), "")
        page_jobs = _parse_cards(html, firm)
        jobs.extend(page_jobs)
        if not page_jobs:
            break
    return jobs


def scrape_html(firm: dict, http) -> list[dict]:
    """Fetch server-rendered HTML page(s) directly (no browser) and parse job cards
    with CSS selectors. Pairs with the curl_cffi client to read sites that block
    headless browsers (Cloudflare, Radware/perfdrive) but serve plain HTTP clients.

    firm['url'] (single) or firm['urls'] (list, e.g. several search-term queries)
    — results from all urls are merged and de-duplicated by job URL.
    """
    h = firm.get("http", {})
    urls = firm.get("urls") or [firm["url"]]
    seen, jobs = set(), []
    for u in urls:
        try:
            resp = http.get(u, params=h.get("params"), headers=h.get("headers"), timeout=30)
            resp.raise_for_status()
        except Exception:
            continue
        for job in _parse_cards(resp.text, firm):
            if job["url"] in seen:
                continue
            seen.add(job["url"])
            jobs.append(job)
    return jobs


def _parse_cards(html: str, firm: dict) -> list[dict]:
    """Shared CSS-selector card parser for api_html / html modes.

    sel.link may be omitted — then the card's own href is used (when the card is
    an <a>). url_prefix (firm-level or under api/http) resolves relative hrefs.
    """
    from bs4 import BeautifulSoup

    sel = firm["selectors"]
    prefix = (firm.get("url_prefix")
              or (firm.get("api") or {}).get("url_prefix")
              or (firm.get("http") or {}).get("url_prefix"))
    soup = BeautifulSoup(html, "html.parser")
    jobs: list[dict] = []
    for card in soup.select(sel["card"]):
        title_el = card.select_one(sel["title"]) if sel.get("title") else None
        title = _clean(title_el.get_text() if title_el else card.get_text())
        if not title:
            continue
        link_el = card.select_one(sel["link"]) if sel.get("link") else None
        href = (link_el.get("href") if link_el else None)
        if not href and card.name == "a":
            href = card.get("href")
        if sel.get("require_link") and not href:
            continue
        url = href or firm.get("search_url", "")
        if href and prefix and not str(href).startswith("http"):
            url = prefix.rstrip("/") + "/" + str(href).lstrip("/")
        # location: a single selector, or a list of selectors joined (e.g. city+state)
        loc_spec = sel.get("location")
        if isinstance(loc_spec, list):
            parts = [card.select_one(s) for s in loc_spec]
            location = _clean(", ".join(p.get_text(strip=True) for p in parts if p))
        else:
            loc_el = card.select_one(loc_spec) if loc_spec else None
            location = _clean(loc_el.get_text()) if loc_el else ""
        split = firm.get("location_split")
        if split and location:
            location = _clean(location.split(split)[0])
        posted_el = card.select_one(sel["posted"]) if sel.get("posted") else None
        jobs.append({
            "firm": firm["name"], "title": title, "location": location,
            "url": url, "posted": _clean(posted_el.get_text()) if posted_el else "",
        })
    return jobs


def scrape_sitemap(firm: dict, http) -> list[dict]:
    """FREE bypass for bot-walled sites (Cloudflare etc.): their XML sitemap is
    served to search engines, so we read it directly — no browser, no Apify.

    Config (firm['sitemap']):
      url:      sitemap URL (may be a <sitemapindex>; we recurse one level)
      job_match: substring a URL must contain to count as a job (default '/job')
      index_match: (optional) only recurse child sitemaps whose URL contains this
      max: cap on job URLs to parse (default 3000)
    Title is derived from the URL slug; location isn't in sitemaps (left blank).
    """
    import gzip
    import re as _re

    sm = firm["sitemap"]
    job_match = sm.get("job_match", "/job")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
               "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"}

    def fetch(url: str) -> str:
        r = http.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        if url.endswith(".gz"):
            return gzip.decompress(r.content).decode("utf-8", "ignore")
        return r.text

    body = fetch(sm["url"])
    # entries: list of (loc, lastmod)
    entries: list[tuple[str, str]] = []
    if "<sitemapindex" in body:
        children = _re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", body)
        if sm.get("index_match"):
            children = [c for c in children if sm["index_match"] in c]
        for child in children[: sm.get("max_children", 20)]:
            try:
                cbody = fetch(child)
            except Exception:
                continue
            entries += _re.findall(r"<loc>\s*([^<\s]+)\s*</loc>(?:\s*<lastmod>\s*([^<\s]+))?", cbody)
    else:
        entries = _re.findall(r"<loc>\s*([^<\s]+)\s*</loc>(?:\s*<lastmod>\s*([^<\s]+))?", body)

    # Optional recency filter — drop entries whose <lastmod> is older than N days
    # (sitemaps can list expired jobs; recent lastmod is a freshness proxy).
    cutoff = None
    if sm.get("max_age_days"):
        from datetime import datetime, timedelta, timezone
        cutoff = datetime.now(timezone.utc) - timedelta(days=sm["max_age_days"])

    jobs: list[dict] = []
    seen = set()
    for loc, lastmod in entries:
        if job_match not in loc or loc in seen:
            continue
        if cutoff and lastmod:
            try:
                from datetime import datetime
                if datetime.fromisoformat(lastmod.replace("Z", "+00:00")) < cutoff:
                    continue
            except Exception:
                pass
        seen.add(loc)
        title = _title_from_url(loc)
        if not title:
            continue
        jobs.append({
            "firm": firm["name"],
            "title": title,
            "location": "",
            "url": loc,
            # some sitemaps stamp every entry with today's <lastmod> (useless as a
            # post date) — ignore_lastmod leaves it empty so enrichment fills the real one
            "posted": "" if sm.get("ignore_lastmod") else (lastmod or "")[:10],
        })
        if len(jobs) >= sm.get("max", 3000):
            break
    return jobs


def _title_from_url(url: str) -> str:
    """Derive a job title from a URL slug. Picks the last path segment that's
    word-like (more letters than digits), so it works whether the title is the
    final segment (Apex) or sits before a numeric id segment (Robert Half)."""
    import re as _re
    segs = [s for s in url.rstrip("/").split("/") if s]
    for seg in reversed(segs):
        letters = sum(c.isalpha() for c in seg)
        digits = sum(c.isdigit() for c in seg)
        if letters >= 4 and letters > digits:
            return _clean(_re.sub(r"[-_]+", " ", seg)).title()
    return _clean(_re.sub(r"[-_]+", " ", segs[-1])).title() if segs else ""


def scrape_jobdiva(firm: dict, http=None) -> list[dict]:
    """Generic adapter for JobDiva candidate-portal staffing firms. Two-step:
    auth/a (Basic + a/compid/portalid headers) -> token, then POST searchjobsportal.
    Config: jobdiva:{a, compid, pages}. Find `a` token in the vendor's
    www2.jobdiva.com/portal/?a=... link, and compid in the same URL.
    """
    from curl_cffi import requests as _cf

    c = firm["jobdiva"]
    atok, compid = c["a"], str(c.get("compid", "1"))
    base = "https://ws.jobdiva.com/candPortal/rest"
    s = _cf.Session(impersonate="chrome120")
    s.headers.update({"Referer": "https://www2.jobdiva.com/"})
    try:
        auth = s.get(f"{base}/auth/a", timeout=25, headers={
            "Authorization": "Basic YXhlbG9uOmF4ZWxvbg==", "portalid": "1", "compid": compid, "a": atok}).json()
        token, pid = auth["token"], auth["portalID"]
    except Exception:
        return []

    def jd_date(v):
        try:
            from datetime import datetime, timezone
            return datetime.fromtimestamp(int(v) / 1000, timezone.utc).date().isoformat()
        except Exception:
            return ""

    per = 50
    jobs: list[dict] = []
    for page in range(c.get("pages", 2)):
        frm, to = page * per + 1, (page + 1) * per
        body = {"city": "", "country": "", "from": str(frm), "to": str(to), "keywords": "",
                "portalID": str(pid), "unit": "mi", "zipcode": "", "jobCategories": "",
                "jobDivisions": "", "jobTypes": "", "miles": "", "onsiteFlex": "",
                "qualifications": "", "states": ""}
        try:
            data = s.post(f"{base}/job/searchjobsportal", timeout=25,
                          headers={"Content-Type": "application/x-www-form-urlencoded",
                                   "token": token, "a": atok, "portalid": str(pid)},
                          data=body).json().get("data", [])
        except Exception:
            break
        if not data:
            break
        for d in data:
            title = _clean(d.get("title", ""))
            if not title:
                continue
            loc = d.get("mainLocation") or d.get("location") or ""
            if isinstance(loc, dict):
                loc = ", ".join(str(loc.get(k, "")) for k in ("city", "state", "country") if loc.get(k))
            elif isinstance(loc, list) and loc:
                loc = ", ".join(str(x.get("city", x) if isinstance(x, dict) else x) for x in loc[:1])
            jobs.append({
                "firm": firm["name"], "title": title, "location": _clean(str(loc)),
                # job id lives in the #fragment (which our identity strips), so also
                # put it in the query — keeps each job distinct and the link still works
                "url": f"https://www2.jobdiva.com/portal/?a={atok}&compid={compid}&jobid={d.get('id')}#/jobs/{d.get('id')}",
                "posted": jd_date(d.get("postDate")),
            })
    return jobs


def scrape_ceipal(firm: dict, http=None) -> list[dict]:
    """Generic adapter for Ceipal-powered staffing firms (huge in the C2C space).
    The embedded widget's job API checks an X-Referer-Host header and posts a
    multipart form; we replicate it. Parameterized by api_key + cp_id (found in the
    vendor page's data-ceipal-api-key / data-ceipal-career-portal-id attributes).
    """
    import re as _re
    import requests as _rq

    c = firm["ceipal"]
    apikey, cpid = c["apikey"], c["cp_id"]
    base = f"https://careerapi.ceipal.com/{apikey}/CareerPortalJobPostings/"
    headers = {"Referer": "https://jobsapi.ceipal.com/", "X-Requested-With": "XMLHttpRequest",
               "User-Agent": "Mozilla/5.0"}

    def ceipal_date(s: str) -> str:        # MM/DD/YY -> YYYY-MM-DD
        m = _re.match(r"(\d{1,2})/(\d{1,2})/(\d{2})", s or "")
        return f"20{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}" if m else (s or "")

    jobs: list[dict] = []
    for page in range(1, c.get("pages", 12) + 1):
        fields = {"from_chatbot": "0", "page": str(page), "api_key": apikey,
                  "method": "CareerPortalJobPostings", "cp_id": cpid, "from_career_portal": "1"}
        try:
            r = _rq.post(f"{base}?page={page}", headers=headers,
                         files={k: (None, v) for k, v in fields.items()}, timeout=30)
            results = r.json().get("results", [])
        except Exception:
            break
        if not results:
            break
        for d in results:
            title = _clean(d.get("position_title", ""))
            if not title:
                continue
            loc = [d.get("city", ""), d.get("state", "")]
            country = (d.get("country") or "").strip()
            if country and country.lower() not in ("us", "usa", "united states", "u.s.", "u.s"):
                loc.append(country)          # surface foreign country so US filter catches it
            jobs.append({
                "firm": firm["name"], "title": title,
                "location": _clean(", ".join(x for x in loc if x)),
                "url": d.get("campus_portal_job_details_url") or firm.get("search_url", ""),
                "posted": ceipal_date(d.get("created", "")),
            })
    return jobs


def scrape_apify_search(firm: dict, http, token: str) -> list[dict]:
    """Enumerate a firm's jobs via Apify's rag-web-browser in Google-search mode.

    Used for Cloudflare-walled firms (e.g. Apex): Google has already indexed past
    the wall, so a `site:firm.com/job <keywords>` query returns job pages cheaply.
    Needs an Apify API token (APIFY_TOKEN env var). Each search result becomes a job.
    """
    ap = firm["apify"]
    actor = ap["actor"]
    url = f"https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items?token={token}"
    payload = {
        "query": ap["query"],
        "maxResults": ap.get("max_results", 15),
        "outputFormats": ["markdown"],
    }
    resp = http.post(url, json=payload, timeout=120)
    resp.raise_for_status()
    items = resp.json()

    jobs: list[dict] = []
    for it in items:
        sr = it.get("searchResult") or {}
        title = _clean(sr.get("title") or it.get("metadata", {}).get("title") or "")
        link = sr.get("url") or it.get("metadata", {}).get("url") or ""
        if not title or not link:
            continue
        # Strip the firm-name suffix many titles carry: "Data Engineer | Everforth Apex"
        title = _clean(title.split("|")[0])
        jobs.append({
            "firm": firm["name"],
            "title": title,
            "location": "",   # not present in search snippets
            "url": link,
            "posted": "",
        })
    return jobs


def _location(item: dict, spec) -> str:
    """Location may be one path or a list of paths to join, e.g. ['City','State'].

    Each dug value may itself be a list (some APIs return City: ["Austin"]) —
    flatten those to their first element so we get 'Austin, TX' not "['Austin'], ['TX']".
    """
    paths = spec if isinstance(spec, list) else [spec]
    parts = []
    for p in paths:
        val = _dig(item, p)
        if isinstance(val, list):
            val = val[0] if val else ""
        val = str(val).strip()
        if val and val.lower() not in ("none", "null"):
            parts.append(val)
    return _clean(", ".join(parts))


def normalize_posted(s: str) -> str:
    """Convert relative posting strings to an ISO date so freshness sorts correctly.
    Workday gives 'Posted 30+ Days Ago' / 'Posted 7 Days Ago' / 'Posted Today' —
    those don't parse as dates, so without this they'd wrongly fall back to NEW.
    """
    if not s:
        return s
    import re as _re
    from datetime import datetime, timedelta, timezone
    low = s.lower()
    today = datetime.now(timezone.utc).date()
    if "today" in low or "just posted" in low:
        return today.isoformat()
    if "yesterday" in low:
        return (today - timedelta(days=1)).isoformat()
    for unit, days in (("day", 1), ("week", 7), ("month", 30), ("year", 365)):
        m = _re.search(r"(\d+)\+?\s*" + unit, low)
        if m:
            return (today - timedelta(days=int(m.group(1)) * days)).isoformat()
    return s


def extract_posted_date(html: str) -> str:
    """Pull a posting date from a job detail page. Handles schema.org JSON-LD
    (`"datePosted":`), microdata (`itemprop="datePosted">Mar 03, 2026<`, used by
    Insight Global), and visible 'Post Date / Posted: Mon DD, YYYY' labels.
    """
    import re as _re
    for pat in (
        r'"datePosted"\s*:\s*"([0-9][0-9T:.\-+ Z]{7,39})"',
        r'itemprop=["\']datePosted["\'][^>]*>\s*([^<]{4,40}?)\s*<',
        r'datePosted["\']?\s*[:=]\s*["\']?([0-9]{4}-[0-9]{1,2}-[0-9]{1,2})',
        r'[Pp]ost(?:ed)?\s*Date[^A-Za-z0-9]{0,18}([A-Z][a-z]{2,8}\.?\s+\d{1,2},?\s+\d{4})',
        r'[Pp]osted[:\s]+([A-Z][a-z]{2,8}\.?\s+\d{1,2},?\s+\d{4})',
    ):
        m = _re.search(pat, html)
        if m:
            val = m.group(1).strip()
            if _re.search(r'\d{4}', val):   # sanity: must contain a 4-digit year
                return val
    return ""


def extract_location(html: str) -> str:
    """Pull 'City, ST' from a job detail page (schema.org address or microdata)."""
    import re as _re
    city = _re.search(r'"addressLocality"\s*:\s*"([^"]{2,40})"', html)
    region = _re.search(r'"addressRegion"\s*:\s*"([^"]{2,40})"', html)
    parts = [m.group(1).strip() for m in (city, region) if m]
    if parts:
        return ", ".join(parts)
    m = _re.search(r'itemprop=["\']addressLocality["\'][^>]*>\s*([^<]{2,30}?)\s*<', html)
    return m.group(1).strip() if m else ""


def within_age(posted: str, max_days: int) -> bool:
    """True if `posted` parses to within max_days, or is missing/unparseable
    (don't drop what we can't date)."""
    if not posted or not max_days:
        return True
    import re as _re
    from datetime import datetime, timezone
    s = posted.strip().replace("Z", "+00:00")
    dt = None
    try:
        dt = datetime.fromisoformat(s)
    except Exception:
        for f in ("%Y-%m-%d", "%m/%d/%Y", "%b %d, %Y", "%B %d, %Y"):
            try:
                dt = datetime.strptime(posted.strip()[:20], f)
                break
            except Exception:
                pass
    if dt is None:
        return True
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - dt).days <= max_days


def enrich_posted_dates(jobs: list[dict], http, known: dict, job_id) -> int:
    """For firms that expose the posting date only on the detail page, set
    job['posted'] from that page. Reuses a previously-stored date (no fetch); only
    fetches when the date is genuinely missing — so it self-heals old date-less
    jobs once, then costs ~nothing. Returns count newly fetched.
    """
    n = 0
    for job in jobs:
        if job.get("posted"):
            continue
        prev = known.get(job_id(job))
        if prev and prev.get("posted"):
            job["posted"] = prev["posted"]   # already have it — don't refetch
            continue
        try:
            html = http.get(job["url"], timeout=20).text
        except Exception:
            continue
        dt = extract_posted_date(html)
        if dt:
            job["posted"] = dt[:10] if dt[:1].isdigit() else dt
            n += 1
        if not job.get("location"):           # also backfill location while here
            loc = extract_location(html)
            if loc:
                job["location"] = loc
    return n


def _apply_url_transforms(url: str, item: dict, api: dict) -> str:
    """Turn an apply URL into the job-description (JD) URL.

      url_regex_sub: {pattern, repl}  -> re.sub on the resolved url
                                         (Kforce: strip '/ApplyOnline...' -> JD)
      url_template:  "https://.../job/{jobId}/{slug:title}" built from item fields;
                     {slug:field} hyphenates the field (TEKsystems JD path).
    """
    import re
    sub = api.get("url_regex_sub")
    if sub:
        url = re.sub(sub["pattern"], sub.get("repl", ""), url)
    tmpl = api.get("url_template")
    if tmpl:
        def repl(m):
            key = m.group(1)
            if key.startswith("slug:"):
                val = str(_dig(item, key[5:]))
                return re.sub(r"[^A-Za-z0-9]+", "-", val).strip("-")
            return str(_dig(item, key))
        url = re.sub(r"\{([^}]+)\}", repl, tmpl)
    return url


def _dig(item: dict, path: str):
    """Dotted-path getter: 'a.b' -> item['a']['b']. Returns '' on miss."""
    if not path:
        return ""
    node = item
    for key in path.split("."):
        if isinstance(node, dict) and key in node:
            node = node[key]
        else:
            return ""
    return node
