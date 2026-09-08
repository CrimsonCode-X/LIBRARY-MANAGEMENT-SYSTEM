# LibraryOS V1 Architecture

## Product

LibraryOS is a digital-library discovery and personal reading platform. It aggregates legitimate book metadata and access information from external providers instead of maintaining a manually entered physical inventory.

## Providers

V1 providers:

- Open Library — primary catalogue/discovery metadata
- Project Gutenberg — open/public-domain ebook source
- Internet Archive — digital-library metadata and reading/access source

Phase 2:

- Google Books — supplementary metadata and preview/full-view information

## Architecture

```text
Next.js frontend
       |
       | REST / JSON
       v
FastAPI backend
       |
       +--------------------+
       |                    |
       v                    v
PostgreSQL             Provider layer
                            |
                 +----------+----------+
                 |          |          |
            Open Library  Gutenberg  Internet Archive
                            |
                       normalization
                            |
                       deduplication
```

## Core principles

1. External providers are sources, not interchangeable databases.
2. Provider-specific schemas never leak into API/domain models.
3. A book is a canonical work in our database; provider records are attached as `book_sources`.
4. Reading availability is source-specific and may change; it must not be represented by a permanent `books.available` flag.
5. Provider failures degrade gracefully.
6. External responses are cached where appropriate.
7. V1 links users to legitimate provider reading/access destinations rather than mirroring copyrighted content.
8. Search results are normalized and deduplicated before being returned to the frontend.

## V1 domain

- User
- Book
- Author
- Source
- BookSource
- Category
- UserLibraryEntry
- ReadingSession

Physical copies, loans, returns and fines are intentionally removed from V1 because they belong to a physical-library workflow.
