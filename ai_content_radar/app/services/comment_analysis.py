from typing import List, Dict, Any
import statistics
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime, timezone

analyzer = SentimentIntensityAnalyzer()

DEBATE_KEYWORDS = [
    "i disagree", "this is wrong", "no way",
    "you're wrong", "that's stupid", "exactly",
    "absolutely not", "that's incorrect", "wrong",
    "fake", "propaganda", "lies", "truth"
]

class CommentAnalysisService:
    @staticmethod
    def is_debate_comment(text: str) -> bool:
        return any(kw in text.lower() for kw in DEBATE_KEYWORDS)

    @staticmethod
    def analyze_comments(comments: List[Dict[str, Any]], total_view_count: int, publish_time: datetime) -> Dict[str, Any]:
        if not comments:
            return {
                "discussion_score": 0,
                "debate_ratio": 0,
                "sentiment_conflict": 0,
                "comment_density": 0,
                "comment_velocity": 0
            }

        total_comments = len(comments)
        debate_count = 0
        sentiment_scores = []

        for c in comments:
            text = c["comment_text"]
            if CommentAnalysisService.is_debate_comment(text):
                debate_count += 1
                c["is_debate"] = True
            else:
                c["is_debate"] = False
            
            vs = analyzer.polarity_scores(text)
            c["sentiment_score"] = vs["compound"]
            c["sentiment"] = "positive" if vs["compound"] >= 0.05 else "negative" if vs["compound"] <= -0.05 else "neutral"
            sentiment_scores.append(vs["compound"])

        debate_ratio = debate_count / total_comments
        sentiment_conflict = statistics.stdev(sentiment_scores) if len(sentiment_scores) > 1 else 0
        
        # Comment Density: total_comments / views
        comment_density = total_comments / total_view_count if total_view_count > 0 else 0
        
        # Comment Velocity: total_comments / days
        days_since_upload = (datetime.now(timezone.utc) - publish_time).days
        comment_velocity = total_comments / (max(0, days_since_upload) + 1)

        # Normalize components for Discussion Score (0-100)
        # comment_density: 0.01 (1%) is very high. Cap at 0.02
        norm_density = min(0.02, comment_density) / 0.02
        
        # debate_ratio: 0.3 (30%) is high. Cap at 0.5
        norm_debate = min(0.5, debate_ratio) / 0.5
        
        # comment_velocity: 100 comments/day is high for our sample. Cap at 200
        norm_velocity = min(200, comment_velocity) / 200
        
        # sentiment_conflict: max stdev for -1 to 1 is 1.0
        norm_conflict = sentiment_conflict # already 0-1ish

        discussion_score = (
            norm_density * 0.4 +
            norm_debate * 0.3 +
            norm_velocity * 0.2 +
            norm_conflict * 0.1
        ) * 100

        return {
            "discussion_score": min(100, discussion_score),
            "debate_ratio": debate_ratio,
            "sentiment_conflict": sentiment_conflict,
            "comment_density": comment_density,
            "comment_velocity": comment_velocity,
            "analyzed_comments": comments
        }

comment_analysis_service = CommentAnalysisService()
