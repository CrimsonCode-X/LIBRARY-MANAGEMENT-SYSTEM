from fastapi import FastAPI

app = FastAPI(
    title="LibraryOS API",
    version="0.2.0",
    description="Unified digital-library discovery API.",
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
