from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.database import Base

class VideoMetrics(Base):
    __tablename__ = "video_metrics"

    video_id = Column(String(20), ForeignKey("videos.video_id"), primary_key=True)
    buzz_score = Column(Float)
    discussion_score = Column(Float)
    clip_score = Column(Float)
    view_velocity = Column(Float)
    engagement_rate = Column(Float)
    fresh_score = Column(Float)
    comment_density = Column(Float)
    comment_velocity = Column(Float)
    debate_ratio = Column(Float)
    sentiment_conflict = Column(Float)
    viral_spike = Column(Boolean, default=False)
    scored_at = Column(DateTime(timezone=True), server_default=func.now())

    video = relationship("Video", back_populates="metrics")
