import requests
import feedparser

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    ),
    "Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}

RSS_FEEDS = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.securityweek.com/feed/",
    "https://krebsonsecurity.com/feed/",
    "https://www.bleepingcomputer.com/feed/",
]


def fetch_news():
    articles = []

    for url in RSS_FEEDS:

        print(f"\nFetching: {url}")

        try:
            response = requests.get(
                url,
                headers=HEADERS,
                timeout=20,
            )

            print("Status Code:", response.status_code)

            if response.status_code != 200:
                print("Skipping...")
                continue

            feed = feedparser.parse(response.content)

            print("Entries Found:", len(feed.entries))

            for entry in feed.entries:

                articles.append({
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "summary": entry.get("summary", "")
                })

        except Exception as e:
            print("ERROR:", e)

    print(f"\nTotal Articles: {len(articles)}")

    return articles