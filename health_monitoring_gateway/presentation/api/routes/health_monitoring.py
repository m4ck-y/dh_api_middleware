"""Health Monitoring sub-app with its own documentation."""

from __future__ import annotations

from fastapi import FastAPI

from health_monitoring_gateway.presentation.api.routes.gw import (
    batch,
    measure_groups,
    measure_types,
    measurements,
    monitoring_backend,
    people,
    relations,
    reports,
    units,
)


def create_health_monitoring_app() -> FastAPI:
    """Create sub-app for Health Monitoring microservice.

    Each sub-app has its own /docs at /health_monitoring/docs

    Usage:
        from health_monitoring import create_health_monitoring_app
        app = FastAPI()
        app.mount("/health_monitoring", create_health_monitoring_app())
    """
    app = FastAPI(
        title="Health Monitoring API",
        version="0.1.0",
        description="Health Monitoring microservice - proxy to backend",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    app.include_router(relations.router)
    app.include_router(measure_types.router)
    app.include_router(measure_groups.router)
    app.include_router(units.router)
    app.include_router(people.router)
    app.include_router(measurements.router)
    app.include_router(reports.router)
    app.include_router(batch.router)
    app.include_router(monitoring_backend.router)

    return app
