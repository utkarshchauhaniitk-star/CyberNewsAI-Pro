const API_BASE = '/api';

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error('Health check failed');
  return res.json();
}

export async function fetchCategories() {
  const res = await fetch(`${API_BASE}/categories`);
  if (!res.ok) throw new Error('Failed to load categories');
  return res.json();
}

export async function fetchSources() {
  const res = await fetch(`${API_BASE}/sources`);
  if (!res.ok) throw new Error('Failed to load news sources');
  return res.json();
}

export async function fetchArticles({
  q = '',
  category = 'All',
  source = 'All',
  severity = 'All',
  has_cve = null,
  pinned_only = null,
  page = 1,
  limit = 12
} = {}) {
  const params = new URLSearchParams();
  if (q) params.set('q', q);
  if (category && category !== 'All') params.set('category', category);
  if (source && source !== 'All') params.set('source', source);
  if (severity && severity !== 'All') params.set('severity', severity);
  if (has_cve !== null) params.set('has_cve', String(has_cve));
  if (pinned_only !== null) params.set('pinned_only', String(pinned_only));
  params.set('page', String(page));
  params.set('limit', String(limit));

  const res = await fetch(`${API_BASE}/articles?${params.toString()}`);
  if (!res.ok) throw new Error(`Failed to fetch articles (${res.status})`);
  return res.json();
}

export async function togglePinArticle(id) {
  const res = await fetch(`${API_BASE}/articles/${id}/pin`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  });
  if (!res.ok) throw new Error(`Failed to pin article (${res.status})`);
  return res.json();
}

export async function fetchArticleById(id) {
  const res = await fetch(`${API_BASE}/articles/${id}`);
  if (!res.ok) throw new Error(`Article not found (${res.status})`);
  return res.json();
}

export async function summarizeArticle(id, maxWords = 150) {
  const res = await fetch(`${API_BASE}/articles/${id}/summarize`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ max_words: maxWords })
  });
  if (!res.ok) throw new Error(`Failed to generate summary (${res.status})`);
  return res.json();
}

export async function refreshNewsFeeds() {
  const res = await fetch(`${API_BASE}/news/refresh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  });
  if (!res.ok) throw new Error(`Failed to refresh feeds (${res.status})`);
  return res.json();
}

export async function fetchThreatStats() {
  const res = await fetch(`${API_BASE}/threat-stats`);
  if (!res.ok) throw new Error(`Failed to load threat statistics (${res.status})`);
  return res.json();
}

export async function generateNarrationScript({
  article_ids,
  video_style = 'briefing',
  duration_minutes = 5
}) {
  const res = await fetch(`${API_BASE}/scripts/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      article_ids,
      video_style,
      duration_minutes
    })
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to generate script (${res.status})`);
  }
  return res.json();
}

export async function fetchSavedScripts() {
  const res = await fetch(`${API_BASE}/scripts`);
  if (!res.ok) throw new Error('Failed to load script history');
  return res.json();
}

export function getScriptExportUrl(id) {
  return `${API_BASE}/scripts/${id}/export`;
}
