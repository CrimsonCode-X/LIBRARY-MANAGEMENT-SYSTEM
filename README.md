# LibraryOS

A production-oriented digital-library discovery platform evolving from the original Python + MySQL Library Management System.

## What changed

The original project expected a person to manually enter books, members, issue transactions and returns. LibraryOS removes that physical-library assumption.

Instead, the application aggregates legitimate book metadata and reading/access information from external digital-library providers, normalizes the data, deduplicates the same work across providers, and lets users build a personal reading library.

## V1 providers

- **Open Library** — catalogue and discovery metadata
- **Project Gutenberg** — open/public-domain ebook catalogue and reading links
- **Internet Archive** — digital-library metadata and reading/access links

Google Books is planned as a Phase 2 supplementary provider.

## V1 product flow

```text
Search
  ↓
Provider aggregation
  ↓
Normalize
  ↓
Deduplicate
  ↓
Unified book result
  ↓
Read / Preview / Access at the legitimate source
  ↓
Save to personal library
  ↓
Track reading state/history
```

## Architecture

- Frontend: Next.js + TypeScript
- Backend: FastAPI + Python
- Database: PostgreSQL
- ORM: SQLAlchemy
- Migrations: Alembic
- External providers: Open Library, Project Gutenberg, Internet Archive
- Testing: Pytest + Playwright (planned)
- Deployment: Docker + GitHub Actions (planned)

See [`docs/architecture.md`](docs/architecture.md) and [`docs/implementation-plan.md`](docs/implementation-plan.md).

## Development status

| Area | Status |
|---|---|
| Legacy CLI preserved on `main` | Done |
| V1 architecture | Done |
| Provider contract | Done |
| Open Library adapter | Initial implementation |
| Internet Archive adapter | Initial implementation |
| Gutenberg catalogue adapter | Initial implementation |
| Deduplication service | Initial implementation |
| FastAPI skeleton | Done |
| PostgreSQL persistence | Next |
| Unified search API | Next |
| Next.js frontend | Next |
| Authentication | Planned |
| Personal library | Planned |
| Reading history | Planned |
| CI/CD + deployment | Planned |

## Legacy version

The original CLI implementation remains on the `main` branch. It uses Python + MySQL and supports manual book/member management, issue and return operations.
