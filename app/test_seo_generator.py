from app.generators.seo_generator import generate_seo

sample = """
Microsoft released an emergency security update.

Oracle servers are under attack.

A ransomware campaign is spreading worldwide.
"""

result = generate_seo(sample)

print(result)