from __future__ import annotations

import asyncio

from app.providers.base import BookProvider, UnifiedBook
from app.services.deduplication import merge_books


class SearchService:
    def __init__(self, providers: list[BookProvider]):
        self.providers = providers

    async def search(self, query: str, page: int = 1, limit: int = 20) -> list[UnifiedBook]:
        tasks = [provider.search(query, page=page, limit=limit) for provider in self.providers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        books: list[UnifiedBook] = []
        for result in results:
            if isinstance(result, Exception):
                continue
            books.extend(result)
        return merge_books(books)
