from __future__ import annotations

import csv
import io

import httpx

from .base import AccessType, BookProvider, BookSource, UnifiedBook


class GutenbergProvider:
    """Project Gutenberg provider backed by its official catalogue CSV.

    Gutenberg publishes a machine-readable catalogue rather than a conventional
    search API. V1 therefore treats the catalogue as an ingestion source. The
    search method expects the catalogue rows to be loaded by the application
    layer; `search_catalogue` is provided for local/in-memory use.
    """

    name = "gutenberg"
    catalogue_url = "https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv"

    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def download_catalogue(self) -> str:
        response = await self.client.get(self.catalogue_url, timeout=30.0)
        response.raise_for_status()
        return response.text

    def search_catalogue(self, csv_text: str, query: str, limit: int = 20) -> list[UnifiedBook]:
        terms = [term.lower() for term in query.split() if term]
        rows = csv.DictReader(io.StringIO(csv_text))
        results: list[UnifiedBook] = []
        for row in rows:
            haystack = " ".join([
                row.get("Title") or row.get("title") or "",
                row.get("Authors") or row.get("author") or "",
                row.get("Subjects") or row.get("subject") or "",
            ]).lower()
            if terms and not all(term in haystack for term in terms):
                continue
            results.append(self._normalize(row))
            if len(results) >= limit:
                break
        return results

    async def search(self, query: str, page: int = 1, limit: int = 20) -> list[UnifiedBook]:
        raise NotImplementedError("Use catalogue ingestion for Gutenberg search")

    async def get_book(self, external_id: str) -> UnifiedBook | None:
        book_id = str(external_id).strip()
        if not book_id.isdigit():
            return None
        return UnifiedBook(
            title=f"Project Gutenberg #{book_id}",
            sources=[
                BookSource(
                    self.name,
                    book_id,
                    f"https://www.gutenberg.org/ebooks/{book_id}",
                    f"https://www.gutenberg.org/ebooks/{book_id}",
                    AccessType.OPEN,
                    ("html", "epub", "txt"),
                )
            ],
        )

    def _normalize(self, row: dict) -> UnifiedBook:
        book_id = (row.get("Text#") or row.get("EBook-No.") or row.get("ebook_no") or "").strip()
        title = (row.get("Title") or row.get("title") or "Untitled").strip()
        authors_raw = (row.get("Authors") or row.get("author") or "").strip()
        authors = [a.strip() for a in authors_raw.split(";") if a.strip()]
        languages = (row.get("Language") or row.get("language") or "").strip()
        return UnifiedBook(
            title=title,
            authors=authors,
            language=languages.split(";")[0].strip() if languages else None,
            sources=[
                BookSource(
                    self.name,
                    book_id,
                    f"https://www.gutenberg.org/ebooks/{book_id}",
                    f"https://www.gutenberg.org/ebooks/{book_id}",
                    AccessType.OPEN,
                    ("html", "epub", "txt"),
                )
            ],
        )
