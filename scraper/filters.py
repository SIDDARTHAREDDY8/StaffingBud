"""Keyword + location filtering for scraped jobs.

Goal: keep ALL IT / software / data roles, drop clearly non-IT roles (these
staffing firms also post warehouse, nursing, mechanical-engineering, sales, etc.).
"""
from __future__ import annotations

# A job is kept if its title matches ANY of these (broad IT allowlist).
# Ambiguous short tokens are space-padded so they match as words, not substrings.
KEYWORDS = [
    # software / general engineering
    "software", "developer", "engineer", "programmer", "sde", "swe",
    "full stack", "fullstack", "full-stack", "front end", "frontend", "front-end",
    "back end", "backend", "back-end", "web dev", "application dev", "applications dev",
    # languages / frameworks
    "java", "python", "javascript", "typescript", "react", "angular", "vue",
    "node", ".net", "c#", "c++", "golang", " go ", "ruby", "php", "scala",
    "kotlin", "swift", "rust", "perl",
    # mobile
    "mobile", "ios", "android",
    # cloud / infra / devops
    "devops", " sre", "site reliability", "cloud", "aws", "azure", "gcp",
    "kubernetes", "docker", "terraform", "linux", "infrastructure", "systems",
    "network", "sysadmin", "system admin", "platform", "site reliab",
    # data / ml / ai
    "data", "machine learning", " ml ", " ai ", "artificial intelligence",
    "analytics", "analyst", "scientist", "database", " sql", "etl", "snowflake",
    "spark", "hadoop", "tableau", "power bi", "dba",
    # qa / security
    " qa ", "sdet", "tester", "test engineer", "automation", "security",
    "cyber", "penetration",
    # roles / tech misc
    "architect", " it ", "information technology", "salesforce", "sap", "oracle",
    "servicenow", "sharepoint", "business analyst", "scrum master", "product owner",
    "product manager", "technical", "integration", " api ", " ui ", " ux",
    "helpdesk", "help desk", "support engineer", "support analyst", "technology",
    "programmer analyst", "web ", "blockchain",
]

# Drop these even if a keyword matched — clearly non-IT or staffing-internal roles.
EXCLUDE = [
    # staffing-firm internal / sales
    "sales", "account manager", "account executive", "recruiter",
    "business development", "talent acquisition", "staffing consultant",
    # security clearance (not viable for many candidates)
    "clearance", "secret", "ts/sci", "polygraph",
    # non-IT engineering disciplines
    "mechanical engineer", "civil engineer", "chemical engineer", "aerospace",
    "structural engineer", "process engineer", "manufacturing engineer",
    "field engineer", "sales engineer", "electrical engineer", "industrial engineer",
    "environmental engineer", "petroleum", "geotechnical",
    # clearly non-IT roles
    "nurse", " rn ", "clinical", "physician", "therapist", "pharmacy", "caregiver",
    "warehouse", "forklift", "driver", " cdl", "welder", "machinist", "assembler",
    "custodian", "janitor", "cashier", "bartender", "chef", "cook", "hvac",
    "plumber", "electrician", "mechanic", "laborer", "receptionist",
    "accountant", "bookkeeper", "attorney", "paralegal", "teacher", "phlebot",
    "machine operator", "production operator", "maintenance technician",
    # non-IT "analyst"/"engineer"/specialist roles that match broad keywords
    "financial analyst", "tax analyst", "accounting analyst", "credit analyst",
    "budget analyst", "research analyst", "marketing analyst", "supply chain analyst",
    "logistics", "procurement", "machining", " cnc", "project engineer",
    "manufacturing", "tax ", "payroll", "warehouse", "buyer", "merchandis",
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
