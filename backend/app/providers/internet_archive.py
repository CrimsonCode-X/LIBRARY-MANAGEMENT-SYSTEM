from __future__ import annotations

import httpx

from .base import AccessType, BookProvider, BookSource, UnifiedBook


class InternetArchiveProvider:
    name = "internet_archive"
    search_url = "https://archive.org/advancedsearch.php"
    metadata_url = "https://archive.org/metadata"

    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def search(self, query: str, page: int = 1, limit: int = 20) -> list[UnifiedBook]:
        response = await self.client.get(
            self.search_url,
            params={
                "q": f"mediatype:texts AND ({query})",
                "fl[]": ["identifier", "title", "creator", "description", "year", "language", "subject"],
                "rows": limit,
                "page": page,
                "output": "json",
            },
            timeout=10.0,
        )
        response.raise_for_status()
        docs = response.json().get("response", {}).get("docs", [])
        return [self._normalize(doc) for doc in docs]

    async def get_book(self, external_id: str) -> UnifiedBook | None:
        response = await self.client.get(f"{self.metadata_url}/{external_id}", timeout=10.0)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return self._normalize(response.json().get("metadata", {}) | {"identifier": external_id})

    def _normalize(self, doc: dict) -> UnifiedBook:
        identifier = doc.get("identifier") or ""
        creator = doc.get("creator") or []
        if isinstance(creator, str):
            creator = [creator]
        subjects = doc.get("subject") or []
        if isinstance(subjects, str):
            subjects = [subjects]
        year = None
        raw_year = str(doc.get("year") or "")
        if raw_year[:4].isdigit():
            year = int(raw_year[:4])
        return UnifiedBook(
            title=doc.get("title") or identifier,
            authors=creator,
            description=doc.get("description"),
            publication_year=year,
            language=(doc.get("language") or None),
            subjects=subjects[:20],
            sources=[
                BookSource(
                    self.name,
                    identifier,
                    f"https://archive.org/details/{identifier}",
                    f"https://archive.org/details/{identifier}",
                    AccessType.UNKNOWN,
                )
            ],
        )
