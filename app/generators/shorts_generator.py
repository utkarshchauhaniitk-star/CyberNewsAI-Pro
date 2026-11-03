from app.ai.gemini_client import ask_gemini


def generate_shorts(script):
    prompt = f"""
You are a viral YouTube Shorts creator.

Using this cybersecurity script, create:

- A 45-60 second YouTube Shorts script.
- Start with a strong hook.
- Keep the pace fast.
- End with:
"Follow for daily cybersecurity updates."

Video Script:

{script}

Return only the Shorts script.
"""

    return ask_gemini(prompt)