"""Keyword + location filtering for scraped jobs."""
from __future__ import annotations

# Roles you care about. A job is kept if its title matches ANY of these.
KEYWORDS = [
    "data", "machine learning", "ml ", "ai ", "artificial intelligence",
    "python", "data scien", "data engineer", "analytics", "analyst",
    "mlops", "nlp", "deep learning", "recommendation", "recsys",
    "llm", "genai", "data analyst", "etl", "snowflake", "spark",
]

# Drop obvious noise (senior leadership, sales, unrelated).
EXCLUDE = [
    "sales", "account manager", "account executive", "recruiter",
    "business development", "director", "vp ", "vice president",
    "intern", "clearance", "secret",
]


def matches_keywords(title: str) -> bool:
    t = f" {title.lower()} "
    if any(x in t for x in EXCLUDE):
        return False
    return any(k in t for k in KEYWORDS)


def matches_location(location: str, allowed: list[str]) -> bool:
    if not allowed:
        return True
    if not location:
        return True  # keep unknowns rather than silently dropping
    loc = location.lower()
    return any(a.lower() in loc for a in allowed)


def apply_filters(jobs: list[dict], firm: dict) -> list[dict]:
    allowed = firm.get("location_filter", [])
    out = []
    for j in jobs:
        if not matches_keywords(j["title"]):
            continue
        if not matches_location(j["location"], allowed):
            continue
        out.append(j)
    return out
