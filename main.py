"""Entry module: ASGI app and optional `python main.py` server."""

from __future__ import annotations

from health_monitoring_gateway.infrastructure.settings import get_settings
from health_monitoring_gateway.presentation.api.factory import create_app

app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.gateway_listen_host,
        port=settings.gateway_listen_port,
        reload=False,
    )
