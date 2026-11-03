from app.generators.image_prompt_generator import generate_image_prompts

script = """
Microsoft has released an emergency security update after hackers exploited
a zero-day vulnerability affecting millions of Windows users.
"""

print(generate_image_prompts(script))