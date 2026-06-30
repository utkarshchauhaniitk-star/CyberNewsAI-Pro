import feedparser
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 Chrome/137.0 Safari/537.36"
    )
}


RSS_FEEDS = {
    "BleepingComputer": "https://www.bleepingcomputer.com/feed/",
    "The Hacker News": "https://feeds.feedburner.com/TheHackersNews",
    "SecurityWeek": "https://securityweek.com/feed/",
    "CISA": "https://www.cisa.gov/news.xml",
}


def clean_html(text):
    return BeautifulSoup(text, "html.parser").get_text(" ", strip=True)


def fetch_feed(name, url):
    """
    Fetch one RSS feed.
    """

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    feed = feedparser.parse(response.content)

    articles = []

    for entry in feed.entries:

        articles.append({

            "source": name,

            "title": entry.get("title", ""),

            "summary": clean_html(

                entry.get("summary", "")

            ),

            "link": entry.get("link", ""),

            "published": entry.get(

                "published",

                ""

            )

        })

    return articles


def fetch_all_news():

    all_articles = []

    for source, url in RSS_FEEDS.items():

        try:

            print(f"Fetching {source}...")

            news = fetch_feed(source, url)

            print(f"   {len(news)} articles")

            all_articles.extend(news)

        except Exception as e:

            print(f"{source} failed")

            print(e)

    return all_articles