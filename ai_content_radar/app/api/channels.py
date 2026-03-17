from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db
from app.db.schemas import ChannelRead
from app.models import Channel
from sqlalchemy import select

router = APIRouter(prefix="/channels", tags=["channels"])

@router.get("", response_model=List[ChannelRead])
async def list_channels(db: AsyncSession = Depends(get_db)):
    stmt = select(Channel).order_by(Channel.name)
    result = await db.execute(stmt)
    return result.scalars().all()
