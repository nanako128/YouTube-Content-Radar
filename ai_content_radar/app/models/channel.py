from sqlalchemy import Column, Integer, String, BigInteger, Float, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.db.database import Base

class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    subscriber_count = Column(BigInteger)
    uploads_playlist_id = Column(String(50))
    is_curated = Column(Boolean, default=False)
    avg_view_velocity = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_crawled_at = Column(DateTime(timezone=True))

    videos = relationship("Video", back_populates="channel")
