"""공통 Gemini AI 유틸리티."""
import os
import google.generativeai as genai


def summarize(prompt: str) -> str:
    """Gemini 1.5 Flash로 텍스트를 생성합니다."""
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
    return model.generate_content(prompt).text
