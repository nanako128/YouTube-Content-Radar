from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db
from app.db.schemas import VideoRead, RankingRead
from app.services.ranking_service import ranking_service
from app.models import Video, Ranking, VideoMetrics
from sqlalchemy import select

router = APIRouter(prefix="/videos", tags=["videos"])

@router.get("/top-buzz", response_model=List[RankingRead])
async def get_top_buzz(db: AsyncSession = Depends(get_db)):
    results = await ranking_service.get_latest_rankings(db, "buzz")
    return [
        RankingRead(
            rank=r.Ranking.rank,
            score=r.Ranking.score,
            video=r.Video,
            metrics=r.Video.metrics
        ) for r in results
    ]

@router.get("/top-discussion", response_model=List[RankingRead])
async def get_top_discussion(db: AsyncSession = Depends(get_db)):
    results = await ranking_service.get_latest_rankings(db, "discussion")
    return [
        RankingRead(
            rank=r.Ranking.rank,
            score=r.Ranking.score,
            video=r.Video,
            metrics=r.Video.metrics
        ) for r in results
    ]

@router.get("/viral", response_model=List[RankingRead])
async def get_viral(db: AsyncSession = Depends(get_db)):
    results = await ranking_service.get_latest_rankings(db, "viral")
    return [
        RankingRead(
            rank=r.Ranking.rank,
            score=r.Ranking.score,
            video=r.Video,
            metrics=r.Video.metrics
        ) for r in results
    ]
