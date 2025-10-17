from fastapi import APIRouter, Query
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import TrendSample  # ✅ unified import
from ..services.tiktok_client import fetch_public_trending_by_tag
import datetime as dt
from random import randint


router = APIRouter(prefix="/api/trends", tags=["trends"])

@router.get("/")
def get_trends(tag: str = Query(...)):
    data = fetch_public_trending_by_tag(tag)

    # Fallback mock data if TikTok client returns nothing
    if not data or len(data) == 0:
        data = [
            {
                "video_id": f"mock_{i}_{tag}",
                "author": f"user_{i}",
                "likes": randint(500, 5000),
                "views": randint(5000, 50000),
                "comments": randint(10, 100),
                "collected_at": dt.datetime.utcnow().isoformat(),
            }
            for i in range(10)
        ]

    # ✅ Persist to Postgres
    db: Session = SessionLocal()
    for d in data:
        db.add(
            TrendSample(
                tag=tag,
                video_id=d["video_id"],
                author=d["author"],
                likes=d["likes"],
                views=d["views"],
                comments=d["comments"],
            )
        )
    db.commit()
    db.close()

    return data
