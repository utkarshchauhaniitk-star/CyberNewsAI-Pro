import datetime
import pytest
from news.deduplicator import remove_duplicates
from news.rss_fetcher import clean_html
from backend.services.threat_classifier import extract_cves, classify_category, determine_severity
from backend.services.news_service import parse_iso_date, generate_article_id
from backend.services.ai_service import generate_article_summary

def test_clean_html_utility():
    raw_html = "<p>Adversary launched <b>ransomware</b> attack. <a href='https://example.com'>Read more</a></p>"
    cleaned = clean_html(raw_html)
    assert "<p>" not in cleaned
    assert "<b>" not in cleaned
    assert "ransomware attack. Read more" in cleaned
    assert clean_html("") == ""
    assert clean_html(None) == ""

def test_deduplicator_removes_exact_and_link_duplicates():
    articles = [
        {"title": "CISA Releases Zero-Day Advisory", "link": "https://example.com/art1"},
        {"title": "cisa releases zero-day advisory", "link": "https://example.com/art1-copy"},  # Duplicate title
        {"title": "Unique Threat Story", "link": "https://example.com/art1"},  # Duplicate link
        {"title": "New Ransomware Strain Detected", "link": "https://example.com/art2"},
    ]
    deduped = remove_duplicates(articles)
    assert len(deduped) == 2
    titles = [a["title"] for a in deduped]
    assert "CISA Releases Zero-Day Advisory" in titles
    assert "New Ransomware Strain Detected" in titles

def test_deduplicator_handles_malformed_entries_safely():
    malformed = [
        None,
        "not a dict",
        {},
        {"title": ""},
        {"title": None},
        {"title": "Valid Article Title", "link": "https://example.com/valid"}
    ]
    deduped = remove_duplicates(malformed)
    assert len(deduped) == 1
    assert deduped[0]["title"] == "Valid Article Title"

def test_cve_extraction_and_normalization():
    sample_text = (
        "Security researchers analyzed CVE-2026-1234 and active exploitation of cve-2025-99999. "
        "Also mentioned was an invalid tag CVE-ABC and a repeat of CVE-2026-1234."
    )
    cves = extract_cves(sample_text)
    assert len(cves) == 2
    assert "CVE-2026-1234" in cves
    assert "CVE-2025-99999" in cves
    assert extract_cves("") == []
    assert extract_cves(None) == []

def test_threat_classification_and_severity():
    # 1. Ransomware classification
    cat1 = classify_category("LockBit Ransomware Encrypts Hospital Network", "Attackers demanded ransom", "BleepingComputer")
    assert cat1 == "Ransomware & Extortion"

    # 2. Critical severity trigger (actively exploited zero-day)
    sev1 = determine_severity("Critical Zero-Day Actively Exploited in the Wild", "Unauthenticated RCE", ["CVE-2026-0001"])
    assert sev1 == "Critical"

    # 3. High severity trigger (data breach / privilege escalation)
    sev2 = determine_severity("Authentication Bypass Leads to Privilege Escalation", "Adversary gained admin", ["CVE-2026-5555"])
    assert sev2 in ("High", "Critical")

    # 4. Low severity trigger (advisory / best practices)
    sev3 = determine_severity("CISA Releases Weekly Best Practices Reminder", "Routine security tips", [])
    assert sev3 == "Low"

def test_iso_date_parsing_resilience():
    # Standard RFC 2822
    rfc_date = "Tue, 10 Nov 2026 12:00:00 GMT"
    parsed1 = parse_iso_date(rfc_date)
    assert "2026-11-10" in parsed1

    # Standard ISO
    iso_date = "2026-11-10T08:30:00Z"
    parsed2 = parse_iso_date(iso_date)
    assert "2026-11-10" in parsed2

    # None or unparseable fallback
    parsed_fallback = parse_iso_date(None)
    assert parsed_fallback is not None
    assert "T" in parsed_fallback

def test_deterministic_article_id_generation():
    id1 = generate_article_id("https://krebsonsecurity.com/story1", "Krebs Story Title")
    id2 = generate_article_id("https://krebsonsecurity.com/story1", "Krebs Story Title")
    id3 = generate_article_id("https://krebsonsecurity.com/story2", "Different Title")
    assert id1 == id2
    assert id1 != id3
    assert len(id1) == 16

def test_ai_summary_heuristic_fallback_integrity():
    synthetic_article = {
        "id": "test_art_001",
        "title": "Phishing Campaign Targets Financial Organizations",
        "source": "SecurityWeek",
        "summary": "Adversaries deployed spear-phishing emails containing malicious PDF attachments. The campaign targeted senior finance executives to harvest corporate credentials.",
        "content": ""
    }
    # Test without GEMINI_API_KEY
    summary_res = generate_article_summary(synthetic_article)
    assert "summary" in summary_res
    assert len(summary_res["summary"]) > 20
    assert summary_res["article_id"] == "test_art_001"
    assert "spear-phishing" in summary_res["summary"].lower() or "security report" in summary_res["summary"].lower()
