import hashlib
import json
import sqlite3
import datetime
from typing import List, Dict, Optional, Tuple

from backend.database import get_db_connection
from backend.services.threat_classifier import enrich_article_metadata
from backend.services.sample_data import get_sample_articles
from news.rss_fetcher import fetch_all_news
from news.deduplicator import remove_duplicates


def generate_article_id(link: str, title: str) -> str:
    """Generates a deterministic unique hash ID for an article based on link and title."""
    seed = (link or title).strip().lower().encode("utf-8")
    return hashlib.sha256(seed).hexdigest()[:16]


def parse_iso_date(raw_date: Optional[str]) -> str:
    """Converts RSS raw date strings into standard ISO format for proper chronological ordering."""
    if not raw_date:
        return datetime.datetime.now().isoformat()
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(raw_date)
        return dt.isoformat()
    except Exception:
        pass
    try:
        from dateutil import parser
        dt = parser.parse(raw_date)
        return dt.isoformat()
    except Exception:
        return datetime.datetime.now().isoformat()


def upsert_article(conn: sqlite3.Connection, article_data: Dict) -> bool:
    """Inserts or updates an article in SQLite. Preserves user pinned state and AI summary. Returns True if newly inserted."""
    cursor = conn.cursor()
    art_id = article_data.get("id") or generate_article_id(article_data.get("link", ""), article_data.get("title", ""))
    
    # Check if exists
    cursor.execute("SELECT id, is_ai_summarized, ai_summary, is_pinned FROM articles WHERE id = ?", (art_id,))
    existing = cursor.fetchone()

    cves_json = json.dumps(article_data.get("cves", []))
    pub_iso = parse_iso_date(article_data.get("published", ""))

    if existing:
        cursor.execute("""
            UPDATE articles SET
                title = ?,
                source = ?,
                summary = ?,
                content = COALESCE(?, content),
                link = ?,
                published = ?,
                published_date = ?,
                category = ?,
                cves = ?,
                severity = ?,
                updated_at = datetime('now')
            WHERE id = ?
        """, (
            article_data.get("title"),
            article_data.get("source"),
            article_data.get("summary"),
            article_data.get("content"),
            article_data.get("link"),
            article_data.get("published"),
            pub_iso,
            article_data.get("category", "General Cyber"),
            cves_json,
            article_data.get("severity", "Medium"),
            art_id
        ))
        return False
    else:
        cursor.execute("""
            INSERT INTO articles (
                id, title, source, summary, content, link,
                published, published_date, category, cves, severity,
                ai_summary, is_ai_summarized, is_pinned
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            art_id,
            article_data.get("title"),
            article_data.get("source"),
            article_data.get("summary"),
            article_data.get("content", ""),
            article_data.get("link"),
            article_data.get("published"),
            pub_iso,
            article_data.get("category", "General Cyber"),
            cves_json,
            article_data.get("severity", "Medium"),
            article_data.get("ai_summary", None),
            1 if article_data.get("ai_summary") else 0,
            1 if article_data.get("is_pinned") else 0
        ))
        return True


def seed_database_if_empty():
    """Seeds the SQLite database with verified sample cyber news if no articles exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM articles;")
    count = cursor.fetchone()[0]

    if count == 0:
        print("[Database] Articles table is empty. Initializing with sample dataset...")
        sample_articles = get_sample_articles()
        deduped = remove_duplicates(sample_articles)
        inserted = 0
        for raw in deduped:
            enriched = enrich_article_metadata(raw)
            if upsert_article(conn, enriched):
                inserted += 1
        conn.commit()
        print(f"[Database] Successfully seeded {inserted} verified articles.")
    conn.close()


def refresh_news_feed() -> Dict:
    """Fetches live RSS feeds concurrently from the internet, deduplicates, enriches with metadata, and updates SQLite."""
    conn = get_db_connection()
    t_start = datetime.datetime.now()
    try:
        raw_articles = fetch_all_news()
        if not raw_articles:
            print("[NewsService] Live fetch returned 0 articles. Falling back to cached seed.")
            raw_articles = get_sample_articles()

        deduped = remove_duplicates(raw_articles)
        new_count = 0
        for item in deduped:
            enriched = enrich_article_metadata(item)
            if upsert_article(conn, enriched):
                new_count += 1
        conn.commit()

        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM articles;")
        total_in_db = cursor.fetchone()[0]

        duration = (datetime.datetime.now() - t_start).total_seconds()

        return {
            "success": True,
            "message": f"Real-time sync complete: Captured {len(raw_articles)} live threat advisories ({new_count} new) in {duration:.1f}s.",
            "articles_fetched": len(raw_articles),
            "new_articles_added": new_count,
            "total_in_db": total_in_db,
            "duration_seconds": round(duration, 2)
        }
    except Exception as e:
        conn.rollback()
        print(f"[NewsService] Error refreshing feeds: {e}")
        return {
            "success": False,
            "message": f"Failed to refresh live feeds: {str(e)}",
            "articles_fetched": 0,
            "new_articles_added": 0,
            "total_in_db": 0
        }
    finally:
        conn.close()


def query_articles(
    search: Optional[str] = None,
    category: Optional[str] = None,
    source: Optional[str] = None,
    severity: Optional[str] = None,
    has_cve: Optional[bool] = None,
    pinned_only: Optional[bool] = None,
    page: int = 1,
    limit: int = 12
) -> Tuple[List[Dict], int]:
    """Queries articles from SQLite with filtering, searching, and pagination."""
    conn = get_db_connection()
    cursor = conn.cursor()

    conditions = []
    params = []

    if search:
        search_param = f"%{search.strip().lower()}%"
        conditions.append("(LOWER(title) LIKE ? OR LOWER(summary) LIKE ? OR LOWER(cves) LIKE ?)")
        params.extend([search_param, search_param, search_param])

    if category and category != "All":
        conditions.append("category = ?")
        params.append(category)

    if source and source != "All":
        conditions.append("source = ?")
        params.append(source)

    if severity and severity != "All":
        conditions.append("severity = ?")
        params.append(severity)

    if has_cve is True:
        conditions.append("cves != '[]' AND cves IS NOT NULL")
    elif has_cve is False:
        conditions.append("(cves = '[]' OR cves IS NULL)")

    if pinned_only is True:
        conditions.append("is_pinned = 1")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    # Total count query
    count_query = f"SELECT COUNT(*) FROM articles {where_clause}"
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]

    # Paginated query
    offset = (page - 1) * limit
    data_query = f"""
        SELECT id, title, source, summary, content, link, published, published_date,
               category, cves, severity, ai_summary, is_ai_summarized, is_pinned, created_at
        FROM articles
        {where_clause}
        ORDER BY is_pinned DESC, published_date DESC, created_at DESC
        LIMIT ? OFFSET ?
    """
    cursor.execute(data_query, params + [limit, offset])
    rows = cursor.fetchall()

    results = []
    for r in rows:
        results.append({
            "id": r["id"],
            "title": r["title"],
            "source": r["source"],
            "summary": r["summary"],
            "content": r["content"],
            "link": r["link"],
            "published": r["published"],
            "published_date": r["published_date"],
            "category": r["category"],
            "cves": json.loads(r["cves"]) if r["cves"] else [],
            "severity": r["severity"],
            "ai_summary": r["ai_summary"],
            "is_ai_summarized": bool(r["is_ai_summarized"]),
            "is_pinned": bool(r["is_pinned"]),
            "created_at": r["created_at"]
        })

    conn.close()
    return results, total


