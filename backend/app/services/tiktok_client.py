import httpx, datetime as dt, asyncio
from typing import List, Dict

# base public trending endpoint (no login required)
TRENDING_FEED = "https://www.tiktok.com/api/discover/item_list/"

# respect robots.txt: ~1 req / 5 s
RATE_LIMIT_SECONDS = 5

async def _fetch_public_trending(tag: str, limit: int = 10) -> List[Dict]:
    """Fetch trending TikTok videos for a tag using the public JSON feed."""
    params = {"aid": "1988", "count": limit, "keyword": tag}
    headers = {
        "User-Agent": "TrendLensBot/1.0 (+https://trendlens.io; contact@trendlens.io)",
        "Referer": f"https://www.tiktok.com/tag/{tag}",
        "Accept": "application/json, text/javascript",
    }

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            r = await client.get(TRENDING_FEED, params=params, headers=headers)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            print("Fetch error:", e)
            return []

    now = dt.datetime.utcnow()
    videos = []
    for item in data.get("itemList", []):
        stats = item.get("stats", {})
        author = item.get("author", {}).get("uniqueId", "unknown")
        videos.append({
            "video_id": item.get("id"),
            "author": author,
            "likes": stats.get("diggCount", 0),
            "views": stats.get("playCount", 0),
            "comments": stats.get("commentCount", 0),
            "collected_at": now.isoformat()
        })
    return videos

# Public sync wrapper for FastAPI routes
def fetch_public_trending_by_tag(tag: str, limit: int = 10) -> List[Dict]:
    """Sync wrapper used by FastAPI endpoints."""
    return asyncio.run(_fetch_public_trending(tag, limit))
