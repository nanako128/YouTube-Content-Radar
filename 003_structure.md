# 003 – Codebase Structure

The project is split into two independent repositories (or monorepo subdirectories):

---

## Backend — `ai_content_radar/`

```
ai_content_radar/
├── app/
│   ├── main.py                   # FastAPI app entrypoint, router registration
│   ├── config.py                 # Settings via pydantic-settings (env vars)
│   │
│   ├── api/                      # Route handlers (thin controllers)
│   │   ├── videos.py             # GET /videos/top-buzz, /top-discussion, /viral
│   │   ├── trends.py             # GET /trends/topics
│   │   └── channels.py           # GET /channels/discovered
│   │
│   ├── services/                 # Business logic
│   │   ├── youtube_service.py    # YouTube Data API wrapper
│   │   ├── ranking_service.py    # Ranking generation logic
│   │   ├── comment_analysis.py   # Discussion Score + debate detection
│   │   ├── trend_detection.py    # TF-IDF, embeddings, HDBSCAN clustering
│   │   └── discovery_engine.py   # 3-source video discovery orchestrator
│   │
│   ├── models/                   # SQLAlchemy ORM models
│   │   ├── channel.py
│   │   ├── video.py
│   │   ├── comment.py
│   │   └── metrics.py
│   │
│   ├── db/
│   │   ├── database.py           # SQLAlchemy engine + session factory
│   │   └── schemas.py            # Pydantic response schemas
│   │
│   ├── tasks/                    # Celery tasks
│   │   ├── crawl_tasks.py        # daily_channel_crawl, weekly_keyword_discovery
│   │   ├── ranking_tasks.py      # daily_ranking_generation
│   │   └── trend_tasks.py        # trend_analysis (Phase 2)
│   │
│   └── utils/
│       ├── nlp_utils.py          # TF-IDF helpers, sentiment helpers
│       └── score_utils.py        # Buzz Score, Fresh Score formulas
│
├── celery_worker.py              # Celery app + Beat schedule definition
├── requirements.txt
├── docker-compose.yml
├── .env.example
└── alembic/                      # DB migrations
    ├── env.py
    └── versions/
```

### Key Design Principles (Backend)
- **Thin routes:** API handlers only validate input and call service layer.
- **Service layer:** All business logic lives in `services/`. No DB access in routes directly.
- **Task isolation:** Celery tasks call services; tasks do not contain logic themselves.
- **Config via env:** All secrets (API keys, DB URLs) loaded from `.env` via `pydantic-settings`.

---

## Frontend — `frontend/`

```
frontend/
├── app/                          # Next.js App Router
│   ├── layout.tsx                # Root layout (sidebar + header)
│   ├── page.tsx                  # Dashboard Home "/"
│   ├── videos/
│   │   ├── buzz/page.tsx         # /videos/buzz
│   │   ├── discussion/page.tsx   # /videos/discussion
│   │   └── viral/page.tsx        # /videos/viral
│   ├── trends/
│   │   └── page.tsx              # /trends
│   └── channels/
│       └── page.tsx              # /channels
│
├── components/
│   ├── layout/
│   │   ├── Sidebar.tsx
│   │   └── Header.tsx
│   ├── ui/
│   │   ├── ScoreBadge.tsx
│   │   ├── VideoCard.tsx
│   │   ├── DataTable.tsx
│   │   ├── LoadingState.tsx
│   │   └── ErrorBanner.tsx
│   └── charts/
│       └── TrendSparkline.tsx    # Phase 2
│
├── lib/
│   ├── api.ts                    # API client (fetch wrappers)
│   └── utils.ts                  # Score color helpers, date formatters
│
├── types/
│   └── index.ts                  # Shared TypeScript types / interfaces
│
├── public/
│   └── logo.svg
│
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

### Key Design Principles (Frontend)
- **Server Components by default:** Pages fetch data server-side for SEO and performance.
- **Client Components only when needed:** Filters, interactive tables use `"use client"`.
- **API client in `lib/api.ts`:** All fetch calls centralized; easy to swap base URL.
- **Type-safe:** All API responses typed in `types/index.ts`.
