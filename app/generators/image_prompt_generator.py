from app.ai.gemini_client import ask_gemini


def generate_image_prompts(script):

    prompt = f"""
You are an expert cinematic AI prompt engineer.

Using the following YouTube cybersecurity script, create image prompts.

Rules:

- Create one prompt for every scene.
- Around 10-15 scenes.
- Ultra realistic.
- Cinematic lighting.
- High detail.
- 8K quality.
- No text in image.
- No watermark.
- Keep prompts descriptive.

Script:

{script}

Return only image prompts.

Example:

Scene 1:
A hacker sitting in a dark room,
multiple monitors,
green code,
cinematic lighting,
ultra realistic,
8K.

Scene 2:
Microsoft Windows logo breaking apart,
red cyber warning,
dramatic lighting,
high detail.

...
"""

    return ask_gemini(prompt)