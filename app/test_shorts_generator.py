from app.generators.shorts_generator import generate_shorts

sample = """
Microsoft released an emergency Windows update.

Oracle servers are under attack.

Hackers are spreading ransomware worldwide.
"""

print(generate_shorts(sample))