"""공통 RSS 피드 수집 유틸리티."""
import re
import time
import feedparser

_MAX_RETRIES = 3
_RETRY_DELAY = 5  # seconds


def fetch_feeds(urls: list[str], max_per_feed: int = 6, max_total: int = 15) -> list[dict]:
    """여러 RSS 피드에서 항목을 수집해 중복 제거 후 반환합니다. 피드별 최대 3회 재시도합니다."""
    items = []
    seen = set()

    for url in urls:
        entries = _fetch_with_retry(url)
        for entry in entries[:max_per_feed]:
            title   = entry.get("title", "").strip()
            summary = entry.get("summary", entry.get("description", "")).strip()
            link    = entry.get("link", "")
            source  = entry.get("_source", "Unknown")

            if not title or not link or title in seen:
                continue
            seen.add(title)

            summary = re.sub(r"<[^>]+>", "", summary)[:300]
            items.append({"title": title, "summary": summary, "url": link, "source": source})

    return items[:max_total]


def _fetch_with_retry(url: str) -> list:
    """단일 RSS 피드를 최대 3회 재시도하며 파싱합니다."""
    last_error = None
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            feed = feedparser.parse(url)
            if feed.bozo and not feed.entries:
                raise ValueError(f"피드 파싱 실패: {feed.bozo_exception}")
            # 각 entry에 source 정보 추가
            source = feed.feed.get("title", "Unknown")
            for entry in feed.entries:
                entry["_source"] = source
            return feed.entries
        except Exception as e:
            last_error = e
            print(f"⚠️  피드 오류 ({url}) 시도 {attempt}/{_MAX_RETRIES}: {e}")
            if attempt < _MAX_RETRIES:
                time.sleep(_RETRY_DELAY)

    print(f"❌ 피드 수집 최종 실패, 건너뜀: {url}")
    return []
