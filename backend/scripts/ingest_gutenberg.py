from __future__ import annotations

import asyncio

from app.db import SessionLocal
from app.providers.gutenberg import GutenbergProvider
from app.services.gutenberg_ingestion import ingest_gutenberg_catalogue
import httpx


async def main() -> None:
    async with httpx.AsyncClient(
        headers={"User-Agent": "LibraryOS/0.1 (catalogue ingestion)"}
    ) as client:
        provider = GutenbergProvider(client)
        print("Downloading Project Gutenberg catalogue...")
        csv_text = await provider.download_catalogue()

    with SessionLocal() as session:
        count = ingest_gutenberg_catalogue(session, csv_text)

    print(f"Ingested {count} Project Gutenberg records.")


if __name__ == "__main__":
    asyncio.run(main())
