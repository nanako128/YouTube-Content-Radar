# 007 – Infrastructure

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                                  │
│                                                                      │
│   Browser / Mobile                                                   │
│       │                                                              │
│       ▼                                                              │
│   ┌──────────────────┐                                               │
│   │  Next.js Frontend │  (port 3000)                                 │
│   │  (SSR + Client)   │                                              │
│   └────────┬─────────┘                                               │
│            │ HTTP REST                                                │
└────────────┼────────────────────────────────────────────────────────┘
             │
┌────────────┼────────────────────────────────────────────────────────┐
│            ▼          APPLICATION LAYER                              │
│   ┌──────────────────┐                                               │
│   │  FastAPI Server   │  (port 8000)                                 │
│   │  (uvicorn)        │                                              │
│   └──┬───────────┬───┘                                               │
│      │           │                                                   │
│      ▼           ▼                                                   │
│  ┌───────┐  ┌─────────┐                                              │
│  │ Redis │  │ Postgres │                                             │
│  │ Cache │  │   DB     │                                             │
│  │(6379) │  │ (5432)   │                                             │
│  └───────┘  └─────────┘                                             │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                     BACKGROUND WORKER LAYER                          │
│                                                                      │
│   ┌─────────────────┐     ┌──────────────────┐                      │
│   │  Celery Worker  │     │  Celery Beat      │                      │
│   │  (task runner)  │◄────│  (scheduler)      │                      │
│   └────────┬────────┘     └──────────────────┘                      │
│            │                                                         │
│            │ dispatches tasks via Redis broker                       │
│            │                                                         │
│            ├──► youtube_service.py ──► YouTube Data API v3           │
│            ├──► score_utils.py                                       │
│            ├──► comment_analysis.py                                  │
│            ├──► ranking_service.py ──► PostgreSQL                   │
│            └──► trend_detection.py (Phase 2)                         │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Docker Compose Services

```yaml
# docker-compose.yml (summary)

services:

  db:
    image: postgres:15
    ports: ["5432:5432"]
    environment:
      POSTGRES_DB: content_radar
      POSTGRES_USER: radar
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  api:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ports: ["8000:8000"]
    env_file: .env
    depends_on: [db, redis]

  worker:
    build: .
    command: celery -A celery_worker worker --loglevel=info --concurrency=4
    env_file: .env
    depends_on: [db, redis]

  beat:
    build: .
    command: celery -A celery_worker beat --loglevel=info
    env_file: .env
    depends_on: [db, redis]

  frontend:
    build: ./frontend
    command: npm run dev
    ports: ["3000:3000"]
    environment:
      NEXT_PUBLIC_API_URL: http://api:8000

volumes:
  postgres_data:
```

---

## Environment Variables

**Backend `.env`:**
```
DATABASE_URL=postgresql+asyncpg://radar:password@db:5432/content_radar
REDIS_URL=redis://redis:6379/0
YOUTUBE_API_KEY=your_key_here
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2
```

**Frontend `.env.local`:**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Scheduled Task Timing

| Task | Schedule | Description |
|---|---|---|
| `daily_channel_crawl` | Daily 04:00 UTC | Crawl all curated channels, compute Buzz Score |
| `daily_ranking_generation` | Daily 05:00 UTC | Generate and cache top-N rankings |
| `weekly_keyword_discovery` | Weekly Mon 06:00 UTC | Keyword search, discover new channels |
| `trend_analysis` | Daily 05:30 UTC | Phase 2: TF-IDF + clustering |

---

## Scaling Considerations (Post-MVP)

| Concern | Solution |
|---|---|
| YouTube API quota limit | Request quota increase; add quota tracking middleware |
| Celery worker throughput | Increase `--concurrency`; add more worker replicas |
| DB read load | Add read replica; use Redis for ranking cache aggressively |
| Frontend traffic | Deploy Next.js on Vercel or behind CDN |
| Secrets management | Move to AWS Secrets Manager or Vault in production |

---

## Production Deployment (Recommended)

| Service | Platform |
|---|---|
| Frontend | Vercel |
| Backend API | AWS ECS / Railway / Render |
| PostgreSQL | AWS RDS or Supabase |
| Redis | AWS ElastiCache or Upstash |
| Celery Workers | Same ECS cluster or Fly.io workers |
| CI/CD | GitHub Actions |
