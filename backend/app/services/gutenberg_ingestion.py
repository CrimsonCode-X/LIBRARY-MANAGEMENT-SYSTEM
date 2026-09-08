from __future__ import annotations

import csv
import io
from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Author, Book, BookAuthor, BookSource, Source
from app.providers.base import AccessType
from app.services.deduplication import normalize_text


GUTENBERG_PROVIDER = "gutenberg"


def _first(row: dict, *keys: str) -> str:
    for key in keys:
        value = (row.get(key) or "").strip()
        if value:
            return value
    return ""


def _year(row: dict) -> int | None:
    for key in ("Copyright Year", "copyright_year"):
        value = _first(row, key)
        if value.isdigit() and len(value) == 4:
            return int(value)
    return None


def _authors(row: dict) -> list[str]:
    raw = _first(row, "Authors", "author")
    return [part.strip() for part in raw.split(";") if part.strip()]


def _subjects(row: dict) -> list[str]:
    raw = _first(row, "Subjects", "subject")
    return [part.strip() for part in raw.split(" -- ") if part.strip()]


def _rows(csv_text: str) -> Iterable[dict]:
    yield from csv.DictReader(io.StringIO(csv_text))


def ingest_gutenberg_catalogue(session: Session, csv_text: str) -> int:
    """Upsert Project Gutenberg catalogue rows into the unified catalogue.

    The official CSV is treated as the provider catalogue. Existing Gutenberg
    records are updated by provider/external ID; new rows are matched to an
    existing canonical book by normalized title + author before a new book is
    created.
    """
    provider = session.scalar(select(Source).where(Source.provider == GUTENBERG_PROVIDER))
    if provider is None:
        provider = Source(provider=GUTENBERG_PROVIDER)
        session.add(provider)
        session.flush()

    ingested = 0
    for row in _rows(csv_text):
        external_id = _first(row, "Text#", "EBook-No.", "ebook_no")
        title = _first(row, "Title", "title")
        authors = _authors(row)
        if not external_id or not title:
            continue

        canonical_title = normalize_text(title)
        author_key = normalize_text(authors[0]) if authors else ""
        book = _find_book(session, canonical_title, author_key)
        if book is None:
            book = Book(
                canonical_title=title,
                publication_year=_year(row),
                language=_first(row, "Language", "language").split(";")[0].strip() or None,
            )
            session.add(book)
            session.flush()

        for author_name in authors:
            author = session.scalar(select(Author).where(Author.name == author_name))
            if author is None:
                author = Author(name=author_name)
                session.add(author)
                session.flush()
            exists = session.scalar(
                select(BookAuthor).where(
                    BookAuthor.book_id == book.id,
                    BookAuthor.author_id == author.id,
                )
            )
            if exists is None:
                session.add(BookAuthor(book_id=book.id, author_id=author.id))

        source_row = session.scalar(
            select(BookSource).where(
                BookSource.source_id == provider.id,
                BookSource.external_id == external_id,
            )
        )
        source_url = f"https://www.gutenberg.org/ebooks/{external_id}"
        metadata = {
            "subjects": _subjects(row),
            "copyright_year": _first(row, "Copyright Year", "copyright_year") or None,
        }
        if source_row is None:
            session.add(
                BookSource(
                    book_id=book.id,
                    source_id=provider.id,
                    external_id=external_id,
                    source_url=source_url,
                    reading_url=source_url,
                    access_type=AccessType.OPEN.value,
                    formats=["html", "epub", "txt"],
                    metadata_json=metadata,
                )
            )
        else:
            source_row.book_id = book.id
            source_row.source_url = source_url
            source_row.reading_url = source_url
            source_row.access_type = AccessType.OPEN.value
            source_row.formats = ["html", "epub", "txt"]
            source_row.metadata_json = metadata

        ingested += 1

    session.commit()
    return ingested


def _find_book(session: Session, canonical_title: str, author_key: str) -> Book | None:
    if not canonical_title:
        return None

    candidates = session.scalars(
        select(Book).where(Book.canonical_title.ilike(f"%{canonical_title}%"))
    ).all()
    if not candidates:
        return None
    if not author_key:
        return candidates[0]

    for candidate in candidates:
        author_names = session.scalars(
            select(Author.name)
            .join(BookAuthor, BookAuthor.author_id == Author.id)
            .where(BookAuthor.book_id == candidate.id)
        ).all()
        if any(author_key == normalize_text(name) for name in author_names):
            return candidate
    return None
