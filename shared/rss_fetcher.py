"""Shared RSS feed fetching utility."""
import re
import time
import feedparser

_MAX_RETRIES = 3
_RETRY_DELAY = 5  # seconds


def fetch_feeds(urls: list[str], max_per_feed: int = 6, max_total: int = 15) -> list[dict]:
    """Fetch items from multiple RSS feeds, deduplicate, and return a flat list. Retries each feed up to 3 times."""
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
    """Parse a single RSS feed with up to 3 retries. Returns an empty list on final failure."""
    last_error = None
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            feed = feedparser.parse(url)
            if feed.bozo and not feed.entries:
                raise ValueError(f"Feed parse failed: {feed.bozo_exception}")
            source = feed.feed.get("title", "Unknown")
            for entry in feed.entries:
                entry["_source"] = source
            return feed.entries
        except Exception as e:
            last_error = e
            print(f"[WARN] Feed error ({url}) attempt {attempt}/{_MAX_RETRIES}: {e}")
            if attempt < _MAX_RETRIES:
                time.sleep(_RETRY_DELAY)

    print(f"[ERROR] Feed permanently failed, skipping: {url}")
    return []
