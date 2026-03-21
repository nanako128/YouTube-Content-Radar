from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models import Video, VideoMetrics, Ranking
from app.config import settings
from datetime import datetime, timezone

class RankingService:
    @staticmethod
    async def generate_daily_rankings(db: AsyncSession):
        # ... (此處省略部分代碼，保持與原檔案一致)
        # (我會確保 generate_daily_rankings 保持不變，只增加 import 和修改 get_latest_rankings)
        now = datetime.now(timezone.utc)
        
        # Buzz Ranking
        buzz_stmt = (
            select(VideoMetrics)
            .order_by(desc(VideoMetrics.buzz_score))
            .limit(settings.MAX_RANKING_SIZE)
        )
        buzz_results = await db.execute(buzz_stmt)
        for i, metrics in enumerate(buzz_results.scalars().all()):
            ranking = Ranking(
                type="buzz",
                video_id=metrics.video_id,
                rank=i + 1,
                score=metrics.buzz_score,
                ranked_at=now
            )
            db.add(ranking)

        # Discussion Ranking
        disc_stmt = (
            select(VideoMetrics)
            .where(VideoMetrics.discussion_score.isnot(None))
            .order_by(desc(VideoMetrics.discussion_score))
            .limit(settings.MAX_RANKING_SIZE)
        )
        disc_results = await db.execute(disc_stmt)
        for i, metrics in enumerate(disc_results.scalars().all()):
            ranking = Ranking(
                type="discussion",
                video_id=metrics.video_id,
                rank=i + 1,
                score=metrics.discussion_score,
                ranked_at=now
            )
            db.add(ranking)

        # Viral Ranking
        viral_stmt = (
            select(VideoMetrics)
            .where(VideoMetrics.viral_spike == True)
            .order_by(desc(VideoMetrics.view_velocity))
            .limit(settings.MAX_RANKING_SIZE)
        )
        viral_results = await db.execute(viral_stmt)
        for i, metrics in enumerate(viral_results.scalars().all()):
            ranking = Ranking(
                type="viral",
                video_id=metrics.video_id,
                rank=i + 1,
                score=metrics.view_velocity,
                ranked_at=now
            )
            db.add(ranking)

        await db.commit()

    @staticmethod
    async def get_latest_rankings(db: AsyncSession, ranking_type: str, limit: int = 50):
        # Find latest ranked_at for this type
        latest_stmt = (
            select(func.max(Ranking.ranked_at))
            .where(Ranking.type == ranking_type)
        )
        latest_res = await db.execute(latest_stmt)
        latest_time = latest_res.scalar()
        
        if not latest_time:
            return []

        stmt = (
            select(Ranking, Video)
            .join(Video, Ranking.video_id == Video.video_id)
            .options(selectinload(Video.metrics))
            .where(Ranking.type == ranking_type, Ranking.ranked_at == latest_time)
            .order_by(Ranking.rank)
            .limit(limit)
        )
        results = await db.execute(stmt)
        return results.all()

ranking_service = RankingService()
