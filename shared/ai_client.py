"""Shared Gemini AI utility."""
import os
import time
from google import genai

_MAX_RETRIES = 3
_RETRY_DELAY = 10  # seconds


def summarize(prompt: str) -> str:
    """Generate text using Gemini 2.5 Flash. Retries up to 3 times on failure."""
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    last_error = None

    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            return response.text
        except Exception as e:
            last_error = e
            print(f"[WARN] Gemini API error (attempt {attempt}/{_MAX_RETRIES}): {e}")
            if attempt < _MAX_RETRIES:
                time.sleep(_RETRY_DELAY)

    raise RuntimeError(f"Gemini API failed after {_MAX_RETRIES} attempts: {last_error}")
