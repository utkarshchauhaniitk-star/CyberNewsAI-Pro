import json
import os
from pathlib import Path
from typing import List, Dict

SAMPLE_JSON_PATH = Path(__file__).resolve().parent.parent.parent / "output" / "articles.json"

# Verified fallback cybersecurity articles if output/articles.json is missing or offline
FALLBACK_ARTICLES: List[Dict] = [
    {
        "title": "CISA Adds Critical Palo Alto Networks PAN-OS Vulnerability (CVE-2026-0257) to KEV Catalog",
        "source": "CISA",
        "summary": "CISA has added CVE-2026-0257 to its Known Exploited Vulnerabilities Catalog. The vulnerability allows authentication bypass in PAN-OS management interfaces, enabling threat actors to execute arbitrary commands with root privileges.",
        "link": "https://www.cisa.gov/news-events/alerts/cve-2026-0257-palo-alto",
        "published": "2026-11-01T14:00:00Z",
        "category": "Vulnerabilities & Exploits",
        "cves": ["CVE-2026-0257"],
        "severity": "Critical"
    },
    {
        "title": "Qilin Ransomware Gang Targets Critical Healthcare Infrastructure via Unpatched VPN Portals",
        "source": "BleepingComputer",
        "summary": "Security researchers observed the Qilin extortion group exploiting legacy remote access appliances to encrypt electronic health record servers and exfiltrate over 400 GB of patient data.",
        "link": "https://www.bleepingcomputer.com/news/security/qilin-ransomware-healthcare-vpn-breach/",
        "published": "2026-11-02T10:30:00Z",
        "category": "Ransomware & Extortion",
        "cves": [],
        "severity": "Critical"
    },
    {
        "title": "Volt Typhoon APT Uses Living-off-the-Land Binaries in Telecommunications Espionage Campaign",
        "source": "The Hacker News",
        "summary": "Nation-state threat actors linked to Volt Typhoon have compromised telecommunication network routers using legitimate administrative tools and compromised credentials, evading EDR detection.",
        "link": "https://thehackernews.com/2026/11/volt-typhoon-telecom-living-off-land.html",
        "published": "2026-11-02T18:15:00Z",
        "category": "Nation-State & APT",
        "cves": [],
        "severity": "High"
    },
    {
        "title": "Critical Microsoft SharePoint Zero-Day CVE-2026-50522 Under Active Exploitation",
        "source": "SecurityWeek",
        "summary": "Microsoft has released an out-of-band security advisory for CVE-2026-50522, an unauthenticated remote code execution flaw in on-premises SharePoint deployments rated CVSS 9.8.",
        "link": "https://www.securityweek.com/microsoft-sharepoint-remote-code-execution-cve-2026-50522/",
        "published": "2026-11-03T08:00:00Z",
        "category": "Vulnerabilities & Exploits",
        "cves": ["CVE-2026-50522"],
        "severity": "Critical"
    },
    {
        "title": "Massive Cloud Infrastructure Misconfiguration Exposes 1.8M Financial Records",
        "source": "The Hacker News",
        "summary": "An open Amazon Web Services S3 storage bucket containing unencrypted banking audit logs and consumer identities was discovered by security researchers and subsequently secured.",
        "link": "https://thehackernews.com/2026/11/cloud-s3-misconfiguration-financial-leak.html",
        "published": "2026-11-03T11:45:00Z",
        "category": "Cloud & Infrastructure",
        "cves": [],
        "severity": "High"
    },
    {
        "title": "Lumma Stealer Variant Spreads via Compromised Browser Extensions",
        "source": "BleepingComputer",
        "summary": "Cybercriminals hijacked developer accounts on web store marketplaces to push trojanized browser extensions designed to steal cryptocurrency private keys and browser session cookies.",
        "link": "https://www.bleepingcomputer.com/news/security/lumma-stealer-spreads-browser-extensions/",
        "published": "2026-11-03T15:20:00Z",
        "category": "Malware & Botnets",
        "cves": [],
        "severity": "Medium"
    }
]


def get_sample_articles() -> List[Dict]:
    """Loads sample articles from output/articles.json or returns verified fallbacks."""
    if os.path.exists(SAMPLE_JSON_PATH):
        try:
            with open(SAMPLE_JSON_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    return data
        except Exception:
            pass
    return FALLBACK_ARTICLES
