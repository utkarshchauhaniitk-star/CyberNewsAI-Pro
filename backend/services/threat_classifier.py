import re
from typing import List, Tuple, Dict

# Regex for Common Vulnerabilities and Exposures (CVE) IDs
CVE_REGEX = re.compile(r"\bCVE-\d{4}-\d{4,7}\b", re.IGNORECASE)

# Category classification keyword rules
CATEGORY_KEYWORDS: Dict[str, List[str]] = {
    "Ransomware & Extortion": [
        "ransomware", "extortion", "encryptor", "decryptor", "ransom",
        "lockbit", "qilin", "blackcat", "alphv", "akira", "clop",
        "rhysida", "medusa", "play ransomware", "bianlian", "ransom note"
    ],
    "Vulnerabilities & Exploits": [
        "cve-", "vulnerability", "zero-day", "0-day", "exploit", "proof-of-concept",
        "rce", "remote code execution", "privilege escalation", "buffer overflow",
        "auth bypass", "unauthenticated", "security flaw", "patch tuesday", "cvss"
    ],
    "Data Breaches & Leaks": [
        "data breach", "breached", "leaked", "exfiltration", "stolen records",
        "database leak", "credentials exposed", "customer data", "dark web forum",
        "shinyhunters", "dumped online", "exposed database"
    ],
    "Nation-State & APT": [
        "nation-state", "apt", "advanced persistent threat", "espionage",
        "state-sponsored", "russia", "china", "iran", "north korea",
        "sandworm", "fancy bear", "cozy bear", "volt typhoon", "salt typhoon",
        "lazarus", "unc", "ta505"
    ],
    "Malware & Botnets": [
        "malware", "trojan", "infostealer", "botnet", "wiper", "rootkit",
        "spyware", "keylogger", "backdoor", "c2", "command-and-control",
        "redline", "lumma", "vidar", "mirai", "dropper", "loader"
    ],
    "Cloud & Infrastructure": [
        "cloud", "aws", "azure", "kubernetes", "docker", "s3 bucket",
        "misconfiguration", "gcp", "active directory", "identity",
        "scada", "plc", "industrial control", "ot/ics", "water plant", "power grid"
    ],
    "Defense & Advisories": [
        "cisa", "advisory", "nsa", "fbi", "best practices", "guidance",
        "mitigation", "framework", "nist", "patch now", "alert"
    ]
}

# Critical severity markers
CRITICAL_MARKERS = [
    "zero-day", "0-day", "actively exploited", "in the wild",
    "unauthenticated rce", "critical severity", "cvss 10", "cvss 9.",
    "emergency patch", "critical infrastructure", "remote code execution"
]

HIGH_MARKERS = [
    "ransomware", "privilege escalation", "authentication bypass",
    "data breach", "state-sponsored", "espionage", "exploit available",
    "proof-of-concept", "mass exploitation"
]

LOW_MARKERS = [
    "advisory", "best practice", "survey", "report", "opinion",
    "tips", "reminder", "patch tuesday scheduled"
]


def extract_cves(text: str) -> List[str]:
    """Extracts and normalizes unique CVE identifiers from text."""
    if not text:
        return []
    matches = CVE_REGEX.findall(text)
    # Deduplicate preserving order, uppercase
    cves = []
    seen = set()
    for m in matches:
        upper_cve = m.upper()
        if upper_cve not in seen:
            seen.add(upper_cve)
            cves.append(upper_cve)
    return cves


def classify_category(title: str, summary: str, source: str) -> str:
    """Classifies an article into a primary cybersecurity category based on keyword density."""
    text = f"{title} {summary}".lower()

    # Source-based hint
    if source.lower() == "cisa":
        if "ransomware" in text:
            return "Ransomware & Extortion"
        if "cve-" in text or "vulnerability" in text:
            return "Vulnerabilities & Exploits"
        return "Defense & Advisories"

    scores: Dict[str, int] = {}
    for cat, keywords in CATEGORY_KEYWORDS.items():
        score = 0
        for kw in keywords:
            # Title matches carry 3x weight
            if kw in title.lower():
                score += 3
            elif kw in text:
                score += 1
        if score > 0:
            scores[cat] = score

    if not scores:
        return "General Cyber"

    # Return category with highest score
    return max(scores.items(), key=lambda x: x[1])[0]


def determine_severity(title: str, summary: str, cves: List[str]) -> str:
    """Calculates threat severity: Critical, High, Medium, or Low."""
    text = f"{title} {summary}".lower()

    for marker in CRITICAL_MARKERS:
        if marker in text:
            return "Critical"

    # Multiple CVEs or presence of RCE keywords elevate to High
    if len(cves) >= 2:
        return "High"

    for marker in HIGH_MARKERS:
        if marker in text:
            return "High"

    for marker in LOW_MARKERS:
        if marker in text:
            return "Low"

    return "Medium"


def enrich_article_metadata(article: Dict) -> Dict:
    """Enriches a raw article with category, CVE identifiers, and severity level."""
    full_text = f"{article.get('title', '')} {article.get('summary', '')} {article.get('content', '')}"
    cves = extract_cves(full_text)
    category = classify_category(
        article.get("title", ""),
        article.get("summary", ""),
        article.get("source", "")
    )
    severity = determine_severity(
        article.get("title", ""),
        article.get("summary", ""),
        cves
    )

    enriched = dict(article)
    enriched["cves"] = cves
    enriched["category"] = category
    enriched["severity"] = severity
    return enriched
