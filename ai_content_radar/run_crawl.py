import asyncio
from app.db.database import AsyncSessionLocal
from app.services.discovery_engine import discovery_engine

async def main():
    print("Starting manual crawl and analysis...")
    async with AsyncSessionLocal() as db:
        try:
            # Run the daily channel crawl (which also analyzes discussions)
            await discovery_engine.daily_channel_crawl(db)
            print("Crawl completed successfully!")
        except Exception as e:
            print(f"An error occurred during crawl: {e}")

if __name__ == "__main__":
    asyncio.run(main())
