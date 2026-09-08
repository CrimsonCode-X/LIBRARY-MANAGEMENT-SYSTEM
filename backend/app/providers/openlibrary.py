from __future__ import annotations

import httpx

from .base import AccessType, BookProvider, BookSource, UnifiedBook


class OpenLibraryProvider:
    name = "openlibrary"
    base_url = "https://openlibrary.org"
    search_fields = (
        "key,title,author_name,first_publish_year,publish_year,language,isbn,"
        "cover_i,subject,ia,has_fulltext,public_scan_b,availability"
    )

    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def search(self, query: str, page: int = 1, limit: int = 20) -> list[UnifiedBook]:
        response = await self.client.get(
            f"{self.base_url}/search.json",
            params={
                "q": query.strip(),
                "page": page,
                "limit": limit,
                "fields": self.search_fields,
            },
            timeout=8.0,
        )
        response.raise_for_status()
        docs = response.json().get("docs", [])
        return [self._normalize(doc) for doc in docs if doc.get("title")]

    async def get_book(self, external_id: str) -> UnifiedBook | None:
        response = await self.client.get(f"{self.base_url}/works/{external_id}.json", timeout=8.0)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        data = response.json()
        title = data.get("title")
        if not title:
            return None
        authors = [a.get("author", {}).get("key", "").split("/")[-1] for a in data.get("authors", [])]
        return UnifiedBook(
            title=title,
            authors=authors,
            description=self._description(data.get("description")),
            cover_url=(f"https://covers.openlibrary.org/b/id/{data['covers'][0]}-L.jpg" if data.get("covers") else None),
            subjects=[s for s in data.get("subjects", [])[:20] if isinstance(s, str)],
            sources=[BookSource(self.name, external_id, f"{self.base_url}/works/{external_id}", access_type=AccessType.UNKNOWN)],
        )

    def _normalize(self, doc: dict) -> UnifiedBook:
        work_key = (doc.get("key") or "").split("/")[-1]
        authors = doc.get("author_name") or []
        years = doc.get("publish_year") or []
        year = doc.get("first_publish_year") or (min(years) if years else None)
        isbn = doc.get("isbn") or []
        isbn10 = next((x for x in isbn if len(x.replace("-", "")) == 10), None)
        isbn13 = next((x for x in isbn if len(x.replace("-", "")) == 13), None)
        cover = doc.get("cover_i")
        access_type, reading_url = self._access(doc)
        return UnifiedBook(
            title=doc.get("title") or "Untitled",
            authors=authors,
            publication_year=year,
            language=(doc.get("language") or [None])[0],
            isbn10=isbn10,
            isbn13=isbn13,
            cover_url=f"https://covers.openlibrary.org/b/id/{cover}-L.jpg" if cover else None,
            subjects=(doc.get("subject") or [])[:20],
            sources=[
                BookSource(
                    self.name,
                    work_key or doc.get("edition_key", [""])[0],
                    f"https://openlibrary.org{doc.get('key', '')}",
                    reading_url,
                    access_type,
                )
            ],
        )

    @staticmethod
    def _access(doc: dict) -> tuple[AccessType, str | None]:
        availability = doc.get("availability") or {}
        status = availability.get("status") if isinstance(availability, dict) else None
        if status == "open":
            return AccessType.OPEN, availability.get("url") or availability.get("reading_url")
        if status == "borrowable":
            return AccessType.BORROW, availability.get("url") or availability.get("reading_url")
        if doc.get("public_scan_b"):
            return AccessType.FULL_VIEW, f"https://openlibrary.org{doc.get('key', '')}"
        if doc.get("has_fulltext"):
            return AccessType.FULL_VIEW, f"https://openlibrary.org{doc.get('key', '')}"
        return AccessType.UNKNOWN, None

    @staticmethod
    def _description(value: object) -> str | None:
        if isinstance(value, str):
            return value
        if isinstance(value, dict):
            return value.get("value")
        return None
