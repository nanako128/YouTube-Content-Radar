# 010 – Non-Functional Requirements & Other Considerations

---

## 1. Performance Requirements

| Metric | Target | Implementation |
|---|---|---|
| API response time (cached) | < 200 ms | Redis 24h cache for all ranking endpoints |
| API response time (uncached) | < 1,000 ms | Indexed DB queries |
| Daily crawl completion | < 60 minutes | Async crawl + batched API calls |
| Frontend First Contentful Paint | < 1.5 s | Next.js SSR; cached API data |
| Frontend Time to Interactive | < 3 s | Lightweight JS bundle |

---

## 2. Reliability & Availability

- **Crawl failure handling:** If a daily crawl fails mid-way, the last successful ranking remains cached in Redis. Users see stale data with a "Last updated: X hours ago" indicator.
- **Partial failures:** If a single channel times out during crawl, log the error and continue with the next channel. Do not fail the entire task.
- **YouTube API quota guard:** Track unit usage per run. If estimated remaining quota < 500 units, abort `search.list` calls and log a warning. Never abort comment fetching once started (higher priority).
- **Celery task retry:** All Celery tasks should have `max_retries=3, countdown=60` on transient failures (network timeouts).
- **DB connection resilience:** Use SQLAlchemy connection pool with `pool_recycle=1800`.

---

## 3. Security

| Area | Requirement |
|---|---|
| YouTube API Key | Stored in environment variable only; never committed to git |
| `.env` file | Listed in `.gitignore`; `.env.example` committed instead |
| API Authentication | Phase 1: IP whitelist or optional `X-API-Key` header. Phase 2: proper auth. |
| SQL Injection | Prevented by SQLAlchemy ORM + parameterized queries only |
| Rate limiting | FastAPI middleware: 100 req/min per IP (Phase 2) |
| CORS | Backend allows only `http://localhost:3000` (dev) and production frontend domain |

---

## 4. Observability & Logging

| Layer | Tool | Notes |
|---|---|---|
| Backend logs | Python `logging` → stdout | Structured JSON in production |
| Celery task logs | Celery task result backend (Redis) | Track success/failure/duration |
| Error tracking | Sentry (optional, Phase 2) | |
| DB query logging | SQLAlchemy `echo=False` in prod | Enable debug logging only locally |
| Health endpoint | `GET /health` | Returns last crawl time, DB record counts |

---

## 5. Data Retention

| Data | Retention Policy |
|---|---|
| `videos` | Retain indefinitely (historical reference) |
| `comments` | Retain for 90 days (disk management) |
| `rankings` | Retain for 30 days of daily snapshots |
| `topics` | Retain indefinitely |
| Redis cache | Auto-expires (TTL = 24h) |

---

## 6. Internationalization (i18n)

- **Phase 1:** UI language is English only.
- **Phase 2:** If Japanese content team uses the dashboard, consider adding Japanese UI strings. The app structure should support `next-intl` for this.
- Video content itself may be in any language; the system does not filter by language in Phase 1.

---

## 7. Accessibility (a11y)

- All data tables must be keyboard-navigable.
- Score badges must not rely solely on color (include numeric value).
- Images (thumbnails) must have `alt` attributes.
- Minimum color contrast ratio: WCAG AA (4.5:1 for normal text).

---

## 8. Configuration & Maintainability

Key values that should be easily configurable (in `config.py`, not hardcoded):

| Config Key | Default | Notes |
|---|---|---|
| `CURATED_CHANNEL_IDS` | `[]` | List of channel IDs to crawl |
| `DISCOVERY_KEYWORDS` | `["AI", "Gen Z", ...]` | Keyword list for weekly search |
| `BUZZ_SCORE_THRESHOLD` | `70` | Min score to trigger related video expansion |
| `VIRAL_SPIKE_MULTIPLIER` | `3` | Channel avg velocity multiplier for viral flag |
| `COMMENT_LIMIT_PER_VIDEO` | `200` | Max comments fetched per video |
| `TOP_N_FOR_COMMENT_FETCH` | `20` | Top N videos that get full comment analysis |
| `MIN_CHANNEL_SUBSCRIBERS` | `10000` | Filter for discovered channels |
| `RANKING_CACHE_TTL` | `86400` | Redis TTL in seconds (24h) |

---

## 9. Future Considerations

| Feature | Notes |
|---|---|
| Clip Score | Score predicting short-form clipping potential (e.g., video length, density of key moments) |
| Multi-platform | Extend crawler to TikTok or Instagram Reels data |
| Notification | Slack/email alert when a video exceeds buzz_score threshold |
| User accounts | Allow team members to save/favorite videos |
| Annotation | Let editors mark which videos were actually used for content |
| A/B scoring | Test alternative scoring formulas with manual validation data |
