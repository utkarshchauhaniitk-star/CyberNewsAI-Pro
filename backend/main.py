import math
import os
import sys
from pathlib import Path
from typing import Optional, List

# Ensure project root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from backend.database import init_db
from backend.models import (
    ArticleResponse,
    ArticlesListResponse,
    ThreatStatsResponse,
    SummarizeRequest,
    SummarizeResponse,
    GenerateScriptRequest,
    ScriptResponse,
    RefreshResponse
)
from backend.services.news_service import (
    seed_database_if_empty,
    refresh_news_feed,
    query_articles,
    get_article_by_id,
    update_article_ai_summary,
    get_threat_statistics,
    save_generated_script,
    get_all_scripts,
    get_script_by_id,
    toggle_article_pin
)
from backend.services.ai_service import (
    generate_article_summary,
    generate_video_script,
    export_script_as_text
)
from backend.services.threat_classifier import CATEGORY_KEYWORDS


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes SQLite schema and seeds with verified threat data on launch."""
    init_db()
    seed_database_if_empty()
    print("🚀 CyberNewsAI FastAPI backend initialized successfully.")
    yield


# Immediate fallback initialization in case lifespan isn't entered (e.g. testing without context manager)
init_db()
seed_database_if_empty()

app = FastAPI(
    title="CyberNewsAI — Threat Intelligence API",
    description="Professional cybersecurity news ingestion, threat intelligence analytics, and AI video narration script generator.",
    version="2.0.0",
    lifespan=lifespan
)

# Enable CORS for frontend Vite/React development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["System"])
def health_check():
    """Health status and environment diagnostics."""
    has_gemini_key = bool(os.getenv("GEMINI_API_KEY"))
    return {
        "status": "healthy",
        "service": "CyberNewsAI Threat Intelligence Engine",
        "version": "2.0.0",
        "gemini_api_configured": has_gemini_key
    }


@app.get("/api/categories", tags=["Metadata"])
def get_categories() -> List[str]:
    """Returns available threat intelligence categories."""
    return ["All"] + list(CATEGORY_KEYWORDS.keys()) + ["General Cyber"]


@app.get("/api/sources", tags=["Metadata"])
def get_sources() -> List[str]:
    """Returns list of monitored cybersecurity news sources."""
    return ["All", "BleepingComputer", "The Hacker News", "SecurityWeek", "CISA", "KrebsOnSecurity"]


@app.get("/api/articles", response_model=ArticlesListResponse, tags=["Articles"])
def list_articles(
    q: Optional[str] = Query(None, description="Search query across titles, summaries, and CVEs"),
    category: Optional[str] = Query("All", description="Threat category filter"),
    source: Optional[str] = Query("All", description="Source vendor filter"),
    severity: Optional[str] = Query("All", description="Severity filter: Critical, High, Medium, Low"),
    has_cve: Optional[bool] = Query(None, description="Filter for articles with specific CVE identifiers"),
    pinned_only: Optional[bool] = Query(None, description="Filter for pinned articles"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(12, ge=1, le=50, description="Items per page")
):
    """Retrieves paginated, searchable, and filtered cybersecurity articles."""
    items, total = query_articles(
        search=q,
        category=category,
        source=source,
        severity=severity,
        has_cve=has_cve,
        pinned_only=pinned_only,
        page=page,
        limit=limit
    )

    total_pages = max(1, math.ceil(total / limit))
    return ArticlesListResponse(
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages,
        items=items
    )


@app.post("/api/articles/{article_id}/pin", tags=["Articles"])
def pin_article(article_id: str):
    """Toggles pinning an article for instant access."""
    try:
        new_state = toggle_article_pin(article_id)
        return {"article_id": article_id, "is_pinned": new_state, "message": "Article pinned" if new_state else "Article unpinned"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.get("/api/articles/{article_id}", response_model=ArticleResponse, tags=["Articles"])
def get_article(article_id: str):
    """Retrieves comprehensive details for an individual article."""
    art = get_article_by_id(article_id)
    if not art:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with ID '{article_id}' not found."
        )
    return art


@app.post("/api/articles/{article_id}/summarize", response_model=SummarizeResponse, tags=["AI Services"])
def summarize_article(article_id: str, payload: SummarizeRequest):
    """Generates or returns an AI-crafted concise summary for an article."""
    art = get_article_by_id(article_id)
    if not art:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with ID '{article_id}' not found."
        )

    # If already summarized, return existing AI summary
    if art.get("is_ai_summarized") and art.get("ai_summary"):
        return SummarizeResponse(
            article_id=article_id,
            summary=art["ai_summary"],
            is_ai_generated=True,
            source_disclaimer="AI-generated summary based solely on verified report details."
        )

    result = generate_article_summary(art, max_words=payload.max_words)
    update_article_ai_summary(article_id, result["summary"])

    return SummarizeResponse(
        article_id=article_id,
        summary=result["summary"],
        is_ai_generated=True,
        source_disclaimer=result.get("source_disclaimer")
    )


@app.post("/api/news/refresh", response_model=RefreshResponse, tags=["News Ingestion"])
def refresh_news():
    """Polls external RSS feeds, enriches stories with threat intelligence, and stores them."""
    result = refresh_news_feed()
    return RefreshResponse(**result)


@app.get("/api/threat-stats", response_model=ThreatStatsResponse, tags=["Threat Intelligence"])
def get_threat_stats():
    """Aggregates real-time metrics across all threat stories, categories, and CVEs."""
    stats = get_threat_statistics()
    return ThreatStatsResponse(**stats)


@app.post("/api/scripts/generate", response_model=ScriptResponse, tags=["Script Studio"])
def generate_script_endpoint(payload: GenerateScriptRequest):
    """Synthesizes a full cybersecurity video narration script from selected articles."""
    articles = []
    for art_id in payload.article_ids:
        art = get_article_by_id(art_id)
        if art:
            articles.append(art)

    if not articles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="None of the selected article IDs could be found in the database."
        )

    script_data = generate_video_script(
        articles=articles,
        duration_minutes=payload.duration_minutes,
        video_style=payload.video_style
    )

    save_generated_script(script_data)

    return ScriptResponse(
        id=script_data["id"],
        title=script_data["title"],
        target_duration=script_data["target_duration"],
        script_content=script_data["script_content"],
        seo_title=script_data["seo_title"],
        description=script_data["description"],
        tags=script_data["tags"],
        article_ids=script_data["article_ids"],
        article_titles=script_data["article_titles"],
        is_ai_generated=True,
        created_at=script_data["created_at"]
    )


@app.get("/api/scripts", tags=["Script Studio"])
def list_scripts():
    """Lists previously generated video narration scripts."""
    return get_all_scripts()


@app.get("/api/scripts/{script_id}", response_model=ScriptResponse, tags=["Script Studio"])
def get_script(script_id: str):
    """Retrieves a single generated script."""
    script = get_script_by_id(script_id)
    if not script:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Script with ID '{script_id}' not found."
        )
    return script


@app.get("/api/scripts/{script_id}/export", tags=["Script Studio"])
def export_script(script_id: str):
    """Exports a generated script as a clean downloadable .txt file."""
    script = get_script_by_id(script_id)
    if not script:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Script with ID '{script_id}' not found."
        )

    exported_text = export_script_as_text(script)
    filename = f"cybernews_script_{script_id[:8]}.txt"

    return Response(
        content=exported_text,
        media_type="text/plain; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )


# ---------------------------------------------------------------------------
# Mount React Frontend SPA (if built)
# ---------------------------------------------------------------------------
FRONTEND_DIST_DIR = ROOT_DIR / "frontend" / "dist"

if FRONTEND_DIST_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST_DIR / "assets")), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        # Allow API requests through
        if full_path.startswith("api"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        file_path = FRONTEND_DIST_DIR / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(FRONTEND_DIST_DIR / "index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
