from sqlalchemy import String, BigInteger, DateTime, func, Index
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

class TrendSample(Base):
    __tablename__ = "trend_samples"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tag: Mapped[str] = mapped_column(String(64), index=True)
    author: Mapped[str] = mapped_column(String(64))
    likes: Mapped[int] = mapped_column(BigInteger)
    views: Mapped[int] = mapped_column(BigInteger)
    comments: Mapped[int] = mapped_column(BigInteger)
    collected_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())

Index("ix_tag_time", TrendSample.tag, TrendSample.collected_at.desc())
