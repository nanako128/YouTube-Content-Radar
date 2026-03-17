from sqlalchemy import Column, Integer, String, BigInteger, Text, DateTime, ForeignKey, func, ARRAY
from sqlalchemy.orm import relationship
from app.db.database import Base

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String(20), unique=True, nullable=False, index=True)
    channel_id = Column(String(50), ForeignKey("channels.channel_id"), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    duration = Column(Integer)  # in seconds
    publish_time = Column(DateTime(timezone=True), nullable=False, index=True)
    view_count = Column(BigInteger, default=0)
    like_count = Column(BigInteger, default=0)
    comment_count = Column(BigInteger, default=0)
    tags = Column(ARRAY(Text))
    language = Column(String(10))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    channel = relationship("Channel", back_populates="videos")
    metrics = relationship("VideoMetrics", back_populates="video", uselist=False)
    comments = relationship("Comment", back_populates="video")
    rankings = relationship("Ranking", back_populates="video")
