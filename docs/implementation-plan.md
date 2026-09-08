# LibraryOS V1 Implementation Plan

## Milestones

### M0 — Preserve
- Keep current CLI application intact on `main`.
- Develop the new platform on `refactor/digital-library-v1`.
- Record the legacy system as v0.1.

### M1 — Provider contracts
- Define provider interface.
- Define unified book/source models.
- Add provider error and timeout types.

### M2 — Provider integrations
- Implement Open Library adapter.
- Implement Project Gutenberg adapter.
- Implement Internet Archive adapter.
- Normalize each provider into the common schema.

### M3 — Entity resolution
- Normalize title/author text.
- Match ISBNs where present.
- Match normalized title + author + publication year.
- Add deterministic deduplication tests.

### M4 — Persistence
- Add PostgreSQL.
- Add SQLAlchemy models.
- Add Alembic migrations.
- Add repository/service layer.

### M5 — Unified search API
- `GET /api/v1/search`
- `GET /api/v1/books/{id}`
- `GET /api/v1/books/{id}/sources`
- Pagination, ranking, provider status and graceful degradation.

### M6 — Frontend
- Next.js + TypeScript.
- Homepage search.
- Search results.
- Unified book details page.
- Source/access cards.

### M7 — Accounts
- Registration/login/logout/me.
- Personal library.
- Want-to-read / reading / completed states.

### M8 — Reading history
- Reading sessions.
- Last-read timestamp.
- Progress where the selected source supports meaningful tracking.

### M9 — Reliability
- Provider caching.
- Timeouts/retries.
- Rate-limit handling.
- Scheduled metadata refresh.
- Health endpoint.

### M10 — Quality
- Unit tests.
- Provider contract tests.
- API integration tests.
- Playwright end-to-end flow.

### M11 — Delivery
- Docker Compose.
- GitHub Actions.
- Production environment configuration.
- Deployment.
- README and architecture documentation.

## Manual-input gates

These are the only planned gates that require the owner to intervene:

1. **External service credentials:** provide API keys only if a provider requires them for the chosen production setup. Open Library/Gutenberg/Internet Archive should not be made dependent on invented credentials.
2. **Database deployment:** production PostgreSQL connection string/credentials must be supplied by the owner or chosen hosting account.
3. **Deployment accounts:** the owner must authenticate with the selected hosting/GitHub/Vercel accounts when deployment requires browser authorization.
4. **Production domain:** optional; owner must provide the domain if a custom domain is desired.
5. **Product decisions that cannot be inferred safely:** branding/name changes, whether to keep the legacy CLI files after V1, and any licensing/terms acceptance required by a provider account.

Everything else should be implemented autonomously and surfaced as a status item rather than blocking progress.
