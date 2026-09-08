from fastapi import APIRouter, Query
import httpx

from app.providers.internet_archive import InternetArchiveProvider
from app.providers.openlibrary import OpenLibraryProvider
from app.services.search import SearchService

router = APIRouter(prefix="/search", tags=["search"])


@router.get("")
async def search_books(
    q: str = Query(min_length=2, max_length=200),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=50),
):
    async with httpx.AsyncClient(headers={"User-Agent": "LibraryOS/0.2 (+https://github.com/CrimsonCode-X/LIBRARY-MANAGEMENT-SYSTEM)"}) as client:
        service = SearchService([
            OpenLibraryProvider(client),
            InternetArchiveProvider(client),
        ])
        books = await service.search(q, page=page, limit=limit)
    return {"query": q, "page": page, "limit": limit, "count": len(books), "results": books}
