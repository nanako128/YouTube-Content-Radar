import asyncio
from app.db.database import engine, Base
from app.models.channel import Channel
from app.models.video import Video
from app.models.comment import Comment
from app.models.keyword import Keyword
from app.models.metrics import VideoMetrics
from app.models.ranking import Ranking

async def init_db():
    print("Connecting to database and creating tables...")
    async with engine.begin() as conn:
        # This will create all tables defined in models
        await conn.run_sync(Base.metadata.create_all)
    print("Database initialized successfully!")

if __name__ == "__main__":
    asyncio.run(init_db())
