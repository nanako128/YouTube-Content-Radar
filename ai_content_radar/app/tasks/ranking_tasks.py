from app.tasks.crawl_tasks import celery_app
import asyncio
from app.db.database import AsyncSessionLocal
from app.services.ranking_service import ranking_service

@celery_app.task(name="app.tasks.ranking_tasks.daily_ranking_generation")
def daily_ranking_generation_task():
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.create_task(run_ranking())
    else:
        loop.run_until_complete(run_ranking())

async def run_ranking():
    async with AsyncSessionLocal() as db:
        await ranking_service.generate_daily_rankings(db)

# Update beat schedule
celery_app.conf.beat_schedule.update({
    "daily-ranking": {
        "task": "app.tasks.ranking_tasks.daily_ranking_generation",
        "schedule": 86400.0, # Every 24 hours, should run AFTER crawl
    }
})
