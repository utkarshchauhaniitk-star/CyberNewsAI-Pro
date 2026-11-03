import os

from news.rss_fetcher import fetch_all_news
from app.processors.ranker import rank_articles
from app.processors.bulk_summarizer import summarize_articles
from app.generators.content_generator import generate_content


OUTPUT_DIR = "output"


def save_file(filename, content):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    path = os.path.join(OUTPUT_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Saved: {path}")


def main():
    print("=" * 60)
    print("🚀 Starting CyberNewsAI v2")
    print("=" * 60)

    # ---------------------------------------------------
    # STEP 1 - Fetch News
    # ---------------------------------------------------
    print("\n📡 Fetching RSS Feeds...\n")

    articles = fetch_all_news()

    print(f"\nFetched {len(articles)} articles.")

    # ---------------------------------------------------
    # STEP 2 - Rank Articles
    # ---------------------------------------------------
    print("\n🤖 Ranking today's most important stories...\n")

    top_articles = rank_articles(articles)

    print(f"\nSelected {len(top_articles)} stories.")

    # ---------------------------------------------------
    # STEP 3 - Summaries
    # ---------------------------------------------------
    print("\n📝 Generating summaries...\n")

    summaries = summarize_articles(top_articles)

    save_file("summaries.md", summaries)

    # ---------------------------------------------------
    # STEP 4 - Generate Content Package
    # ---------------------------------------------------
    print("\n🎬 Generating YouTube content...\n")

    content = generate_content(summaries)

    # ---------------------------------------------------
    # STEP 5 - Save Everything
    # ---------------------------------------------------
    save_file("script.md", content["script"])

    save_file("seo_title.txt", content["seo_title"])

    save_file("description.txt", content["description"])

    save_file("tags.txt", content["tags"])

    save_file("shorts.txt", content["shorts"])

    save_file(
        "thumbnail_prompt.txt",
        content["thumbnail_prompt"],
    )

    save_file("raw_output.txt", content["raw"])

    print("\n" + "=" * 60)
    print("🎉 CyberNewsAI Completed Successfully!")
    print("=" * 60)

    print("\nGenerated Files:")

    print("📄 summaries.md")
    print("📄 script.md")
    print("📄 seo_title.txt")
    print("📄 description.txt")
    print("📄 tags.txt")
    print("📄 shorts.txt")
    print("📄 thumbnail_prompt.txt")
    print("📄 raw_output.txt")


if __name__ == "__main__":
    main()