def toggle_article_pin(article_id: str) -> bool:
    """Toggles the pinned status of an article in SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT is_pinned FROM articles WHERE id = ?", (article_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise ValueError(f"Article {article_id} not found")

    new_val = 0 if row[0] == 1 else 1
    cursor.execute("UPDATE articles SET is_pinned = ?, updated_at = datetime('now') WHERE id = ?", (new_val, article_id))
    conn.commit()
    conn.close()
    return bool(new_val)


def get_article_by_id(article_id: str) -> Optional[Dict]:
    """Retrieves a single article by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, source, summary, content, link, published, published_date,
               category, cves, severity, ai_summary, is_ai_summarized, is_pinned, created_at
        FROM articles WHERE id = ?
    """, (article_id,))
    r = cursor.fetchone()
    conn.close()

    if not r:
        return None

    return {
        "id": r["id"],
        "title": r["title"],
        "source": r["source"],
        "summary": r["summary"],
        "content": r["content"],
        "link": r["link"],
        "published": r["published"],
        "published_date": r["published_date"],
        "category": r["category"],
        "cves": json.loads(r["cves"]) if r["cves"] else [],
        "severity": r["severity"],
        "ai_summary": r["ai_summary"],
        "is_ai_summarized": bool(r["is_ai_summarized"]),
        "is_pinned": bool(r["is_pinned"]),
        "created_at": r["created_at"]
    }


def update_article_ai_summary(article_id: str, summary: str):
    """Updates an article with an AI generated summary."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE articles
        SET ai_summary = ?, is_ai_summarized = 1, updated_at = datetime('now')
        WHERE id = ?
    """, (summary, article_id))
    conn.commit()
    conn.close()


def get_threat_statistics() -> Dict:
    """Computes comprehensive threat intelligence metrics across all stored articles."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM articles;")
    total_articles = cursor.fetchone()[0]

    cursor.execute("SELECT severity, COUNT(*) FROM articles GROUP BY severity;")
    severity_counts = {row[0]: row[1] for row in cursor.fetchall()}

    cursor.execute("SELECT category, COUNT(*) FROM articles GROUP BY category;")
    category_counts = {row[0]: row[1] for row in cursor.fetchall()}

    cursor.execute("SELECT source, COUNT(*) FROM articles GROUP BY source;")
    source_counts = {row[0]: row[1] for row in cursor.fetchall()}

    # Extract all distinct CVEs
    cursor.execute("SELECT cves FROM articles WHERE cves != '[]' AND cves IS NOT NULL;")
    cve_rows = cursor.fetchall()
    all_cves = set()
    for row in cve_rows:
        try:
            items = json.loads(row[0])
            for c in items:
                all_cves.add(c)
        except Exception:
            pass

    cursor.execute("SELECT MAX(updated_at) FROM articles;")
    last_updated = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM articles WHERE is_pinned = 1;")
    pinned_count = cursor.fetchone()[0]

    conn.close()

    return {
        "total_articles": total_articles,
        "critical_threats": severity_counts.get("Critical", 0),
        "high_threats": severity_counts.get("High", 0),
        "medium_threats": severity_counts.get("Medium", 0),
        "low_threats": severity_counts.get("Low", 0),
        "pinned_count": pinned_count,
        "cve_count": len(all_cves),
        "category_counts": category_counts,
        "severity_counts": severity_counts,
        "source_counts": source_counts,
        "recent_cves": sorted(list(all_cves))[:15],
        "last_updated": last_updated
    }


