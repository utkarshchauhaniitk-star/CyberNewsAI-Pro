import sqlite3
import os
import json
from pathlib import Path
from typing import Optional, Dict, Any, List

DB_DIR = Path(__file__).resolve().parent.parent / "data"
DB_PATH = DB_DIR / "cybernews.db"


def get_db_connection() -> sqlite3.Connection:
    """Returns an SQLite connection with Row factory and WAL mode enabled."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


def init_db():
    """Initializes SQLite database tables and indices."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Articles table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        source TEXT NOT NULL,
        summary TEXT,
        content TEXT,
        link TEXT UNIQUE NOT NULL,
        published TEXT,
        published_date TEXT,
        category TEXT NOT NULL DEFAULT 'General Cyber',
        cves TEXT DEFAULT '[]',
        severity TEXT NOT NULL DEFAULT 'Medium',
        ai_summary TEXT,
        is_ai_summarized INTEGER DEFAULT 0,
        is_pinned INTEGER DEFAULT 0,
        created_at TEXT DEFAULT (datetime('now')),
        updated_at TEXT DEFAULT (datetime('now'))
    );
    """)

    # Alter table if is_pinned column is missing (for existing databases)
    try:
        cursor.execute("ALTER TABLE articles ADD COLUMN is_pinned INTEGER DEFAULT 0;")
    except Exception:
        pass

    # Indices for high-performance querying and filtering
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_articles_category ON articles(category);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_articles_severity ON articles(severity);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_articles_source ON articles(source);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_articles_pubdate ON articles(published_date DESC);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_articles_pinned ON articles(is_pinned);")

    # Scripts table for video narration scripts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scripts (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        target_duration TEXT NOT NULL,
        article_ids TEXT NOT NULL,
        script_content TEXT NOT NULL,
        seo_title TEXT,
        description TEXT,
        tags TEXT,
        is_ai_generated INTEGER DEFAULT 1,
        created_at TEXT DEFAULT (datetime('now'))
    );
    """)

    conn.commit()
    conn.close()
