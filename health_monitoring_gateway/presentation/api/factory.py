"""FastAPI app factory with sub-apps for each microservice."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from health_monitoring_gateway.presentation.api.routes.health_monitoring import (
    create_health_monitoring_app,
)
from health_monitoring_gateway.presentation.api.routes.middleware_health import (
    router as middleware_health_router,
)


def create_app() -> FastAPI:
    """Create the main gateway application.

    Each microservice is mounted as a sub-app with its own /docs.
    - Main gateway: http://localhost:8080/docs
    - Health Monitoring: http://localhost:8080/health_monitoring/docs
    """
    app = FastAPI(
        title="API Gateway — Middleware",
        version="0.1.0",
        description="""
## Overview

Central gateway/middleware for multiple microservices.

## Services

| Service | Docs | Prefix |
|---------|------|--------|
| Main Gateway | [/docs](/docs) | `/` |
| Health Monitoring | [/health_monitoring/docs](/health_monitoring/docs) | `/health_monitoring` |

## Security

This gateway has **NO database access**. It's a stateless HTTP proxy.
If compromised, the attacker only accesses this proxy, not the actual services.
        """,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(middleware_health_router)

    health_monitoring_app = create_health_monitoring_app()
    app.mount("/health_monitoring", health_monitoring_app)

    return app
