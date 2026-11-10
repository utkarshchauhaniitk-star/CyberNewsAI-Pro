def remove_duplicates(articles):
    """
    Remove duplicate news articles based on title and canonical URL.
    Safely handles missing keys, whitespace, and non-dict records.
    """
    seen_titles = set()
    seen_links = set()
    unique = []

    for article in articles:
        if not isinstance(article, dict):
            continue

        raw_title = article.get("title")
        if not raw_title or not isinstance(raw_title, str):
            continue

        title = raw_title.strip().lower()
        raw_link = article.get("link")
        link = raw_link.strip().lower() if isinstance(raw_link, str) else ""

        # Check if already seen by title or link
        if title in seen_titles:
            continue
        if link and link in seen_links:
            continue

        seen_titles.add(title)
        if link:
            seen_links.add(link)

        unique.append(article)

    return unique
