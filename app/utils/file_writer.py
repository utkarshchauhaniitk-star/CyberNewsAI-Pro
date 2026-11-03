import os


def save_text(filename, text):
    """
    Save text to a file.
    Creates the folder automatically if it doesn't exist.
    """

    folder = os.path.dirname(filename)

    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)