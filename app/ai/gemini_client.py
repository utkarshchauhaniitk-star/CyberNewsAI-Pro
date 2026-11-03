import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError, ServerError

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in .env file."
    )

client = genai.Client(api_key=API_KEY)

MODEL = "models/gemini-3.5-flash"


def ask_gemini(prompt, retries=5):
    """
    Send a prompt to Gemini with automatic retry.
    """

    delay = 2

    for attempt in range(1, retries + 1):

        try:

            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )

            return response.text

        except (ClientError, ServerError) as e:

            print(f"\nGemini Error ({attempt}/{retries})")
            print(e)

            if attempt == retries:
                raise

            print(f"Retrying in {delay} seconds...\n")

            time.sleep(delay)

            delay *= 2