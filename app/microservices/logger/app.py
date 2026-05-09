"""Observability Gateway - Telemetry ingestion.

## Test UI

Preview: [{service_url}]({service_url})

## Overview

Centralized system for log and event ingestion.

## Endpoints

- Events
- Logs
- Metrics
- Traces
- Batch

## Backend

Proxies to: [{service_url}/docs]({service_url}/docs)
"""

from __future__ import annotations

from fastapi import FastAPI

from app.settings import settings

LOGGER_URL = settings.SERVICE_LOGGER_URL.rstrip("/")
_DESC = __doc__.replace("{service_url}", LOGGER_URL) if LOGGER_URL else __doc__


def create_app(root_path: str = "") -> FastAPI:
    """Create Logger Tracer sub-app with its own /docs."""
    app = FastAPI(
        title="Observability Gateway API",
        version="0.1.0",
        description=_DESC,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        root_path=root_path,
    )

    from app.microservices.logger.routes.v1 import (
        events,
        logs,
        metrics,
        traces,
        batch,
    )

    app.include_router(events.router)
    app.include_router(logs.router)
    app.include_router(metrics.router)
    app.include_router(traces.router)
    app.include_router(batch.router)

    return app
