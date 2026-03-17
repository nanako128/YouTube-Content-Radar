from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, desc
from app.models import Channel, Video, VideoMetrics, Comment, Keyword
from app.services.youtube_service import youtube_service
from app.services.comment_analysis import comment_analysis_service
from app.utils.score_utils import compute_buzz_score, compute_fresh_score
from app.config import settings
from datetime import datetime, timedelta, timezone

class DiscoveryEngine:
    @staticmethod
    async def daily_channel_crawl(db: AsyncSession):
        # 1. Fetch curated channels
        stmt = select(Channel).where(Channel.is_curated == True)
        result = await db.execute(stmt)
        channels = result.scalars().all()
        
        published_after = datetime.now(timezone.utc) - timedelta(days=30)
        
        for channel in channels:
            # 2. Get uploads playlist if not cached
            if not channel.uploads_playlist_id:
                channel.uploads_playlist_id = await youtube_service.get_uploads_playlist_id(channel.channel_id)
                await db.commit()
            
            if not channel.uploads_playlist_id:
                continue
            
            # 3. Fetch recent videos
            videos_data = await youtube_service.fetch_channel_videos(channel.uploads_playlist_id, published_after)
            video_ids = [v["video_id"] for v in videos_data]
            
            if not video_ids:
                continue
                
            # 4. Fetch detailed stats
            stats_data = await youtube_service.fetch_video_stats(video_ids)
            stats_map = {s["video_id"]: s for s in stats_data}
            
            for v in videos_data:
                video_id = v["video_id"]
                s = stats_map.get(video_id)
                if not s: continue
                
                # Update or Insert Video
                stmt = select(Video).where(Video.video_id == video_id)
                res = await db.execute(stmt)
                video = res.scalar()
                
                if not video:
                    video = Video(
                        video_id=video_id,
                        channel_id=channel.channel_id,
                        title=v["title"],
                        description=v["description"],
                        publish_time=v["publish_time"]
                    )
                    db.add(video)
                
                video.view_count = s["view_count"]
                video.like_count = s["like_count"]
                video.comment_count = s["comment_count"]
                video.tags = s["tags"]
                
                # 5. Compute Buzz Score
                buzz_score = compute_buzz_score(
                    s["view_count"], s["like_count"], s["comment_count"], v["publish_time"]
                )
                
                # 6. Check Viral Spike
                view_velocity = s["view_count"] / max(1, (datetime.now(timezone.utc) - v["publish_time"]).days)
                viral_spike = False
                if channel.avg_view_velocity and view_velocity > channel.avg_view_velocity * 3:
                    viral_spike = True
                
                # Update VideoMetrics
                stmt = select(VideoMetrics).where(VideoMetrics.video_id == video_id)
                res = await db.execute(stmt)
                metrics = res.scalar()
                
                if not metrics:
                    metrics = VideoMetrics(video_id=video_id)
                    db.add(metrics)
                
                metrics.buzz_score = buzz_score
                metrics.view_velocity = view_velocity
                metrics.viral_spike = viral_spike
                metrics.engagement_rate = (s["like_count"] + s["comment_count"]) / s["view_count"] if s["view_count"] > 0 else 0
                metrics.fresh_score = compute_fresh_score(v["publish_time"])
                metrics.scored_at = datetime.now(timezone.utc)

            channel.last_crawled_at = datetime.now(timezone.utc)
            await db.commit()

        # 7. Stage 2: Fetch comments for Top 20 Buzz videos
        await DiscoveryEngine.analyze_top_discussions(db)

    @staticmethod
    async def keyword_discovery(db: AsyncSession):
        # 1. Fetch active keywords
        stmt = select(Keyword).where(Keyword.is_active == True)
        result = await db.execute(stmt)
        keywords = result.scalars().all()
        
        published_after = datetime.now(timezone.utc) - timedelta(days=7)
        
        for kw in keywords:
            # 2. Search for videos using keyword
            videos_data = await youtube_service.search_videos(kw.term, max_results=50, published_after=published_after)
            
            for v_data in videos_data:
                # 3. If channel not in DB, add it
                stmt = select(Channel).where(Channel.channel_id == v_data["channel_id"])
                res = await db.execute(stmt)
                channel = res.scalar()
                
                if not channel:
                    channel = Channel(
                        channel_id=v_data["channel_id"],
                        name=v_data["channel_title"],
                        is_curated=False # Newly discovered
                    )
                    db.add(channel)
                    await db.commit()
            
            kw.last_discovered_at = datetime.now(timezone.utc)
            await db.commit()

    @staticmethod
    async def analyze_top_discussions(db: AsyncSession):
        # Get top 20 videos by buzz_score from today's crawl
        stmt = (
            select(Video, VideoMetrics)
            .join(VideoMetrics, Video.video_id == VideoMetrics.video_id)
            .order_by(desc(VideoMetrics.buzz_score))
            .limit(settings.TOP_VIDEOS_FOR_COMMENTS)
        )
        result = await db.execute(stmt)
        
        for video, metrics in result.all():
            comments_data = await youtube_service.fetch_video_comments(video.video_id, settings.MAX_COMMENTS_PER_VIDEO)
            if not comments_data:
                continue
                
            analysis = comment_analysis_service.analyze_comments(
                comments_data, video.view_count, video.publish_time
            )
            
            metrics.discussion_score = analysis["discussion_score"]
            metrics.debate_ratio = analysis["debate_ratio"]
            metrics.sentiment_conflict = analysis["sentiment_conflict"]
            metrics.comment_density = analysis["comment_density"]
            metrics.comment_velocity = analysis["comment_velocity"]
            
            # Save comments
            for c_data in analysis["analyzed_comments"]:
                stmt = select(Comment).where(Comment.comment_id == c_data["comment_id"])
                res = await db.execute(stmt)
                if not res.scalar():
                    comment = Comment(
                        video_id=video.video_id,
                        comment_id=c_data["comment_id"],
                        comment_text=c_data["comment_text"],
                        like_count=c_data["like_count"],
                        sentiment=c_data["sentiment"],
                        sentiment_score=c_data["sentiment_score"],
                        is_debate=c_data["is_debate"],
                        created_at=c_data["created_at"]
                    )
                    db.add(comment)
            
            await db.commit()

discovery_engine = DiscoveryEngine()
