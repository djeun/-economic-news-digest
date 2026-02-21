"""공통 RSS 피드 수집 유틸리티."""
import re
import feedparser


def fetch_feeds(urls: list[str], max_per_feed: int = 6, max_total: int = 15) -> list[dict]:
    """여러 RSS 피드에서 항목을 수집해 중복 제거 후 반환합니다."""
    items = []
    seen = set()

    for url in urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:max_per_feed]:
                title   = entry.get("title", "").strip()
                summary = entry.get("summary", entry.get("description", "")).strip()
                link    = entry.get("link", "")
                source  = feed.feed.get("title", "Unknown")

                if not title or not link or title in seen:
                    continue
                seen.add(title)

                summary = re.sub(r"<[^>]+>", "", summary)[:300]
                items.append({"title": title, "summary": summary, "url": link, "source": source})
        except Exception as e:
            print(f"⚠️  피드 오류 ({url}): {e}")

    return items[:max_total]
