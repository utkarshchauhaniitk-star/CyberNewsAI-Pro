from app.ai.gemini_client import ask_gemini


def generate_seo(youtube_script):
    prompt = f"""
You are a YouTube SEO expert.

Based on this cybersecurity video script, generate:

1. A catchy YouTube title (under 70 characters)
2. A YouTube description (200-300 words)
3. 15 SEO hashtags
4. 20 SEO keywords separated by commas

Video Script:

{youtube_script}

Return exactly in this format:

TITLE:
...

DESCRIPTION:
...

HASHTAGS:
...

KEYWORDS:
...
"""

    return ask_gemini(prompt)