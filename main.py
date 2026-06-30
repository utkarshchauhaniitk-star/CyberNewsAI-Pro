from news.rss_fetcher import fetch_all_news
from news.deduplicator import remove_duplicates

print("Starting CyberNewsAI...\n")

news = fetch_all_news()

print(f"\nFetched {len(news)} articles")

news = remove_duplicates(news)

print(f"After removing duplicates: {len(news)} articles\n")

print("=" * 70)

for article in news[:10]:
    print(f"\n{article['source']}")
    print(article["title"])