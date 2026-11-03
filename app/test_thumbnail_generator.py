from app.generators.thumbnail_generator import generate_thumbnail

script = """
Microsoft has released an emergency security update after hackers exploited a critical Windows vulnerability affecting millions of users worldwide.
"""

print(generate_thumbnail(script))