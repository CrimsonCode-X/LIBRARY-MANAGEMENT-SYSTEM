import pytest

from app.providers.base import BookSource, UnifiedBook
from app.services.search import SearchService


class StubProvider:
    name = "stub"

    def __init__(self, books):
        self.books = books

    async def search(self, query: str, page: int = 1, limit: int = 20):
        return self.books

    async def get_book(self, external_id: str):
        return None


@pytest.mark.asyncio
async def test_search_prefers_title_match_and_filters_irrelevant_results():
    provider = StubProvider([
        UnifiedBook(title="Harry Potter and the Philosopher's Stone", authors=["J. K. Rowling"], sources=[BookSource("stub", "1")]),
        UnifiedBook(title="CIA Records", authors=["Harry Potter Fan Archive"], sources=[BookSource("stub", "2")]),
        UnifiedBook(title="Minecraft Maps", authors=["Community"], description="A Harry Potter themed map", sources=[BookSource("stub", "3")]),
    ])

    results = await SearchService([provider]).search("Harry Potter", limit=20)

    assert [book.title for book in results] == ["Harry Potter and the Philosopher's Stone"]


@pytest.mark.asyncio
async def test_search_survives_provider_failure():
    class FailingProvider(StubProvider):
        async def search(self, query: str, page: int = 1, limit: int = 20):
            raise RuntimeError("provider unavailable")

    good = StubProvider([
        UnifiedBook(title="Dune", authors=["Frank Herbert"], sources=[BookSource("stub", "1")])
    ])

    results = await SearchService([FailingProvider([]), good]).search("Dune")

    assert len(results) == 1
    assert results[0].title == "Dune"
