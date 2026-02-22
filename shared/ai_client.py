"""공통 Gemini AI 유틸리티."""
import os
import time
from google import genai

_MAX_RETRIES = 3
_RETRY_DELAY = 10  # seconds


def summarize(prompt: str) -> str:
    """Gemini 2.5 Flash로 텍스트를 생성합니다. 실패 시 최대 3회 재시도합니다."""
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
            print(f"⚠️  Gemini API 오류 (시도 {attempt}/{_MAX_RETRIES}): {e}")
            if attempt < _MAX_RETRIES:
                time.sleep(_RETRY_DELAY)

    raise RuntimeError(f"Gemini API 호출 {_MAX_RETRIES}회 모두 실패: {last_error}")
