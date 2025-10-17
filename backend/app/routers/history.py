from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import TrendSample

router = APIRouter(prefix="/api/trends", tags=["history"])

@router.get("/history")
def get_history(
    tag: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """
    Retrieve recent trend samples from the database.
    - Optionally filter by tag.
    - Limit to last N records (default 50).
    """
    q = db.query(TrendSample)
    if tag:
        q = q.filter(TrendSample.tag == tag)
    q = q.order_by(TrendSample.collected_at.desc()).limit(limit)
    rows = q.all()

    return [
        {
            "id": r.id,
            "tag": r.tag,
            "video_id": r.video_id,
            "author": r.author,
            "likes": r.likes,
            "views": r.views,
            "comments": r.comments,
            "collected_at": r.collected_at.isoformat() if r.collected_at else None,
        }
        for r in rows
    ]
