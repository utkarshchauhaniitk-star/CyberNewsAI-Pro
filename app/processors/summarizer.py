from app.ai.gemini_client import ask_gemini


def summarize(article):
    prompt = f"""
You are a cybersecurity journalist.

Summarize the following news article in around 150 words.

Title:
{article['title']}

Summary:
{article['summary']}

Use simple English.
"""

    return ask_gemini(prompt)