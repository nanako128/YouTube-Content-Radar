from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_content_radar"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # YouTube API
    YOUTUBE_API_KEY: str
    
    # App Settings
    APP_NAME: str = "AI Content Radar"
    DEBUG: bool = False
    
    # Ranking thresholds
    MAX_RANKING_SIZE: int = 50
    TOP_VIDEOS_FOR_COMMENTS: int = 20
    MAX_COMMENTS_PER_VIDEO: int = 200

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
