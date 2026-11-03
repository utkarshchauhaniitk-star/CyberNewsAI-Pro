from app.fetchers.rss_fetcher import fetch_news

news = fetch_news()

print(f"\nFound {len(news)} articles\n")

for article in news[:5]:
    print(article["title"])
    print(article["link"])
    print("-" * 70)