def save_generated_script(script_data: Dict) -> str:
    """Persists a generated video script into SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO scripts (
            id, title, target_duration, article_ids, script_content,
            seo_title, description, tags, is_ai_generated, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        script_data["id"],
        script_data["title"],
        script_data["target_duration"],
        json.dumps(script_data.get("article_ids", [])),
        script_data["script_content"],
        script_data.get("seo_title", ""),
        script_data.get("description", ""),
        json.dumps(script_data.get("tags", [])),
        1 if script_data.get("is_ai_generated") else 0,
        script_data.get("created_at")
    ))
    conn.commit()
    conn.close()
    return script_data["id"]


def get_all_scripts() -> List[Dict]:
    """Retrieves all generated scripts from SQLite ordered newest first."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, target_duration, article_ids, script_content,
               seo_title, description, tags, is_ai_generated, created_at
        FROM scripts
        ORDER BY created_at DESC
    """)
    rows = cursor.fetchall()
    scripts = []
    for r in rows:
        scripts.append({
            "id": r["id"],
            "title": r["title"],
            "target_duration": r["target_duration"],
            "article_ids": json.loads(r["article_ids"]) if r["article_ids"] else [],
            "script_content": r["script_content"],
            "seo_title": r["seo_title"],
            "description": r["description"],
            "tags": json.loads(r["tags"]) if r["tags"] else [],
            "is_ai_generated": bool(r["is_ai_generated"]),
            "created_at": r["created_at"]
        })
    conn.close()
    return scripts


def get_script_by_id(script_id: str) -> Optional[Dict]:
    """Retrieves a single generated script by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, target_duration, article_ids, script_content,
               seo_title, description, tags, is_ai_generated, created_at
        FROM scripts WHERE id = ?
    """, (script_id,))
    r = cursor.fetchone()
    conn.close()

    if not r:
        return None

    return {
        "id": r["id"],
        "title": r["title"],
        "target_duration": r["target_duration"],
        "article_ids": json.loads(r["article_ids"]) if r["article_ids"] else [],
        "script_content": r["script_content"],
        "seo_title": r["seo_title"],
        "description": r["description"],
        "tags": json.loads(r["tags"]) if r["tags"] else [],
        "is_ai_generated": bool(r["is_ai_generated"]),
        "created_at": r["created_at"]
    }
