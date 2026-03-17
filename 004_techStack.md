# 004 – Tech Stack

## Overview

| Layer | Technology | Version | Rationale |
|---|---|---|---|
| Frontend | Next.js | 14+ (App Router) | SSR + React, strong ecosystem |
| Frontend Language | TypeScript | 5+ | Type safety across API boundaries |
| Frontend Styling | Tailwind CSS | 3+ | Rapid UI development |
| Backend | Python + FastAPI | 3.11 / 0.110+ | Async, auto OpenAPI docs, fast |
| Database | PostgreSQL | 15+ | Reliable relational store for video/ranking data |
| Cache | Redis | 7+ | 24h ranking cache, Celery broker |
| Task Queue | Celery | 5+ | Distributed async task execution |
| Task Scheduler | Celery Beat | (bundled) | Cron-style daily/weekly scheduling |
| ORM | SQLAlchemy | 2.0+ | Async ORM support |
| DB Migrations | Alembic | latest | Schema versioning |
| AI / NLP | sentence-transformers | latest | Title embeddings for trend clustering |
| AI / NLP | scikit-learn | latest | TF-IDF keyword extraction |
| AI / NLP | hdbscan | latest | Density-based topic clustering |
| Sentiment | transformers / VADER | — | Comment sentiment scoring |
| External API | YouTube Data API v3 | v3 | Video metadata, comments, search |
| Containerization | Docker + Docker Compose | — | Local dev parity; prod deployment |
| Config Management | pydantic-settings | 2+ | Env var parsing with type safety |
| HTTP Client (BE) | httpx | — | Async HTTP calls to YouTube API |
| Data Validation | Pydantic | 2+ | Request/response schema validation |

---

## Frontend Dependencies

```json
{
  "next": "^14",
  "react": "^18",
  "typescript": "^5",
  "tailwindcss": "^3",
  "@tanstack/react-table": "^8",
  "recharts": "^2",
  "date-fns": "^3",
  "clsx": "latest",
  "lucide-react": "latest"
}
```

---

## Backend Dependencies (`requirements.txt`)

```
fastapi>=0.110.0
uvicorn[standard]>=0.29.0
sqlalchemy[asyncio]>=2.0.0
alembic>=1.13.0
asyncpg>=0.29.0
redis>=5.0.0
celery[redis]>=5.3.0
celery[beat]
pydantic-settings>=2.0.0
httpx>=0.27.0
google-api-python-client>=2.120.0
sentence-transformers>=2.7.0
scikit-learn>=1.4.0
hdbscan>=0.8.33
vaderSentiment>=3.3.2
python-dotenv>=1.0.0
```

---

## Infrastructure Services (Docker Compose)

| Service | Image | Port |
|---|---|---|
| `api` | Custom Python image | 8000 |
| `worker` | Same Python image (Celery worker) | — |
| `beat` | Same Python image (Celery Beat) | — |
| `db` | `postgres:15` | 5432 |
| `redis` | `redis:7-alpine` | 6379 |
| `frontend` | Node 20 / Next.js | 3000 |

---

## Versioning & Quality

| Tool | Purpose |
|---|---|
| Ruff | Python linting + formatting |
| ESLint + Prettier | TypeScript linting + formatting |
| pytest | Backend unit/integration tests |
| Jest + React Testing Library | Frontend component tests |
