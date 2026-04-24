"""Observability Gateway - Telemetry ingestion.

## Overview

Centralized system for log and event ingestion.

## Endpoints

- Events
- Logs
- Metrics
- Traces
- Batch

## Backend

Proxies to: `{settings.SERVICE_LOGGER_TRACER_URL}`
"""

from __future__ import annotations

from fastapi import FastAPI

from app.settings import settings

LOGGER_TRACER_URL = settings.SERVICE_LOGGER_TRACER_URL.rstrip("/")


def create_app() -> FastAPI:
    """Create Logger Tracer sub-app with its own /docs."""
    app = FastAPI(
        title="Observability Gateway API",
        version="0.1.0",
        description=__doc__,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    from app.microservices.logger_tracer.routes import (
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
