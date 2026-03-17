# 001 – Pages

All pages are built with **Next.js (App Router) + TypeScript**.

---

## Page List

### 1. `/` — Dashboard Home
**Purpose:** Entry point. Shows summary cards and today's top picks at a glance.

**Components:**
- Summary stats bar: total videos crawled today, new channels discovered, active trends
- "Top Buzz" preview card (top 3 videos)
- "Top Discussion" preview card (top 3 videos)
- "Viral Spikes" preview card (top 3 videos)
- "Emerging Trends" topic chip list
- Last updated timestamp

---

### 2. `/videos/buzz` — Top Buzz Videos
**Purpose:** Full ranked list of videos with the highest Buzz Score.

**Components:**
- Sortable/filterable data table
  - Columns: Rank, Thumbnail, Title, Channel, Views, Buzz Score, Fresh Score, Published At
- Filters: date range, min views
- Pagination (20 per page)
- Export to CSV button

---

### 3. `/videos/discussion` — Top Discussion Videos
**Purpose:** Full ranked list of videos with the highest Discussion Score.

**Components:**
- Sortable data table
  - Columns: Rank, Thumbnail, Title, Channel, Comments, Discussion Score, Debate Ratio, Comment Density
- Filters: min debate ratio slider
- Pagination

---

### 4. `/videos/viral` — Viral Spike Videos
**Purpose:** Videos whose view velocity exceeds 3× their channel average.

**Components:**
- Data table with viral badge
  - Columns: Rank, Thumbnail, Title, Channel, View Velocity, Channel Avg Velocity, Spike Ratio
- Real-time indicator if data is from today

---

### 5. `/trends` — Trending Topics
**Purpose:** Topic clusters detected by AI trend analysis (Phase 2; Phase 1 shows placeholder).

**Components:**
- Topic card grid
  - Each card: topic name, keyword chips, video count, trend velocity, emerging badge
- Trend velocity sparkline per topic
- Phase 1: Static placeholder with "Trend Detection coming in Phase 2" notice

---

### 6. `/channels` — Discovered Channels
**Purpose:** Newly discovered channels surfaced via related-video expansion.

**Components:**
- Channel list table
  - Columns: Channel Name, Subscriber Count, Videos Crawled, Avg Buzz Score, Discovered At, Source (curated / discovered)
- Filter: curated vs. discovered toggle

---

### 7. `/videos/[videoId]` — Video Detail (optional, Phase 2)
**Purpose:** Deep-dive into a single video's metrics and comments.

**Components:**
- Video embed (YouTube iframe)
- Metric cards: Buzz Score, Discussion Score, Debate Ratio, View Velocity
- Top comments table with sentiment label and is_debate flag
- Related videos list

---

## Shared Layout Components
| Component | Description |
|---|---|
| `Sidebar` | Navigation links to all main pages |
| `Header` | Page title + last updated badge |
| `ScoreBadge` | Color-coded score pill (green / yellow / red) |
| `VideoCard` | Reusable card with thumbnail, title, channel, scores |
| `LoadingState` | Skeleton loaders for async data |
| `ErrorBanner` | API error fallback message |
