from app.ai.gemini_client import ask_gemini


def generate_script(summaries):
    prompt = f"""
You are a professional cybersecurity YouTube creator.

Create a 4-5 minute YouTube script from these cybersecurity news summaries.

Requirements:
- Start with an exciting hook.
- Explain each news item simply.
- Mention why it matters.
- End with a CTA asking viewers to Like, Share and Subscribe.
- Use conversational English.
- Do NOT use markdown.

News:

{summaries}
"""

    return ask_gemini(prompt)