"""Keyword + location filtering for scraped jobs.

Focused scope: core SOFTWARE ENGINEERING + DATA + AI/ML roles (plus a couple of
niche titles like Member of Technical Staff / Forward Deployed Engineer).
NOT broad IT — we drop help desk, network/sysadmin, business analyst, project
manager, QA, functional ERP/CRM consultants, support, etc.
"""
from __future__ import annotations

# Keep a job only if its title matches ANY of these (focused allowlist).
# We avoid bare "engineer" (matches mechanical/network/sales) and use phrases instead.
KEYWORDS = [
    # software engineer / developer (all flavors)
    "software engineer", "software developer", "software development engineer",
    "sde", " swe", "developer", "programmer",
    "full stack", "fullstack", "full-stack", "full stack engineer",
    "front end", "frontend", "front-end", "back end", "backend", "back-end",
    "web developer", "web engineer", "mobile engineer", "mobile developer",
    "ios engineer", "ios developer", "android engineer", "android developer",
    "embedded engineer", "embedded software", "firmware engineer", "game developer",
    "application engineer", "applications engineer", "api engineer",
    # software-adjacent engineering (write code)
    "platform engineer", "cloud engineer", "devops engineer", "devops",
    "site reliability", "sre", "security engineer", "infrastructure engineer",
    "systems software", "distributed systems",
    # data
    "data engineer", "data scientist", "data science", "data analyst",
    "data analytics", "analytics engineer", "data architect", "database engineer",
    "big data", "etl developer", "etl engineer", "bi developer",
    # ai / ml
    "machine learning", " ml ", " mle", "ml engineer", "ai engineer", " ai ",
    "artificial intelligence", "deep learning", "nlp", "natural language",
    "llm", "genai", "generative ai", "computer vision", "applied scientist",
    "research scientist", "research engineer", "mlops", "ai/ml", "ml/ai",
    # architects (software/data/cloud only)
    "software architect", "data architect", "cloud architect", "solutions architect",
    "application architect", "technical architect",
    # niche titles the user called out
    "member of technical staff", "member of the technical staff", "technical staff",
    "forward deployed",
]

# Drop these even if a keyword matched — non-IT, broad-IT, or non-engineering.
EXCLUDE = [
    # staffing-internal / sales / clearance
    "sales", "account manager", "account executive", "recruiter",
    "business development", "talent acquisition", "staffing consultant",
    "clearance", "secret", "ts/sci", "polygraph",
    # broad IT / ops that aren't core SWE/data/ML
    "help desk", "helpdesk", "service desk", "desktop support", "desktop technician",
    "field service", "field technician", "technical support", "support technician",
    "support analyst", "support engineer", "production support", "application support",
    "network engineer", "network administrator", "network architect", "network analyst",
    "system administrator", "systems administrator", "sysadmin", "system admin",
    "infrastructure analyst", "noc ", "telecom", "voip", "datacenter technician",
    "data center technician",
    # non-engineering roles
    "business analyst", "business systems analyst", "systems analyst",
    "project manager", "program manager", "project coordinator", "project analyst",
    "scrum master", "product owner", "product manager", "release manager",
    "technical writer", "technical recruiter", "delivery manager", "engagement manager",
    # functional ERP/CRM/config (not coding)
    "sap ", "oracle apps", "oracle ebs", "peoplesoft", "workday consultant",
    "workday analyst", "servicenow admin", "sharepoint admin", "salesforce admin",
    "salesforce consultant", "functional consultant", "functional analyst", "erp ",
    # QA (user didn't ask for it)
    "quality assurance", " qa ", "qa engineer", "qa analyst", "test engineer",
    "tester", "manual test", "sdet",
    # DBA / admin
    "database administrator", "dba ", "sccm",
    # non-IT engineering disciplines
    "mechanical engineer", "civil engineer", "chemical engineer", "aerospace",
    "structural engineer", "process engineer", "manufacturing engineer",
    "field engineer", "sales engineer", "electrical engineer", "industrial engineer",
    "environmental engineer", "petroleum", "geotechnical", "project engineer",
    "design engineer", "machining", " cnc",
    # clearly non-IT roles
    "nurse", " rn ", "clinical", "physician", "therapist", "pharmacy", "caregiver",
    "warehouse", "forklift", "driver", " cdl", "welder", "machinist", "assembler",
    "custodian", "janitor", "cashier", "bartender", "chef", "cook", "hvac",
    "plumber", "electrician", "mechanic", "laborer", "receptionist",
    "accountant", "bookkeeper", "attorney", "paralegal", "teacher", "phlebot",
    "financial analyst", "tax analyst", "accounting analyst", "logistics",
    "procurement", "buyer", "merchandis", "payroll", "marketing",
]


def matches_keywords(title: str) -> bool:
    t = f" {title.lower()} "
    if any(x in t for x in EXCLUDE):
        return False
    return any(k in t for k in KEYWORDS)


# Drop clearly non-US locations (these staffing firms post global/offshore roles).
# Deny-list known foreign countries / Canadian provinces / offshore cities; keep US
# and ambiguous/empty locations. Add to this if a foreign city slips through.
NON_US = [
    # countries
    "canada", "india", "united kingdom", " uk", "england", "scotland", "wales",
    "ireland", "poland", "belgium", "netherlands", "germany", "france",
    "switzerland", "portugal", "spain", "italy", "mexico", "brazil", "colombia",
    "argentina", "philippines", "singapore", "australia", "china", "japan",
    "romania", "ukraine", "czech", "hungary", "austria", "sweden", "denmark",
    # canadian provinces (names + ", XX" codes — none overlap US state codes)
    "ontario", "quebec", "québec", "alberta", "british columbia", "manitoba",
    "saskatchewan", "nova scotia", "new brunswick", "newfoundland",
    ", on", ", qc", ", ab", ", bc", ", mb", ", sk", ", ns", ", nb", ", nl", ", pe",
    # canadian cities
    "toronto", "montreal", "montréal", "vancouver", "calgary", "ottawa", "halifax",
    "sherbrooke", "moncton", "winnipeg", "edmonton", "mississauga", "waterloo",
    # india cities
    "hyderabad", "chennai", "bangalore", "bengaluru", "mumbai", "pune", "delhi",
    "noida", "gurgaon", "gurugram", "kolkata", "ahmedabad", "coimbatore",
    "chandigarh", "trivandrum", "kochi", "indore", "jaipur",
    # europe / other offshore cities
    "london", "leeds", "manchester", "dublin", "lisbon", "porto", "wrocław",
    "wroclaw", "kraków", "krakow", "warsaw", "mechelen", "brussels", "geneva",
    "zurich", "amsterdam", "paris", "berlin", "munich", "madrid", "barcelona",
    "milan", "rome", "bucharest", "prague", "manila", "sydney", "melbourne",
    "flanders", "voivod",
]


def is_non_us(location: str) -> bool:
    if not location:
        return False  # unknown -> keep (firms here are US-focused)
    l = f" {location.lower()} "
    return any(tok in l for tok in NON_US)


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
        if is_non_us(j["location"]):          # US-only board: drop offshore roles
            continue
        if not matches_location(j["location"], allowed):
            continue
        out.append(j)
    return out
