"""GitHub 트렌딩 레포 브리핑 — 매일 08:00 PST 이메일 발송."""
import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from zoneinfo import ZoneInfo

_MAX_RETRIES = 3
_RETRY_DELAY = 5  # seconds

# 프로젝트 루트를 import 경로에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from shared.ai_client import summarize
from shared.email_sender import send_html_email


def fetch_data() -> list[dict]:
    """GitHub Trending 페이지에서 오늘의 트렌딩 레포를 스크래핑합니다. 실패 시 최대 3회 재시도합니다."""
    url = "https://github.com/trending"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; news-digest-bot/1.0)"}

    last_error = None
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            break
        except Exception as e:
            last_error = e
            print(f"⚠️  GitHub Trending 요청 오류 (시도 {attempt}/{_MAX_RETRIES}): {e}")
            if attempt < _MAX_RETRIES:
                time.sleep(_RETRY_DELAY)
    else:
        raise RuntimeError(f"GitHub Trending 수집 {_MAX_RETRIES}회 모두 실패: {last_error}")

    soup = BeautifulSoup(response.text, "html.parser")
    repos = []

    for article in soup.select("article.Box-row"):
        # 이름 & URL
        link_el = article.select_one("h2 a")
        if not link_el:
            continue
        parts = [p.strip() for p in link_el.get_text().split("/") if p.strip()]
        full_name = "/".join(parts)
        url_repo = "https://github.com" + link_el["href"].strip()

        # 설명
        desc_el = article.select_one("p")
        description = desc_el.get_text(strip=True) if desc_el else ""

        # 언어
        lang_el = article.select_one("[itemprop='programmingLanguage']")
        language = lang_el.get_text(strip=True) if lang_el else ""

        # 전체 스타
        star_el = article.select_one("a[href$='/stargazers']")
        total_stars = star_el.get_text(strip=True) if star_el else ""

        # 오늘 스타
        today_el = article.select_one("span.d-inline-block.float-sm-right")
        stars_today = today_el.get_text(strip=True) if today_el else ""

        repos.append({
            "name": full_name,
            "url": url_repo,
            "description": description,
            "language": language,
            "total_stars": total_stars,
            "stars_today": stars_today,
        })

    return repos[:15]


def process(repos: list[dict]) -> str:
    today = datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%Y년 %m월 %d일")
    repos_text = "\n\n".join(
        f"[{i+1}] {r['name']}\n"
        f"언어: {r['language'] or '미표시'} | 전체 스타: {r['total_stars']} | 오늘 스타: {r['stars_today']}\n"
        f"설명: {r['description'] or '설명 없음'}"
        for i, r in enumerate(repos)
    )
    prompt = f"""오늘은 {today}입니다.
아래는 오늘의 GitHub 트렌딩 레포지터리 {len(repos)}개입니다.

{repos_text}

위 내용을 바탕으로 한국어 이메일 뉴스레터 본문을 HTML 형식으로 작성해주세요.
아래 3개 섹션을 포함하세요:

1. <h2>🔥 오늘의 트렌드 요약</h2> (전체적인 기술 트렌드를 3~4문장으로 분석)
2. <h2>⭐ 주목할 레포지터리</h2> (상위 레포를 이모지와 함께 2~3문장으로 소개, <ul><li> 형식)
3. <h2>💡 개발자 인사이트</h2> (트렌드에서 읽을 수 있는 시사점 3가지, <ol><li> 형식)

주의사항:
- 한국어로만 작성
- HTML 태그만 사용 (```html 같은 코드 블록 마커 금지)
- 인라인 스타일 불필요 (외부에서 적용)"""
    return summarize(prompt)


def notify(summary_html: str, repos: list[dict]) -> None:
    today = datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%Y년 %m월 %d일")
    mmdd  = datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%m/%d")

    links_html = "".join(
        f'<li>'
        f'<a href="{r["url"]}" style="color:#1a73e8;">{r["name"]}</a>'
        f'<span style="color:#888;font-size:12px;"> · {r["language"]}</span>'
        f'<span style="color:#f9a825;font-size:12px;"> ★ {r["stars_today"]}</span>'
        f'</li>'
        for r in repos
    )

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <style>
    body {{ margin:0; padding:0; background:#f5f5f5;
           font-family:'Apple SD Gothic Neo',Arial,sans-serif; }}
    h2   {{ color:#4a148c; font-size:17px; margin-top:24px; }}
    ul, ol {{ padding-left:20px; line-height:1.9; }}
    li   {{ margin-bottom:6px; }}
    a    {{ color:#1a73e8; }}
  </style>
</head>
<body>
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f5f5;padding:20px 0;">
    <tr><td align="center">
      <table width="620" cellpadding="0" cellspacing="0"
             style="background:#fff;border-radius:12px;overflow:hidden;
                    box-shadow:0 2px 8px rgba(0,0,0,.1);">
        <tr><td style="background:linear-gradient(135deg,#4a148c,#7b1fa2);
                        padding:28px 32px;text-align:center;">
          <h1 style="margin:0;color:#fff;font-size:22px;">🐙 GitHub 트렌딩 브리핑</h1>
          <p style="margin:8px 0 0;color:#ce93d8;font-size:14px;">
            {today} · Powered by Gemini AI (무료)
          </p>
        </td></tr>
        <tr><td style="padding:28px 32px;color:#333;font-size:15px;line-height:1.8;">
          {summary_html}
        </td></tr>
        <tr><td style="padding:0 32px 28px;">
          <h3 style="color:#555;font-size:13px;text-transform:uppercase;
                     letter-spacing:1px;border-top:1px solid #eee;padding-top:20px;">
            📎 오늘의 트렌딩 레포 목록
          </h3>
          <ul style="padding-left:18px;margin:0;font-size:13px;line-height:2.2;">
            {links_html}
          </ul>
        </td></tr>
        <tr><td style="background:#f8f9fa;padding:16px 32px;text-align:center;
                        color:#999;font-size:12px;border-top:1px solid #eee;">
          자동 발송 이메일 · GitHub Trending + Google Gemini (무료) + GitHub Actions
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""

    send_html_email(f"[{mmdd}] 오늘의 GitHub 트렌딩 브리핑 🐙", html)


def main():
    print("📡 GitHub Trending 스크래핑 중...")
    repos = fetch_data()
    if not repos:
        print("❌ 수집된 레포가 없습니다.")
        return
    print(f"   {len(repos)}개 수집 완료")

    print("🤖 Gemini AI로 요약 생성 중...")
    summary_html = process(repos)

    print("📧 이메일 발송 중...")
    notify(summary_html, repos)


if __name__ == "__main__":
    main()
