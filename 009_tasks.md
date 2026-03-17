# 009 – Task List & Schedule

## Phase 1 MVP — Target: 4 Weeks

---

### Week 1 — Project Setup & Backend Foundation

| # | Task | Owner | Est. | Notes |
|---|---|---|---|---|
| 1.1 | Initialize repo structure (backend + frontend) | BE | 0.5d | |
| 1.2 | Set up Docker Compose (postgres, redis, api, worker, beat) | BE | 0.5d | |
| 1.3 | Configure `config.py` with pydantic-settings; `.env.example` | BE | 0.5d | |
| 1.4 | Define SQLAlchemy models: `channels`, `videos`, `video_metrics`, `comments`, `rankings` | BE | 1d | |
| 1.5 | Set up Alembic + run initial migration | BE | 0.5d | |
| 1.6 | Initialize Next.js project (App Router, TypeScript, Tailwind) | FE | 0.5d | |
| 1.7 | Create `lib/api.ts` (base fetch client) and `types/index.ts` | FE | 0.5d | |

---

### Week 2 — Core Backend Logic

| # | Task | Owner | Est. | Notes |
|---|---|---|---|---|
| 2.1 | Implement `youtube_service.py`: `fetch_channel_videos`, `fetch_video_stats` | BE | 1d | Use uploads playlist |
| 2.2 | Implement `youtube_service.py`: `fetch_video_comments`, `search_videos_by_keyword` | BE | 1d | |
| 2.3 | Implement `score_utils.py`: Buzz Score, Fresh Score, normalization | BE | 0.5d | |
| 2.4 | Implement `score_utils.py`: Viral Spike detection | BE | 0.5d | |
| 2.5 | Implement `comment_analysis.py`: debate detection, VADER sentiment, Discussion Score | BE | 1d | |
| 2.6 | Implement `discovery_engine.py`: curated channel crawl + two-stage filtering | BE | 1d | |
| 2.7 | Implement `ranking_service.py`: generate buzz / discussion / viral rankings | BE | 0.5d | |
| 2.8 | Write unit tests for score formulas | BE | 0.5d | pytest |

---

### Week 3 — Celery Tasks + API + Frontend

| # | Task | Owner | Est. | Notes |
|---|---|---|---|---|
| 3.1 | Set up Celery app + `celery_worker.py` | BE | 0.5d | |
| 3.2 | Implement `crawl_tasks.py`: `daily_channel_crawl` task | BE | 0.5d | |
| 3.3 | Implement `ranking_tasks.py`: `daily_ranking_generation` task + Redis cache | BE | 0.5d | |
| 3.4 | Implement `crawl_tasks.py`: `weekly_keyword_discovery` task | BE | 0.5d | |
| 3.5 | Configure Celery Beat schedule (cron times) | BE | 0.5d | |
| 3.6 | Implement FastAPI routes: `GET /videos/top-buzz`, `/top-discussion`, `/viral` | BE | 1d | |
| 3.7 | Implement FastAPI routes: `GET /trends/topics`, `/channels/discovered`, `/health` | BE | 0.5d | |
| 3.8 | Build shared layout: Sidebar + Header components | FE | 0.5d | |
| 3.9 | Build `/videos/buzz` page with DataTable | FE | 1d | |
| 3.10 | Build `/videos/discussion` and `/videos/viral` pages | FE | 1d | |
| 3.11 | Build Dashboard Home (`/`) with summary cards | FE | 0.5d | |
| 3.12 | Build `/channels` page | FE | 0.5d | |

---

### Week 4 — Integration, Polish, Testing

| # | Task | Owner | Est. | Notes |
|---|---|---|---|---|
| 4.1 | End-to-end integration test: trigger crawl manually, verify DB records | BE | 1d | |
| 4.2 | Verify Redis caching works; test cache hit/miss behavior | BE | 0.5d | |
| 4.3 | Frontend: error states, loading skeletons, empty states | FE | 0.5d | |
| 4.4 | Frontend: wire `/trends` page placeholder (Phase 2 notice) | FE | 0.5d | |
| 4.5 | Manual QA: run full daily pipeline with 5 real channels | BE+FE | 1d | |
| 4.6 | Performance check: API response < 500ms cached | BE | 0.5d | |
| 4.7 | Write README with setup instructions | Both | 0.5d | |
| 4.8 | MVP deployment (Docker Compose on server) | BE | 0.5d | |

---

## Phase 2 — AI Trend Detection (Post-MVP)

| # | Task | Est. |
|---|---|---|
| P2.1 | Implement `trend_detection.py`: TF-IDF keyword extraction | 1d |
| P2.2 | Implement embedding generation with sentence-transformers | 1d |
| P2.3 | Implement HDBSCAN clustering | 1d |
| P2.4 | Implement trend velocity calculation + `emerging` status | 0.5d |
| P2.5 | Store topic clusters in `topics` table | 0.5d |
| P2.6 | Build `GET /trends/topics` endpoint with real data | 0.5d |
| P2.7 | Build `/trends` frontend page with topic cards + sparklines | 1.5d |
| P2.8 | Build video detail page `/videos/[videoId]` | 1d |

---

## Total Estimates

| Phase | Duration |
|---|---|
| Phase 1 MVP | ~4 weeks |
| Phase 2 AI Trends | ~1–1.5 weeks |

---

## Milestones

| Date | Milestone |
|---|---|
| End of Week 1 | Dev environment running; DB schema live |
| End of Week 2 | Full scoring pipeline works in isolation (unit tests pass) |
| End of Week 3 | Full pipeline callable via API; frontend rendering real data |
| End of Week 4 | MVP deployed; first real daily crawl completed |
| Phase 2 complete | Trend detection live on `/trends` page |
