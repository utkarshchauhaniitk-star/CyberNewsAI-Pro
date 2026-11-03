import re

from app.ai.gemini_client import ask_gemini


def extract_section(text, section):
    """
    Extracts a section from Gemini output.
    """

    pattern = rf"=+\s*{re.escape(section)}\s*=+\s*(.*?)(?=\n=+[A-Z ]+=+|\Z)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)

    if match:
        return match.group(1).strip()

    return ""


def generate_content(summaries):
    """
    Generates all YouTube assets in ONE Gemini request
    and returns them as a dictionary.
    """

    prompt = f"""
You are an expert cybersecurity YouTube creator.

Using the news summaries below generate:

========================
YOUTUBE SCRIPT
========================

Requirements:
- 5–8 minute script
- Strong hook
- Explain every story
- Smooth transitions
- Professional tone
- End with:
Subscribe for daily cybersecurity news.

========================
SEO TITLE
========================

One highly clickable YouTube title.

========================
DESCRIPTION
========================

SEO-friendly YouTube description.

========================
TAGS
========================

20 comma-separated YouTube tags.

========================
SHORTS SCRIPT
========================

45–60 second Shorts script.

========================
THUMBNAIL PROMPT
========================

Detailed AI thumbnail prompt.

Return ONLY these sections.

News Summaries:

{summaries}
"""

    print("\n🎬 Generating complete content package...\n")

    response = ask_gemini(prompt)

    return {
        "raw": response,
        "script": extract_section(response, "YOUTUBE SCRIPT"),
        "seo_title": extract_section(response, "SEO TITLE"),
        "description": extract_section(response, "DESCRIPTION"),
        "tags": extract_section(response, "TAGS"),
        "shorts": extract_section(response, "SHORTS SCRIPT"),
        "thumbnail_prompt": extract_section(response, "THUMBNAIL PROMPT"),
    }