from datetime import datetime, timezone
import math

def compute_buzz_score(view_count: int, like_count: int, comment_count: int, publish_time: datetime) -> float:
    """
    Computes Buzz Score (0-100)
    Formula: normalize(views*0.4 + engagement*0.3 + comments*0.2 + fresh*0.1)
    """
    # Engagement Rate: (likes + comments) / views (handle division by zero)
    engagement_rate = (like_count + comment_count) / view_count if view_count > 0 else 0
    
    # Freshness Score: 1 / (days_since_upload + 1)
    days_since_upload = (datetime.now(timezone.utc) - publish_time).days
    fresh_score = 1 / (max(0, days_since_upload) + 1)
    
    # Normalizing view_count and comment_count (using log to handle large differences)
    # 1M views -> log10(1,000,000) = 6. Let's cap at log10(10M) = 7
    norm_views = min(7, math.log10(view_count + 1)) / 7
    norm_comments = min(5, math.log10(comment_count + 1)) / 5
    
    # Engagement rate: 0.1 is usually considered good. Cap at 0.2
    norm_engagement = min(0.2, engagement_rate) / 0.2
    
    raw_score = (
        norm_views * 0.4 +
        norm_engagement * 0.3 +
        norm_comments * 0.2 +
        fresh_score * 0.1
    )
    
    return min(100, raw_score * 100)

def compute_fresh_score(publish_time: datetime) -> float:
    days_since_upload = (datetime.now(timezone.utc) - publish_time).days
    return 1 / (max(0, days_since_upload) + 1)
