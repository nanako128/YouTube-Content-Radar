from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import BaseModel
from app.db.database import get_db
from app.models import Keyword
from sqlalchemy import select

router = APIRouter(prefix="/keywords", tags=["keywords"])

class KeywordBase(BaseModel):
    term: str
    is_active: bool = True

class KeywordCreate(KeywordBase):
    pass

class KeywordRead(KeywordBase):
    id: int

    class Config:
        from_attributes = True

@router.get("", response_model=List[KeywordRead])
async def list_keywords(db: AsyncSession = Depends(get_db)):
    stmt = select(Keyword)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("", response_model=KeywordRead)
async def create_keyword(kw: KeywordCreate, db: AsyncSession = Depends(get_db)):
    keyword = Keyword(term=kw.term, is_active=kw.is_active)
    db.add(keyword)
    try:
        await db.commit()
        await db.refresh(keyword)
        return keyword
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Keyword already exists or invalid data")

@router.delete("/{keyword_id}")
async def delete_keyword(keyword_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Keyword).where(Keyword.id == keyword_id)
    result = await db.execute(stmt)
    keyword = result.scalar()
    if not keyword:
        raise HTTPException(status_code=404, detail="Keyword not found")
    await db.delete(keyword)
    await db.commit()
    return {"message": "Keyword deleted"}
