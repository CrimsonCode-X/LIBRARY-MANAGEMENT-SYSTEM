from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol


class AccessType(str, Enum):
    OPEN = "OPEN"
    PUBLIC_DOMAIN = "PUBLIC_DOMAIN"
    FULL_VIEW = "FULL_VIEW"
    PREVIEW = "PREVIEW"
    BORROW = "BORROW"
    PURCHASE = "PURCHASE"
    NONE = "NONE"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class BookSource:
    provider: str
    external_id: str
    source_url: str | None = None
    reading_url: str | None = None
    access_type: AccessType = AccessType.UNKNOWN
    formats: tuple[str, ...] = ()


@dataclass
class UnifiedBook:
    title: str
    authors: list[str] = field(default_factory=list)
    description: str | None = None
    publication_year: int | None = None
    language: str | None = None
    isbn10: str | None = None
    isbn13: str | None = None
    cover_url: str | None = None
    subjects: list[str] = field(default_factory=list)
    sources: list[BookSource] = field(default_factory=list)


class BookProvider(Protocol):
    name: str

    async def search(self, query: str, page: int = 1, limit: int = 20) -> list[UnifiedBook]:
        ...

    async def get_book(self, external_id: str) -> UnifiedBook | None:
        ...
