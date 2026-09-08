from fastapi import FastAPI

from app.api.v1.search import router as search_router

app = FastAPI(
    title="LibraryOS API",
    version="0.2.0",
    description="Unified digital-library discovery API.",
)

app.include_router(search_router, prefix="/api/v1")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
