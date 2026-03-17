# 005 – Research & External API Notes

## 1. YouTube Data API v3

### Overview
The YouTube Data API v3 is the primary external data source. All video metadata, channel data, search results, and comments are fetched through it.

**Console:** https://console.cloud.google.com  
**Docs:** https://developers.google.com/youtube/v3

---

### Quota System

YouTube Data API uses a **unit-based quota** system. Default quota: **10,000 units/day** per project.

| Operation | Units | Notes |
|---|---|---|
| `search.list` | 100 units | Most expensive; use sparingly |
| `videos.list` | 1 unit | Batch up to 50 video IDs |
| `channels.list` | 1 unit | Batch up to 50 |
| `commentThreads.list` | 1 unit | Up to 100 comments per page |
| `playlistItems.list` | 1 unit | Used for channel video lists |

**Estimated daily quota usage (MVP):**

| Task | Calls | Units |
|---|---|---|
| Fetch 20 channels × 50 videos | 20 × `playlistItems.list` | ~20 |
| Batch fetch 1,000 video metadata | ~20 × `videos.list` (50/call) | ~20 |
| Top 20 videos: fetch 200 comments each | 40 × `commentThreads.list` | ~40 |
| Weekly keyword search (daily portion) | 10 × `search.list` | 1,000 |
| Related video fetch for top 10 videos | 10 × `search.list` (relatedToVideoId) | 1,000 |
| **Estimated Total** | | **~2,080 units/day** |

> ⚠️ Note: `relatedToVideoId` parameter in `search.list` was **deprecated in August 2023**. Use alternative: fetch a video's `tags`, then run a keyword search using those tags.

---

### Key API Calls

#### Fetch channel videos (last 30 days)
```
GET https://www.googleapis.com/youtube/v3/search
  ?part=snippet
  &channelId={channelId}
  &type=video
  &publishedAfter={30_days_ago_ISO}
  &maxResults=50
  &order=date
  &key={API_KEY}
```
Cost: 100 units per call. **Alternative (cheaper):** Use `playlistItems.list` on the channel's uploads playlist (1 unit/call).

```
GET https://www.googleapis.com/youtube/v3/channels
  ?part=contentDetails
  &id={channelId}
  &key={API_KEY}
→ extract: contentDetails.relatedPlaylists.uploads (playlist ID)

GET https://www.googleapis.com/youtube/v3/playlistItems
  ?part=snippet,contentDetails
  &playlistId={uploadsPlaylistId}
  &maxResults=50
  &key={API_KEY}
```

#### Fetch video statistics in batch
```
GET https://www.googleapis.com/youtube/v3/videos
  ?part=snippet,statistics,contentDetails
  &id={id1},{id2},...{id50}
  &key={API_KEY}
```

#### Fetch video comments
```
GET https://www.googleapis.com/youtube/v3/commentThreads
  ?part=snippet
  &videoId={videoId}
  &maxResults=100
  &order=relevance
  &key={API_KEY}
```
Fetch 2 pages (200 total). Cost: 2 units per video.

---

### Quota Optimization Strategy
1. Use `playlistItems.list` instead of `search.list` for channel crawl (saves ~1,900 units/day)
2. Batch `videos.list` calls (50 IDs per call)
3. Only fetch comments for Top 20 videos (not all videos)
4. Cache results in Redis; do not re-fetch within 24h
5. Consider applying for higher quota if needed (Google form)

---

## 2. sentence-transformers

**Library:** `sentence-transformers` (Hugging Face)  
**Docs:** https://www.sbert.net  

Used for generating sentence embeddings from video titles for topic clustering.

**Recommended model:** `all-MiniLM-L6-v2`
- 384-dimensional embeddings
- Fast (CPU-friendly), good semantic quality
- ~80MB model size

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(titles)  # numpy array shape: (n, 384)
```

**Alternatives if multilingual content is added:**
- `paraphrase-multilingual-MiniLM-L12-v2` (supports 50+ languages)

---

## 3. HDBSCAN

**Library:** `hdbscan`  
**Docs:** https://hdbscan.readthedocs.io  

Used for topic clustering without requiring a fixed number of clusters. Handles noise (outlier videos that don't belong to any cluster).

```python
import hdbscan
clusterer = hdbscan.HDBSCAN(min_cluster_size=3, metric='euclidean')
labels = clusterer.fit_predict(embeddings)
# labels == -1 means noise (unclustered)
```

**Key params:**
| Param | Value | Notes |
|---|---|---|
| `min_cluster_size` | 3–5 | Minimum videos to form a topic |
| `metric` | `euclidean` | Works well with normalized embeddings |

---

## 4. VADER Sentiment Analysis

**Library:** `vaderSentiment`  
Used for comment sentiment scoring (positive/negative/neutral).

```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
score = analyzer.polarity_scores(comment_text)
# score = {'neg': 0.2, 'neu': 0.5, 'pos': 0.3, 'compound': 0.1}
```

`sentiment_conflict` in the Discussion Score is calculated as the standard deviation of compound scores within a video's comment set — high variance = high conflict.

---

## 5. Open Questions / Risks

| Item | Risk | Mitigation |
|---|---|---|
| `relatedToVideoId` deprecated | Cannot discover related channels via API | Use tags-based keyword search as fallback |
| YouTube API quota exhaustion | Crawler fails mid-day | Implement quota tracking; skip low-priority channels if near limit |
| Comments disabled on videos | Discussion Score unavailable | Treat as 0; still rank by Buzz Score |
| Model cold start (sentence-transformers) | First load ~5s | Pre-load model at worker startup |
| Embedding drift across model versions | Inconsistent clusters | Pin model version; re-embed on version change |
