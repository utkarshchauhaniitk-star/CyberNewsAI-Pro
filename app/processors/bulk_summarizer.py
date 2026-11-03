from app.ai.gemini_client import ask_gemini
from news.rss_fetcher import fetch_full_articles


def summarize_articles(top_articles):
    """
    Downloads the full text of the selected articles
    and summarizes all of them in ONE Gemini request.
    """

    print("\n📥 Downloading full articles...\n")

    top_articles = fetch_full_articles(top_articles)

    article_text = ""

    for i, article in enumerate(top_articles, start=1):

        article_text += f"""
ARTICLE {i}

TITLE:
{article["title"]}

SOURCE:
{article["source"]}

CONTENT:
{article["content"]}

=========================================
"""

    prompt = f"""
You are an expert cybersecurity journalist.

Below are five cybersecurity news articles.

For EACH article provide:

Title:
Summary (100-150 words)

Use this exact format:

### ARTICLE 1
Title:
Summary:

### ARTICLE 2
Title:
Summary:

Continue until ARTICLE 5.

Articles:

{article_text}
"""

    print("🤖 Generating summaries...\n")

    return ask_gemini(prompt)