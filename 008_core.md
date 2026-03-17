# 008 – Core Feature Processing Flows

---

## Flow 1: Daily Channel Crawl

Triggered by Celery Beat at **04:00 UTC daily**.

```
Celery Beat
  │
  ▼
[Task] daily_channel_crawl
  │
  ├─► For each channel in curated_channels list:
  │       │
  │       ├─► youtube_service.get_uploads_playlist_id(channel_id)
  │       │
  │       └─► youtube_service.fetch_channel_videos(playlist_id, published_after=30d)
  │               │
  │               └─► Returns: list of {video_id, title, publish_time}
  │
  ├─► Batch fetch video stats: youtube_service.fetch_video_stats(video_ids[])
  │       └─► Returns: {view_count, like_count, comment_count, tags, duration}
  │
  ├─► Upsert records into `videos` table
  │
  ├─► For each video, compute Buzz Score:
  │       │
  │       └─► score_utils.compute_buzz_score(views, likes, comments, publish_time)
  │               │
  │               ├─► engagement_rate = (likes + comments) / views
  │               ├─► fresh_score = 1 / (days_since_upload + 1)
  │               └─► buzz_score = normalize(
  │                       views * 0.4 +
  │                       engagement_rate * 0.3 +
  │                       comments * 0.2 +
  │                       fresh_score * 0.1
  │                   ) → 0–100
  │
  ├─► Check viral spike for each video:
  │       │
  │       ├─► view_velocity = views / days_since_upload
  │       ├─► channel_avg_velocity = channels.avg_view_velocity
  │       └─► viral_spike = (view_velocity > channel_avg_velocity * 3)
  │
  ├─► Upsert `video_metrics` table
  │
  └─► Select Top 20 videos by buzz_score
          │
          └─► [Stage 2] For each top video:
                  │
                  ├─► youtube_service.fetch_video_comments(video_id, max=200)
                  │
                  ├─► comment_analysis.compute_discussion_score(comments)
                  │       │
                  │       ├─► Detect debate keywords per comment → is_debate flag
                  │       ├─► VADER sentiment per comment → sentiment_score
                  │       ├─► comment_density = total_comments / views
                  │       ├─► comment_velocity = total_comments / days
                  │       ├─► debate_ratio = debate_count / total_count
                  │       ├─► sentiment_conflict = std_dev(compound_scores)
                  │       └─► discussion_score = normalize(
                  │               comment_density * 0.4 +
                  │               debate_ratio * 0.3 +
                  │               comment_velocity * 0.2 +
                  │               sentiment_conflict * 0.1
                  │           ) → 0–100
                  │
                  ├─► Upsert comments into `comments` table
                  └─► Update `video_metrics` with discussion_score
```

---

## Flow 2: Daily Ranking Generation

Triggered at **05:00 UTC daily** (after crawl completes).

```
[Task] daily_ranking_generation
  │
  ├─► Query video_metrics WHERE scored_at > today - 1d
  │
  ├─► Generate ranking type: "buzz"
  │       └─► ORDER BY buzz_score DESC LIMIT 50
  │
  ├─► Generate ranking type: "discussion"
  │       └─► ORDER BY discussion_score DESC LIMIT 50
  │
  ├─► Generate ranking type: "viral"
  │       └─► WHERE viral_spike = TRUE ORDER BY view_velocity DESC LIMIT 50
  │
  ├─► Bulk insert into `rankings` table (with ranked_at = NOW())
  │
  └─► Cache results in Redis:
          KEY: "rankings:buzz"        TTL: 24h
          KEY: "rankings:discussion"  TTL: 24h
          KEY: "rankings:viral"       TTL: 24h
```

---

## Flow 3: Weekly Keyword Discovery

Triggered **Monday 06:00 UTC**.

```
[Task] weekly_keyword_discovery
  │
  ├─► For each keyword in ["AI", "Gen Z", "remote work", "startup", "technology"]:
  │       │
  │       └─► youtube_service.search_videos_by_keyword(keyword, max=50)
  │               └─► Returns: list of {video_id, channel_id, title}
  │
  ├─► For all returned videos:
  │       └─► Extract unique channel_ids not already in `channels` table
  │               └─► Add to candidate channel pool
  │
  ├─► For new candidate channels:
  │       ├─► Fetch channel stats (subscriber_count)
  │       ├─► Filter: subscriber_count > 10,000 (configurable)
  │       └─► Insert into `channels` table (is_curated = false)
  │
  └─► Queue discovered channels for next daily crawl
```

---

## Flow 4: Related Video Channel Expansion

Runs after daily crawl, triggered by high Buzz Score threshold.

```
[Task] discovery_engine.expand_from_related_videos()
  │
  ├─► Query videos WHERE buzz_score > 70 AND publish_time > 7 days ago
  │
  ├─► For each qualifying video:
  │       │
  │       └─► Search YouTube by video's top tags (replaces deprecated relatedToVideoId)
  │               └─► youtube_service.search_videos_by_keyword(tags[0], max=10)
  │
  ├─► Extract unique channel_ids from results
  │
  └─► Add new channels to `channels` table (is_curated = false)
```

---

## Flow 5: API Request (Cached)

```
GET /videos/top-buzz
  │
  ├─► Check Redis: GET "rankings:buzz"
  │       │
  │       ├─► HIT: Return cached JSON (< 1ms)
  │       │
  │       └─► MISS:
  │               ├─► Query `rankings` JOIN `videos` JOIN `video_metrics`
  │               │       WHERE type='buzz' AND ranked_at = latest
  │               │       ORDER BY rank ASC
  │               ├─► Serialize response
  │               ├─► SET Redis "rankings:buzz" TTL=24h
  │               └─► Return response
```

---

## Score Formulas (Reference)

### Buzz Score
```
engagement_rate = (like_count + comment_count) / view_count
fresh_score     = 1 / (days_since_upload + 1)

raw = (
    normalized_views        * 0.4 +
    engagement_rate         * 0.3 +
    normalized_comments     * 0.2 +
    fresh_score             * 0.1
)

buzz_score = min(raw * 100, 100)   # normalized to 0-100
```

### Discussion Score
```
comment_density    = comment_count / view_count
comment_velocity   = comment_count / days_since_upload
debate_ratio       = debate_comment_count / total_sampled_comments
sentiment_conflict = std_dev([c.sentiment_score for c in comments])

raw = (
    comment_density    * 0.4 +
    debate_ratio       * 0.3 +
    normalized_velocity * 0.2 +
    sentiment_conflict * 0.1
)

discussion_score = min(raw * 100, 100)
```

### Viral Spike
```
view_velocity = view_count / days_since_upload
viral_spike   = (view_velocity > channel.avg_view_velocity * 3)
```

### Debate Detection Keywords
```
DEBATE_KEYWORDS = [
    "i disagree", "this is wrong", "no way",
    "you're wrong", "that's stupid", "exactly",
    "absolutely not", "that's incorrect", "wrong"
]

is_debate = any(kw in comment_text.lower() for kw in DEBATE_KEYWORDS)
```
