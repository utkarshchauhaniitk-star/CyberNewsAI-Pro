from app.ai.gemini_client import ask_gemini


def generate_thumbnail(script):

    prompt = f"""
You are an expert YouTube thumbnail designer.

Using this cybersecurity video script, generate:

1. One catchy thumbnail title (3-6 words)
2. One short thumbnail text (2-4 words)
3. A detailed AI image prompt for creating the thumbnail.

Video Script:

{script}

Return exactly like this:

Thumbnail Title:
...

Thumbnail Text:
...

AI Image Prompt:
...
"""

    return ask_gemini(prompt)