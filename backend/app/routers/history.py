from fastapi import APIRouter, Query
from sqlalchemy.orm import Session
from typing import Optional
from ..db import SessionLocal
from ..models import TrendSample  # ✅ unified import (not ..models.trend_sample)

router = APIRouter(prefix="/api/trends", tags=["history"])

@router.get("/history")
def get_history(
    tag: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=500)
):
    """
    Retrieve recent trend samples from the database.
    - Optionally filter by tag.
    - Limit to last N records (default 50).
    """
    db: Session = SessionLocal()
    q = db.query(TrendSample)
    if tag:
        q = q.filter(TrendSample.tag == tag)
    q = q.order_by(TrendSample.collected_at.desc()).limit(limit)
    rows = q.all()
    db.close()

    return [
        {
            "id": r.id,
            "tag": r.tag,
            "video_id": getattr(r, "video_id", None),
            "author": r.author,
            "likes": r.likes,
            "views": r.views,
            "comments": r.comments,
            "collected_at": r.collected_at.isoformat() if r.collected_at else None,
        }
        for r in rows
    ]
