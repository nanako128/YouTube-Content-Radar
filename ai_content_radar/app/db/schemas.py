from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class VideoBase(BaseModel):
    video_id: str
    title: str
    publish_time: datetime
    view_count: int
    like_count: int
    comment_count: int

class VideoRead(VideoBase):
    id: int
    channel_id: str
    description: Optional[str]
    tags: List[str] = []

    class Config:
        from_attributes = True

class VideoMetricsRead(BaseModel):
    buzz_score: float
    discussion_score: Optional[float]
    view_velocity: float
    engagement_rate: float
    fresh_score: float
    viral_spike: bool

    class Config:
        from_attributes = True

class RankingRead(BaseModel):
    rank: int
    score: float
    video: VideoRead
    metrics: Optional[VideoMetricsRead]

    class Config:
        from_attributes = True

class ChannelRead(BaseModel):
    channel_id: str
    name: str
    subscriber_count: Optional[int]
    is_curated: bool
    last_crawled_at: Optional[datetime]

    class Config:
        from_attributes = True
