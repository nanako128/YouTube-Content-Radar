from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func, Index
from sqlalchemy.orm import relationship
from app.db.database import Base

class Ranking(Base):
    __tablename__ = "rankings"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(20), nullable=False)  # buzz, discussion, viral
    video_id = Column(String(20), ForeignKey("videos.video_id"), nullable=False)
    rank = Column(Integer, nullable=False)
    score = Column(Float)
    ranked_at = Column(DateTime(timezone=True), server_default=func.now())

    video = relationship("Video", back_populates="rankings")

    __table_args__ = (
        Index('idx_rankings_type_date_rank', 'type', 'ranked_at', 'rank'),
    )
