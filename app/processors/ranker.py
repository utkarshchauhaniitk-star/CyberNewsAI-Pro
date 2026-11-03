from app.ai.gemini_client import ask_gemini


def rank_articles(articles):
    """
    Uses Gemini to choose the 5 most important cybersecurity stories.
    Returns the corresponding article dictionaries.
    """

    titles = "\n".join(
        f"{i+1}. {article['title']}"
        for i, article in enumerate(articles)
    )

    prompt = f"""
You are a senior cybersecurity news editor.

Below are today's cybersecurity headlines.

Choose the FIVE most important stories based on:

• Global impact
• Severity
• Active exploitation
• Critical vulnerabilities
• Ransomware
• Nation-state attacks
• Major breaches

Return ONLY the five headlines.

Headlines:

{titles}
"""

    response = ask_gemini(prompt)

    print("\nTop Ranked Stories:\n")
    print(response)

    selected = []

    for line in response.splitlines():

        line = line.strip()

        if not line:
            continue

        # Remove numbering if Gemini adds it
        if ". " in line:
            line = line.split(". ", 1)[1]

        for article in articles:

            if article["title"].lower() == line.lower():

                print(f"✓ {article['title']}")

                selected.append(article)

                break

    return selected[:5]