from app.processors.ranker import rank_news

sample_news = """
Microsoft emergency Windows patch
Oracle servers under attack
New ransomware campaign spreading
Apple releases Safari update
Cisco fixes VPN vulnerability
Google Chrome zero-day
Fortinet firewall exploit
"""

print(rank_news(sample_news))