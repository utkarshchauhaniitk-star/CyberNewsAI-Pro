from app.generators.script_generator import generate_script

sample = """
1. Microsoft released an emergency security update for Windows.

2. Hackers targeted Oracle servers worldwide.

3. A new ransomware campaign is spreading through phishing emails.
"""

script = generate_script(sample)

print(script)