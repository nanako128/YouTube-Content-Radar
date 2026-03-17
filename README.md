# AI Content Radar

> AI-powered YouTube content discovery engine for social media teams.

AI Content Radar automatically surfaces viral videos, discussion-heavy content, and emerging trends from YouTube — delivering daily ranked lists that content editors can act on immediately.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Environment Variables](#environment-variables)
  - [Run with Docker Compose](#run-with-docker-compose)
  - [Run Locally (without Docker)](#run-locally-without-docker)
- [API Reference](#api-reference)
- [Scheduled Tasks](#scheduled-tasks)
- [Scoring Logic](#scoring-logic)
- [PRD Documents](#prd-documents)
- [Roadmap](#roadmap)
- [License](#license)

---

## Overview

Social media teams waste hours manually scouring YouTube for content ideas. AI Content Radar solves this by running an automated daily pipeline that:

1. Crawls a curated list of YouTube channels
2. Computes a **Buzz Score** (virality potential) and **Discussion Score** (debate intensity) for each video
3. Detects **viral spikes** — videos growing 3× faster than their channel average
4. Generates ranked lists accessible via a clean REST API and Next.js dashboard

---

## Features

### Phase 1 (MVP)
- 📡 **Channel Crawler** — Fetches recent videos from a curated channel list (last 30 days)
- 🔥 **Buzz Score** — Composite score based on views, engagement rate, comment count, and freshness
- 💬 **Discussion Score** — Detects debate-heavy videos using comment density, debate keyword detection, and sentiment conflict
- ⚡ **Viral Spike Detection** — Flags videos whose view velocity exceeds 3× their channel's average
- 🏆 **Daily Rankings** — Top Buzz, Top Discussion, and Top Viral lists updated every day
- 🔍 **Keyword Discovery** — Weekly search for new content and channels using configurable keywords
- 🖥️ **Dashboard UI** — Next.js frontend displaying all rankings and channel data

### Phase 2 (Planned)
- 🧠 **AI Trend Detection** — TF-IDF + sentence-transformers + HDBSCAN topic clustering
- 📈 **Trend Velocity** — Tracks which topics are emerging vs. fading
- 🗂️ **Video Detail Page** — Deep-dive into individual video metrics and comments

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 14 (App Router) + TypeScript + Tailwind CSS |
| Backend | Python 3.11 + FastAPI |
| Database | PostgreSQL 15 |
| Cache | Redis 7 |
| Task Queue | Celery 5 + Celery Beat |
| AI / NLP | sentence-transformers, scikit-learn, HDBSCAN, VADER |
| External API | YouTube Data API v3 |
| Infrastructure | Docker + Docker Compose |

---

## Project Structure

```
.
├── ai_content_radar/          # Backend (Python / FastAPI)
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── api/               # Route handlers
│   │   ├── services/          # Business logic
│   │   ├── models/            # SQLAlchemy ORM models
│   │   ├── db/                # Database + Pydantic schemas
│   │   ├── tasks/             # Celery tasks
│   │   └── utils/             # Score formulas, NLP helpers
│   ├── celery_worker.py
│   ├── requirements.txt
│   └── alembic/               # DB migrations
│
├── frontend/                  # Frontend (Next.js / TypeScript)
│   ├── app/                   # App Router pages
│   ├── components/            # UI components
│   ├── lib/                   # API client, utilities
│   └── types/                 # Shared TypeScript types
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose
- [YouTube Data API v3 key](https://console.cloud.google.com/) (free, 10,000 units/day)
- Node.js 20+ (for local frontend development without Docker)
- Python 3.11+ (for local backend development without Docker)

---

### Environment Variables

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

**`.env` (backend):**
```env
DATABASE_URL=postgresql+asyncpg://radar:password@db:5432/content_radar
REDIS_URL=redis://redis:6379/0
YOUTUBE_API_KEY=your_youtube_api_key_here
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2
```

**`frontend/.env.local`:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

### Run with Docker Compose

```bash
# 1. Clone the repository
git clone https://github.com/your-org/ai-content-radar.git
cd ai-content-radar

# 2. Set up environment variables
cp .env.example .env
# Edit .env and add your YOUTUBE_API_KEY

# 3. Start all services
docker compose up --build

# 4. Run database migrations
docker compose exec api alembic upgrade head

# 5. (Optional) Manually trigger the first crawl
curl -X POST http://localhost:8000/tasks/trigger-crawl
```

Services will be available at:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs (Swagger):** http://localhost:8000/docs

---

### Run Locally (without Docker)

**Backend:**
```bash
cd ai_content_radar

# Install dependencies
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run DB migrations (requires running PostgreSQL)
alembic upgrade head

# Start API server
uvicorn app.main:app --reload --port 8000

# Start Celery worker (separate terminal)
celery -A celery_worker worker --loglevel=info

# Start Celery Beat scheduler (separate terminal)
celery -A celery_worker beat --loglevel=info
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
# Available at http://localhost:3000
```

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/videos/top-buzz` | Top videos by Buzz Score |
| `GET` | `/videos/top-discussion` | Top videos by Discussion Score |
| `GET` | `/videos/viral` | Videos with viral spike flag |
| `GET` | `/trends/topics` | Detected trend topic clusters |
| `GET` | `/channels/discovered` | Newly discovered channels |
| `GET` | `/health` | Service health + last crawl status |

All ranking endpoints support `limit` and `offset` query parameters.

Full API documentation is available at `http://localhost:8000/docs` (Swagger UI) when the server is running.

For detailed schema definitions, see [002_api.md](./002_api.md).

---

## Scheduled Tasks

| Task | Schedule | Description |
|---|---|---|
| `daily_channel_crawl` | Daily 04:00 UTC | Crawl all channels, compute Buzz + Discussion scores |
| `daily_ranking_generation` | Daily 05:00 UTC | Generate rankings and cache in Redis |
| `weekly_keyword_discovery` | Monday 06:00 UTC | Keyword search, add new channels to pool |
| `trend_analysis` | Daily 05:30 UTC | Phase 2: AI topic clustering |

---

## Scoring Logic

### Buzz Score (0–100)
```
engagement_rate = (likes + comments) / views
fresh_score     = 1 / (days_since_upload + 1)

buzz_score = normalize(
    views            × 0.4 +
    engagement_rate  × 0.3 +
    comments         × 0.2 +
    fresh_score      × 0.1
)
```

### Discussion Score (0–100)
```
comment_density  = comments / views
debate_ratio     = debate_comments / total_comments  # keyword-based
comment_velocity = comments / days_since_upload

discussion_score = normalize(
    comment_density    × 0.4 +
    debate_ratio       × 0.3 +
    comment_velocity   × 0.2 +
    sentiment_conflict × 0.1
)
```

### Viral Spike
```
view_velocity = views / days_since_upload
viral_spike   = (view_velocity > channel_avg_velocity × 3)
```

---

## PRD Documents

Detailed product requirements are in the `/docs` folder:

| File | Description |
|---|---|
| [000_overview.md](./000_overview.md) | Project goals, scope, and success metrics |
| [001_pages.md](./001_pages.md) | Frontend page specifications |
| [002_api.md](./002_api.md) | REST API endpoint definitions |
| [003_structure.md](./003_structure.md) | Full codebase directory structure |
| [004_techStack.md](./004_techStack.md) | All dependencies and versions |
| [005_research.md](./005_research.md) | YouTube API quota analysis and external library notes |
| [006_db.md](./006_db.md) | Database schema and table definitions |
| [007_infra.md](./007_infra.md) | Infrastructure diagram and Docker Compose config |
| [008_core.md](./008_core.md) | Core processing flow diagrams |
| [009_tasks.md](./009_tasks.md) | 4-week sprint plan and milestones |
| [010_other.md](./010_other.md) | Non-functional requirements, security, and future ideas |

---

## Roadmap

- [x] Daily channel crawl pipeline
- [x] Buzz Score + Discussion Score
- [x] Viral spike detection
- [x] Daily rankings via REST API
- [x] Next.js dashboard
- [ ] AI trend detection (TF-IDF + HDBSCAN)
- [ ] Trend velocity tracking and topic pages
- [ ] Video detail page with comment explorer
- [ ] Slack/email alerts for high-buzz videos
- [ ] Multi-platform support (TikTok, Instagram Reels)

---

## License

MIT License. See [LICENSE](./LICENSE) for details.
