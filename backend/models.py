from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class ArticleBase(BaseModel):
    title: str
    source: str
    summary: Optional[str] = ""
    content: Optional[str] = ""
    link: str
    published: Optional[str] = ""
    published_date: Optional[str] = ""
    category: str = "General Cyber"
    cves: List[str] = Field(default_factory=list)
    severity: str = "Medium"
    ai_summary: Optional[str] = None
    is_ai_summarized: bool = False
    is_pinned: bool = False


class ArticleResponse(ArticleBase):
    id: str
    created_at: Optional[str] = None


class ArticlesListResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    items: List[ArticleResponse]


class ThreatStatsResponse(BaseModel):
    total_articles: int
    critical_threats: int
    high_threats: int
    medium_threats: int
    low_threats: int
    cve_count: int
    category_counts: Dict[str, int]
    severity_counts: Dict[str, int]
    source_counts: Dict[str, int]
    recent_cves: List[str]
    last_updated: Optional[str] = None


class SummarizeRequest(BaseModel):
    max_words: Optional[int] = Field(default=150, ge=50, le=400)


class SummarizeResponse(BaseModel):
    article_id: str
    summary: str
    is_ai_generated: bool
    source_disclaimer: str = "AI-generated summary based solely on reported facts."


class GenerateScriptRequest(BaseModel):
    article_ids: List[str] = Field(..., min_length=1, max_length=10)
    video_style: Optional[str] = Field(default="briefing", description="briefing, deep_dive, or urgent_alert")
    duration_minutes: Optional[int] = Field(default=5, ge=1, le=15)
    custom_instructions: Optional[str] = None


class ScriptResponse(BaseModel):
    id: str
    title: str
    target_duration: str
    script_content: str
    seo_title: str
    description: str
    tags: List[str]
    article_ids: List[str]
    article_titles: List[str]
    is_ai_generated: bool
    created_at: str


class RefreshResponse(BaseModel):
    success: bool
    message: str
    articles_fetched: int
    new_articles_added: int
    total_in_db: int
