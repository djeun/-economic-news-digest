"""Global tech news briefing — sends email daily at 08:00 PST."""
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

# Add project root to import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from shared.rss_fetcher import fetch_feeds
from shared.ai_client import summarize
from shared.email_sender import send_html_email

RSS_FEEDS = [
    "https://news.ycombinator.com/rss",
    "https://feeds.feedburner.com/TechCrunch",
    "https://www.theverge.com/rss/index.xml",
]


def fetch_data() -> list[dict]:
    return fetch_feeds(RSS_FEEDS)


def process(articles: list[dict]) -> str:
    today = datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%Y년 %m월 %d일")
    news_text = "\n\n".join(
        f"[{i+1}] {a['title']}\n출처: {a['source']}\n내용: {a['summary']}"
        for i, a in enumerate(articles)
    )
    prompt = f"""오늘은 {today}입니다.
아래는 오늘의 글로벌 테크 뉴스 {len(articles)}건입니다.

{news_text}

위 뉴스를 바탕으로 한국어 이메일 뉴스레터 본문을 HTML 형식으로 작성해주세요.
아래 3개 섹션을 포함하세요:

1. <h2>🔥 오늘의 핵심 테크 트렌드</h2> (전체 동향을 3~4문장으로 요약)
2. <h2>💻 주요 뉴스</h2> (각 뉴스를 이모지와 함께 2~3문장으로 설명, <ul><li> 형식)
3. <h2>🚀 개발자 포인트</h2> (개발자·기술인에게 실용적인 시사점 3가지, <ol><li> 형식)

주의사항:
- 한국어로만 작성
- HTML 태그만 사용 (```html 같은 코드 블록 마커 금지)
- 인라인 스타일 불필요 (외부에서 적용)"""
    return summarize(prompt)


def notify(summary_html: str, articles: list[dict]) -> None:
    today = datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%Y년 %m월 %d일")
    mmdd  = datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%m/%d")

    links_html = "".join(
        f'<li><a href="{a["url"]}" style="color:#1a73e8;">{a["title"]}</a>'
        f' <span style="color:#888;font-size:12px;">({a["source"]})</span></li>'
        for a in articles
    )

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <style>
    body {{ margin:0; padding:0; background:#f5f5f5;
           font-family:'Apple SD Gothic Neo',Arial,sans-serif; }}
    h2   {{ color:#1b5e20; font-size:17px; margin-top:24px; }}
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
        <tr><td style="background:linear-gradient(135deg,#1b5e20,#388e3c);
                        padding:28px 32px;text-align:center;">
          <h1 style="margin:0;color:#fff;font-size:22px;">💻 글로벌 테크 뉴스 브리핑</h1>
          <p style="margin:8px 0 0;color:#a5d6a7;font-size:14px;">
            {today} · Powered by Gemini AI (무료)
          </p>
        </td></tr>
        <tr><td style="padding:28px 32px;color:#333;font-size:15px;line-height:1.8;">
          {summary_html}
        </td></tr>
        <tr><td style="padding:0 32px 28px;">
          <h3 style="color:#555;font-size:13px;text-transform:uppercase;
                     letter-spacing:1px;border-top:1px solid #eee;padding-top:20px;">
            📎 원문 기사 링크
          </h3>
          <ul style="padding-left:18px;margin:0;font-size:13px;line-height:2.2;">
            {links_html}
          </ul>
        </td></tr>
        <tr><td style="background:#f8f9fa;padding:16px 32px;text-align:center;
                        color:#999;font-size:12px;border-top:1px solid #eee;">
          자동 발송 이메일 · RSS + Google Gemini (무료) + GitHub Actions
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""

    send_html_email(f"[{mmdd}] 오늘의 글로벌 테크 뉴스 브리핑 💻", html)


def main():
    print("Fetching RSS news...")
    articles = fetch_data()
    if not articles:
        print("[ERROR] No articles collected.")
        return
    print(f"  {len(articles)} articles collected")

    print("Generating summary with Gemini AI...")
    summary_html = process(articles)

    print("Sending email...")
    notify(summary_html, articles)


if __name__ == "__main__":
    main()
