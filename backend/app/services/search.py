from __future__ import annotations

import asyncio
import logging
import re

from app.providers.base import BookProvider, UnifiedBook
from app.services.deduplication import merge_books, normalize_text

logger = logging.getLogger(__name__)


class SearchService:
    def __init__(self, providers: list[BookProvider]):
        self.providers = providers

    async def search(self, query: str, page: int = 1, limit: int = 20) -> list[UnifiedBook]:
        tasks = [provider.search(query, page=page, limit=limit) for provider in self.providers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        books: list[UnifiedBook] = []
        for provider, result in zip(self.providers, results):
            if isinstance(result, Exception):
                logger.warning("Book provider %s failed during search: %s", provider.name, result)
                continue
            books.extend(result)

        relevant = [book for book in books if self._relevance_score(query, book) > 0]
        merged = merge_books(relevant)
        merged.sort(key=lambda book: self._relevance_score(query, book), reverse=True)
        return merged[:limit]

    @staticmethod
    def _relevance_score(query: str, book: UnifiedBook) -> int:
        query_clean = normalize_text(query)
        if not query_clean:
            return 0

        title = normalize_text(book.title)
        authors = [normalize_text(author) for author in book.authors]
        terms = [term for term in re.findall(r"[a-z0-9]+", query.lower()) if term]

        score = 0
        if title == query_clean:
            score += 100
        elif query_clean in title:
            score += 75

        matched_title_terms = sum(1 for term in terms if term in title)
        score += matched_title_terms * 20

        score += sum(1 for author in authors if query_clean in author) * 45
        score += sum(1 for term in terms if any(term in author for author in authors)) * 10

        # Subjects/descriptions are intentionally not sufficient to make a result
        # relevant: a book mentioning "Harry Potter" in its metadata should not
        # outrank an actual Harry Potter title.
        return score
