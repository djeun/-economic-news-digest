# RSS 피드 지식 베이스

검증된 무료 RSS 피드 목록입니다. API 키 불필요, 완전 무료입니다.
새 항목 추가 시 반드시 직접 접속해서 동작 확인 후 `검증` 열을 ✅로 표시하세요.

---

## 경제 / 비즈니스

| 이름 | URL | 언어 | 검증 | 추가일 | 비고 |
|------|-----|------|------|--------|------|
| CNBC Business | `https://www.cnbc.com/id/10001147/device/rss/rss.html` | EN | ✅ | 2026-02-21 | 실시간, 광범위 |
| MarketWatch | `https://feeds.content.dowjones.io/public/rss/mw_bulletins` | EN | ✅ | 2026-02-21 | 시황 중심 |
| Google News (US Economy) | `https://news.google.com/rss/search?q=US+economy+market&hl=en-US&gl=US&ceid=US:en` | EN | ✅ | 2026-02-21 | 키워드 변경 가능 |

## 테크

| 이름 | URL | 언어 | 검증 | 추가일 | 비고 |
|------|-----|------|------|--------|------|
| Hacker News Top | `https://news.ycombinator.com/rss` | EN | ✅ | 2026-02-21 | 개발자 커뮤니티 |
| Google News (Tech) | `https://news.google.com/rss/search?q=technology&hl=en-US&gl=US&ceid=US:en` | EN | ✅ | 2026-02-21 | 키워드 변경 가능 |

## 사용법 (feedparser)

```python
import feedparser

feed = feedparser.parse("https://www.cnbc.com/id/10001147/device/rss/rss.html")
for entry in feed.entries[:5]:
    print(entry.title)
    print(entry.link)
    print(entry.get("summary", ""))
```

## Google News RSS URL 패턴

키워드만 바꿔서 어떤 주제든 사용 가능:

```
https://news.google.com/rss/search?q={키워드}&hl=en-US&gl=US&ceid=US:en
https://news.google.com/rss/search?q={키워드}&hl=ko&gl=KR&ceid=KR:ko   ← 한국어
```
