# Job 구현 패턴 및 교훈

실제 job을 만들면서 발견한 패턴, 주의사항, 재사용 가능한 코드 조각을 기록합니다.

---

## 패턴: fetch → process → notify

모든 job은 이 3단계 구조를 따릅니다.

```python
def fetch_data() -> list[dict]:   # 외부에서 데이터 수집
def process(data) -> str:         # Gemini로 가공
def notify(content: str) -> None: # Gmail로 발송
def main(): ...
```

---

## 패턴: RSS 피드 중복 제거

여러 RSS 피드를 합칠 때 제목 기준 중복 제거:

```python
seen = set()
for feed_url in RSS_FEEDS:
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        if entry.title not in seen:
            seen.add(entry.title)
            articles.append(...)
```

---

## 패턴: HTML 이메일 기본 구조

재사용 가능한 HTML 이메일 레이아웃:

```python
def build_email(body_html: str, title: str) -> str:
    today = datetime.now(timezone.utc).strftime("%Y년 %m월 %d일")
    return f"""<!DOCTYPE html><html lang="ko"><head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width,initial-scale=1">
    </head><body style="background:#f5f5f5;font-family:Arial,sans-serif;">
      <table width="620" style="background:#fff;margin:20px auto;border-radius:12px;">
        <tr><td style="background:#1a237e;padding:24px;text-align:center;">
          <h1 style="color:#fff;margin:0;">{title}</h1>
          <p style="color:#90caf9;margin:8px 0 0;">{today}</p>
        </td></tr>
        <tr><td style="padding:28px;color:#333;line-height:1.8;">{body_html}</td></tr>
      </table>
    </body></html>"""
```

---

## 주의사항

| 상황 | 문제 | 해결 |
|------|------|------|
| RSS 피드 응답 없음 | feedparser가 빈 feed 반환 | `if not feed.entries: continue` |
| Gemini 속도 제한 | 429 에러 | 분당 15건 제한, job당 1~2회만 호출 |
| Gmail 발송 실패 | 앱 비밀번호 오류 | 2단계 인증 활성화 여부 재확인 |
| HTML 태그 섞임 | summary에 `<p>` 등 포함 | `re.sub(r"<[^>]+>", "", text)` |
