def remove_duplicates(articles):
    """
    Remove duplicate news articles based on title.
    """

    seen = set()
    unique = []

    for article in articles:
        title = article["title"].strip().lower()

        if title not in seen:
            seen.add(title)
            unique.append(article)

    return unique