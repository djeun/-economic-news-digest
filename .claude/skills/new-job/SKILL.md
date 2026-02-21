---
name: new-job
description: 새 자동화 job을 스캐폴딩합니다. job 이름을 인자로 받아 폴더, 스크립트, 워크플로 파일을 생성합니다.
disable-model-invocation: true
allowed-tools: Read, Write, Glob
argument-hint: [job_name]
---

새 자동화 job `$ARGUMENTS`를 아래 절차에 따라 생성하세요.

## 1. 사전 확인

- CLAUDE.md를 읽어 프로젝트 규칙(무료 서비스 목록, 코드 구조)을 확인한다.
- `jobs/$ARGUMENTS/` 폴더가 이미 존재하면 중단하고 사용자에게 알린다.

## 2. 생성할 파일

### `jobs/$ARGUMENTS/main.py`

아래 템플릿을 그대로 사용하되, 주석의 `{job_name}`을 `$ARGUMENTS`로 치환한다.

```python
import os
import smtplib
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import feedparser
import google.generativeai as genai

# ── 환경변수 ──────────────────────────────────────────────────────────────────
GEMINI_API_KEY  = os.environ["GEMINI_API_KEY"]
GMAIL_USER      = os.environ["GMAIL_USER"]
GMAIL_APP_PASS  = os.environ["GMAIL_APP_PASSWORD"]
RECIPIENT_EMAIL = os.environ["RECIPIENT_EMAIL"]

# TODO: 이 job에 필요한 RSS 피드 URL을 추가하세요 (무료만)
RSS_FEEDS: list[str] = []


def fetch_data() -> list[dict]:
    """RSS 피드에서 데이터를 수집합니다."""
    items = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            items.append({
                "title":   entry.get("title", ""),
                "summary": entry.get("summary", "")[:300],
                "url":     entry.get("link", ""),
                "source":  feed.feed.get("title", ""),
            })
    return items[:12]


def process(items: list[dict]) -> str:
    """Gemini AI로 내용을 요약합니다."""
    today = datetime.now(timezone.utc).strftime("%Y년 %m월 %d일")
    content = "\n\n".join(
        f"[{i+1}] {a['title']}\n{a['summary']}"
        for i, a in enumerate(items)
    )
    # TODO: 프롬프트를 이 job의 목적에 맞게 수정하세요
    prompt = f"오늘({today})의 내용을 한국어로 요약해주세요:\n\n{content}"

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    return model.generate_content(prompt).text


def notify(html_body: str) -> None:
    """Gmail SMTP로 이메일을 발송합니다."""
    today = datetime.now(timezone.utc).strftime("%m/%d")
    # TODO: 제목을 이 job에 맞게 수정하세요
    subject = f"[{today}] 자동 브리핑"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = GMAIL_USER
    msg["To"]      = RECIPIENT_EMAIL
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_APP_PASS)
        server.sendmail(GMAIL_USER, RECIPIENT_EMAIL, msg.as_string())
    print(f"✅ 발송 완료 → {RECIPIENT_EMAIL}")


def main():
    print("📡 데이터 수집 중...")
    items = fetch_data()
    if not items:
        print("❌ 수집된 항목 없음")
        return
    print(f"   {len(items)}건 수집 완료")

    print("🤖 AI 요약 중...")
    summary = process(items)

    print("📧 이메일 발송 중...")
    notify(summary)


if __name__ == "__main__":
    main()
```

### `.github/workflows/$ARGUMENTS.yml`

```yaml
name: {$ARGUMENTS 작업 이름}

on:
  schedule:
    - cron: "0 23 * * *"   # 매일 08:00 KST
  workflow_dispatch:

jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"
      - run: pip install -r requirements.txt
      - run: python jobs/$ARGUMENTS/main.py
        env:
          GEMINI_API_KEY:     ${{ secrets.GEMINI_API_KEY }}
          GMAIL_USER:         ${{ secrets.GMAIL_USER }}
          GMAIL_APP_PASSWORD: ${{ secrets.GMAIL_APP_PASSWORD }}
          RECIPIENT_EMAIL:    ${{ secrets.RECIPIENT_EMAIL }}
```

## 3. PLAN.md 업데이트

Phase 2 섹션에 아래 항목을 추가한다:

```
- [ ] $ARGUMENTS job 구현 (`jobs/$ARGUMENTS/`)
```

## 4. PROGRESS.md 업데이트

`대기 중` 섹션에 추가:

```
- $ARGUMENTS job 생성됨 (main.py, workflow 스캐폴딩 완료 — TODO 채워야 함)
```

## 5. 완료 후 안내

생성된 파일 목록과 함께, 사용자가 채워야 할 TODO 항목을 알려준다:
- `RSS_FEEDS` 리스트에 수집할 URL 추가
- 프롬프트를 목적에 맞게 수정
- 이메일 제목 수정
