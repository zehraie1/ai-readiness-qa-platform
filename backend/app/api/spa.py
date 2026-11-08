"""Serve the built React SPA from FastAPI (single origin: first-party session cookie, no CORS)."""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

RESERVED_PREFIXES = ("api/", "health", "ready", "docs", "openapi.json")


def mount_spa(app: FastAPI, dist: Path) -> None:
    index = dist / "index.html"
    if not index.is_file():
        raise RuntimeError(f"SERVE_FRONTEND is enabled but {index} does not exist; run the frontend build")
    # Hashed, immutable build assets.
    app.mount("/assets", StaticFiles(directory=dist / "assets"), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def spa(full_path: str) -> FileResponse:
        if full_path.startswith(RESERVED_PREFIXES):
            raise HTTPException(status_code=404)
        candidate = (dist / full_path).resolve()
        if full_path and candidate.is_file() and candidate.is_relative_to(dist.resolve()):
            return FileResponse(candidate)
        # Client-side route: always return the app shell, never cached.
        return FileResponse(index, headers={"Cache-Control": "no-cache"})
