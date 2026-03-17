import asyncio
from app.db.database import AsyncSessionLocal
from app.models.channel import Channel
from sqlalchemy import select

CHANNELS = [
    {"channel_id": "UCX6OQ3DkcsbYNE6H8uQQuVA", "name": "MrBeast"},
    {"channel_id": "UCBJycsmduvYELg8Ga7gF2DQ", "name": "MKBHD"},
    {"channel_id": "UC0vBXGSyLwVGneZmE2jOdmQ", "name": "The Daily Show"},
    {"channel_id": "UCpwvOunYF_D8M9P6F3r6A7A", "name": "TechCrunch"},
    {"channel_id": "UCvXhM23U-lM_57vR89_j6jA", "name": "Lex Fridman"},
]

async def seed_channels():
    async with AsyncSessionLocal() as db:
        for ch in CHANNELS:
            stmt = select(Channel).where(Channel.channel_id == ch["channel_id"])
            res = await db.execute(stmt)
            if not res.scalar():
                channel = Channel(
                    channel_id=ch["channel_id"],
                    name=ch["name"],
                    is_curated=True,
                    avg_view_velocity=10000.0 # Seed with some base velocity
                )
                db.add(channel)
        await db.commit()
        print(f"Successfully seeded {len(CHANNELS)} channels.")

if __name__ == "__main__":
    asyncio.run(seed_channels())
