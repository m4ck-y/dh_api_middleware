"""Entry module: ASGI app and optional `python entrypoint.py` server."""

from __future__ import annotations

from app.gateway import create_app
from app.settings import settings

app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.entrypoint:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=False,
    )
