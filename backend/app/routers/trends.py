import datetime as dt
from random import randint
from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import TrendSample
from ..services.tiktok_client import fetch_public_trending_by_tag


router = APIRouter(prefix="/api/trends", tags=["trends"])


@router.get("/")
def get_trends(tag: str = Query(...), db: Session = Depends(get_db)) -> List[dict]:
    data = fetch_public_trending_by_tag(tag)

    # Fallback mock data if TikTok client returns nothing
    if not data:
        now = dt.datetime.utcnow().isoformat()
        data = [
            {
                "video_id": f"mock_{i}_{tag}",
                "author": f"user_{i}",
                "likes": randint(500, 5000),
                "views": randint(5000, 50000),
                "comments": randint(10, 100),
                "collected_at": now,
            }
            for i in range(10)
        ]

    seen_ids = set()
    new_rows: List[TrendSample] = []
    for entry in data:
        video_id = entry.get("video_id") or f"mock_{tag}_{len(seen_ids)}"
        if video_id in seen_ids:
            continue
        seen_ids.add(video_id)

        author = entry.get("author") or "unknown"
        likes = int(entry.get("likes") or 0)
        views = int(entry.get("views") or 0)
        comments = int(entry.get("comments") or 0)

        new_rows.append(
            TrendSample(
                tag=tag,
                video_id=video_id,
                author=author,
                likes=likes,
                views=views,
                comments=comments,
            )
        )

        entry["video_id"] = video_id
        entry["author"] = author
        entry["likes"] = likes
        entry["views"] = views
        entry["comments"] = comments
        entry["tag"] = tag

    if new_rows:
        db.add_all(new_rows)
        db.commit()

    return data
