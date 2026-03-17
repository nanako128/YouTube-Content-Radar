from celery import Celery
from app.config import settings
import asyncio
from app.db.database import AsyncSessionLocal
from app.services.discovery_engine import discovery_engine

celery_app = Celery("content_radar", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

@celery_app.task(name="app.tasks.crawl_tasks.daily_channel_crawl")
def daily_channel_crawl_task():
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # This shouldn't happen in a worker usually
        asyncio.create_task(run_crawl())
    else:
        loop.run_until_complete(run_crawl())

async def run_crawl():
    async with AsyncSessionLocal() as db:
        await discovery_engine.daily_channel_crawl(db)

# Beat schedule
celery_app.conf.beat_schedule = {
    "daily-crawl": {
        "task": "app.tasks.crawl_tasks.daily_channel_crawl",
        "schedule": 86400.0, # Every 24 hours
    },
}
