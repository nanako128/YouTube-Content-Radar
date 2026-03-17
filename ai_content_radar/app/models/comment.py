from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String(20), ForeignKey("videos.video_id"), nullable=False, index=True)
    comment_id = Column(String(50), unique=True, nullable=False)
    comment_text = Column(Text, nullable=False)
    like_count = Column(Integer, default=0)
    sentiment = Column(String(10))
    sentiment_score = Column(Float)
    is_debate = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True))
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())

    video = relationship("Video", back_populates="comments")
