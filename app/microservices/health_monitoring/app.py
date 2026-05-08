"""Health Monitoring API - Proxy to backend.

## Test UI

Preview: [{service_url}]({service_url})

## Overview

Proxies requests to Health Monitoring backend service.
Manages people, measurements, measure types, units, and reports.

## Endpoints

- People CRUD
- Measurements CRUD
- Measure Types CRUD
- Measure Groups CRUD
- Units CRUD
- Reports & aggregations
- Batch operations

## Backend

Proxies to: [{service_url}/docs]({service_url}/docs)
"""

from __future__ import annotations

from fastapi import FastAPI

from app.settings import settings

HEALTH_MONITORING_URL = settings.SERVICE_HEALTH_MONITORING_URL.rstrip("/")
_DESC = __doc__.replace("{service_url}", HEALTH_MONITORING_URL) if HEALTH_MONITORING_URL else __doc__


def create_app(root_path: str = "") -> FastAPI:
    """Create Health Monitoring sub-app with its own /docs."""
    app = FastAPI(
        title="Health Monitoring API",
        version="0.1.0",
        description=_DESC,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        root_path=root_path,
    )

    from app.microservices.health_monitoring.routes.v1 import (
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
