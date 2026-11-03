from app.fetchers.rss_fetcher import fetch_news
from app.processors.summarizer import summarize

news = fetch_news()

article = news[0]

print("=" * 70)
print("TITLE:")
print(article["title"])
print("=" * 70)

summary = summarize(article)

print("\nAI SUMMARY:\n")
print(summary)