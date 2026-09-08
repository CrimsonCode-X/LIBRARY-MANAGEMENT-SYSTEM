from __future__ import annotations

import re
import unicodedata

from app.providers.base import UnifiedBook


def normalize_text(value: str | None) -> str:
    if not value:
        return ""
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = value.lower().strip()
    return re.sub(r"[^a-z0-9]+", "", value)


def canonical_key(book: UnifiedBook) -> tuple[str, str, int | None]:
    title = normalize_text(book.title)
    author = normalize_text(book.authors[0] if book.authors else None)
    return title, author, book.publication_year


def merge_books(books: list[UnifiedBook]) -> list[UnifiedBook]:
    merged: dict[tuple[str, str, int | None], UnifiedBook] = {}
    for book in books:
        key = canonical_key(book)
        existing = merged.get(key)
        if existing is None:
            merged[key] = book
            continue
        existing.sources.extend(
            source for source in book.sources
            if source not in existing.sources
        )
        if not existing.description and book.description:
            existing.description = book.description
        if not existing.cover_url and book.cover_url:
            existing.cover_url = book.cover_url
        if not existing.isbn10 and book.isbn10:
            existing.isbn10 = book.isbn10
        if not existing.isbn13 and book.isbn13:
            existing.isbn13 = book.isbn13
        existing.subjects = list(dict.fromkeys(existing.subjects + book.subjects))[:20]
    return list(merged.values())
