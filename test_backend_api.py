import sys
import os

# Ensure current directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from backend.main import app

def run_all_backend_tests():
    print("=" * 60)
    print("🧪 Running CyberNewsAI Backend Test Suite")
    print("=" * 60)

    client = TestClient(app)

    # 1. Health check
    print("\n[1/8] Testing /api/health ...")
    res = client.get("/api/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    health_data = res.json()
    print(f"✅ Health status: {health_data['status']}, Version: {health_data['version']}")

    # 2. Categories & Sources
    print("\n[2/8] Testing /api/categories & /api/sources ...")
    cat_res = client.get("/api/categories")
    assert cat_res.status_code == 200
    categories = cat_res.json()
    assert "Ransomware & Extortion" in categories
    print(f"✅ Categories loaded: {len(categories)} categories found.")

    src_res = client.get("/api/sources")
    assert src_res.status_code == 200
    sources = src_res.json()
    assert "BleepingComputer" in sources
    print(f"✅ Sources loaded: {sources}")

    # 3. Articles listing and pagination
    print("\n[3/8] Testing /api/articles (Listing, Pagination) ...")
    art_res = client.get("/api/articles?limit=5&page=1")
    assert art_res.status_code == 200
    art_data = art_res.json()
    print(f"✅ Total articles in DB: {art_data['total']}, Total pages: {art_data['total_pages']}")
    assert art_data["total"] > 0
    assert len(art_data["items"]) <= 5
    sample_article = art_data["items"][0]
    print(f"   Sample story: '{sample_article['title']}' [{sample_article['category']} | {sample_article['severity']}]")

    # 4. Search and Category filtering
    print("\n[4/8] Testing Search and Filtering ...")
    search_res = client.get("/api/articles?q=malware")
    assert search_res.status_code == 200
    search_data = search_res.json()
    print(f"✅ Search for 'malware' returned {search_data['total']} matching stories.")

    filter_res = client.get("/api/articles?category=Ransomware%20%26%20Extortion")
    assert filter_res.status_code == 200
    filter_data = filter_res.json()
    print(f"✅ Filter by 'Ransomware & Extortion' returned {filter_data['total']} stories.")

    # 5. Article Detail
    print("\n[5/8] Testing /api/articles/{id} detail view ...")
    art_id = sample_article["id"]
    detail_res = client.get(f"/api/articles/{art_id}")
    assert detail_res.status_code == 200
    detail_data = detail_res.json()
    assert detail_data["id"] == art_id
    print(f"✅ Article details verified for ID: {art_id}")

    # 6. Threat Statistics
    print("\n[6/8] Testing /api/threat-stats ...")
    stats_res = client.get("/api/threat-stats")
    assert stats_res.status_code == 200
    stats = stats_res.json()
    print(f"✅ Total Threat Articles: {stats['total_articles']}")
    print(f"   Critical: {stats['critical_threats']}, High: {stats['high_threats']}, Medium: {stats['medium_threats']}, Low: {stats['low_threats']}")
    print(f"   Detected CVEs: {stats['cve_count']} ({stats['recent_cves'][:5]})")
    print(f"   Category breakdown: {stats['category_counts']}")

    # 7. AI Article Summarization
    print("\n[7/8] Testing /api/articles/{id}/summarize ...")
    summary_res = client.post(f"/api/articles/{art_id}/summarize", json={"max_words": 120})
    assert summary_res.status_code == 200
    sum_data = summary_res.json()
    assert sum_data["is_ai_generated"] is True
    assert len(sum_data["summary"]) > 20
    print(f"✅ Summary generated: {sum_data['summary'][:120]}...")

    # 8. Script Generation & Export
    print("\n[8/8] Testing /api/scripts/generate and Export ...")
    # Take first 2 article IDs
    article_ids = [item["id"] for item in art_data["items"][:2]]
    script_req = {
        "article_ids": article_ids,
        "video_style": "briefing",
        "duration_minutes": 3
    }
    script_res = client.post("/api/scripts/generate", json=script_req)
    assert script_res.status_code == 200
    script_data = script_res.json()
    script_id = script_data["id"]
    print(f"✅ Script generated successfully (ID: {script_id})")
    print(f"   SEO Title: {script_data['seo_title']}")
    print(f"   Excerpt: {script_data['script_content'][:150]}...")

    # Test export endpoint
    export_res = client.get(f"/api/scripts/{script_id}/export")
    assert export_res.status_code == 200
    assert "text/plain" in export_res.headers["content-type"]
    assert "attachment" in export_res.headers["content-disposition"]
    assert "CYBERNEWSAI" in export_res.text
    print(f"✅ Script export verified. File payload length: {len(export_res.text)} bytes.")

    print("\n" + "=" * 60)
    print("🎉 ALL 8 BACKEND TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_all_backend_tests()
