"""공통 Gemini AI 유틸리티."""
import os
from google import genai


def summarize(prompt: str) -> str:
    """Gemini 2.0 Flash로 텍스트를 생성합니다."""
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt,
    )
    return response.text
