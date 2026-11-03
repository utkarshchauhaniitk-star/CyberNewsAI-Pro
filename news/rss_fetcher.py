import concurrent.futures
import feedparser
import requests
import trafilatura
from bs4 import BeautifulSoup
from typing import List, Dict

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    ),
    "Accept": "application/rss+xml, application/xml, text/xml;q=0.9, */*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9"
}

RSS_FEEDS = {
    "BleepingComputer": "https://www.bleepingcomputer.com/feed/",
    "The Hacker News": "https://feeds.feedburner.com/TheHackersNews",
    "SecurityWeek": "https://securityweek.com/feed/",
    "CISA": "https://www.cisa.gov/news.xml",
    "KrebsOnSecurity": "https://krebsonsecurity.com/feed/"
}


def clean_html(text: str) -> str:
    """Strips HTML tags cleanly to produce readable summary text."""
    if not text:
        return ""
    return BeautifulSoup(str(text), "html.parser").get_text(" ", strip=True)


def fetch_feed(source: str, url: str) -> List[Dict]:
    """Fetches and parses a single RSS feed with custom timeout and headers."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=12)
        response.raise_for_status()
        feed = feedparser.parse(response.content)

        articles = []
        for entry in feed.entries:
            title = entry.get("title", "").strip()
            if not title:
                continue

            summary = clean_html(entry.get("summary", "") or entry.get("description", ""))
            link = entry.get("link", "").strip()
            published = entry.get("published", "") or entry.get("pubDate", "")

            articles.append({
                "source": source,
                "title": title,
                "summary": summary,
                "link": link,
                "published": published
            })
        return articles
    except Exception as e:
        print(f"[RSSFetcher] Failed to fetch {source} ({url}): {e}")
        return []


def fetch_all_news() -> List[Dict]:
    """
    Fetches all configured RSS feeds concurrently in parallel.
    Completes in ~1-2 seconds instead of sequential blocking.
    """
    all_articles = []
    print("[RSSFetcher] Polling all live cyber news feeds concurrently...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(RSS_FEEDS)) as executor:
        future_to_source = {
            executor.submit(fetch_feed, source, url): source
            for source, url in RSS_FEEDS.items()
        }

        for future in concurrent.futures.as_completed(future_to_source):
            source = future_to_source[future]
            try:
                articles = future.result()
                print(f"[RSSFetcher]  ✓ {source}: {len(articles)} stories")
                all_articles.extend(articles)
            except Exception as e:
                print(f"[RSSFetcher]  ✗ {source} error: {e}")

    print(f"[RSSFetcher] Live poll complete. Ingested total {len(all_articles)} stories.")
    return all_articles


def fetch_full_article(article: Dict) -> Dict:
    """Downloads full article content on demand using trafilatura."""
    link = article.get("link")
    if not link:
        return article

    try:
        downloaded = trafilatura.fetch_url(link)
        if downloaded:
            text = trafilatura.extract(downloaded)
            if text:
                article["content"] = text
                return article
    except Exception:
        pass

    article["content"] = article.get("summary", "")
    return article


def fetch_full_articles(articles: List[Dict]) -> List[Dict]:
    """Downloads full text for a list of articles."""
    return [fetch_full_article(a) for a in articles]
