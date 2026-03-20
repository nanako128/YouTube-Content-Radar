import asyncio
from app.db.database import engine
from app.config import settings

async def test_db():
    print(f"Connecting to: {settings.DATABASE_URL}")
    try:
        async with engine.connect() as conn:
            print("Successfully connected to the database!")
    except Exception as e:
        print(f"Failed to connect to the database: {e}")

if __name__ == "__main__":
    asyncio.run(test_db())
