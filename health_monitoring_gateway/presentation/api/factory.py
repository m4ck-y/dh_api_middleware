"""Assemble the FastAPI application (composition root for HTTP)."""

from __future__ import annotations

from contextlib import asynccontextmanager

import httpx
from fastapi import APIRouter, FastAPI

from health_monitoring_gateway.infrastructure.http.httpx_health_monitoring_backend import (
    HttpxHealthMonitoringBackend,
)
from health_monitoring_gateway.infrastructure.settings import get_settings
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
from health_monitoring_gateway.presentation.api.routes.middleware_health import (
    router as middleware_health_router,
)


@asynccontextmanager
async def _lifespan(app: FastAPI):
    settings = get_settings()
    timeout = httpx.Timeout(60.0)
    limits = httpx.Limits(max_keepalive_connections=20, max_connections=100)
    async with httpx.AsyncClient(
        timeout=timeout,
        limits=limits,
        follow_redirects=False,
    ) as client:
        app.state.health_monitoring_backend = HttpxHealthMonitoringBackend(
            settings=settings,
            client=client,
        )
        yield


def _build_health_monitoring_router() -> APIRouter:
    """
    Include order: static paths before dynamic variants are handled per-router.
    `relations` first keeps `/measure/types-groups` before other `/measure/types/...` routes.
    """
    r = APIRouter(prefix="/health_monitoring")
    r.include_router(relations.router)
    r.include_router(measure_types.router)
    r.include_router(measure_groups.router)
    r.include_router(units.router)
    r.include_router(people.router)
    r.include_router(measurements.router)
    r.include_router(reports.router)
    r.include_router(batch.router)
    r.include_router(monitoring_backend.router)
    return r


def create_app() -> FastAPI:
    app = FastAPI(
        title="API Middleware — Health Monitoring Gateway",
        version="0.1.0",
        lifespan=_lifespan,
        description=(
            "Middleware in front of Health Monitoring. "
            "`GET /health` is this process only. "
            "Routes under `/health_monitoring` call the Health Monitoring backend over HTTP; "
            "Pydantic schemas live in `health_monitoring_gateway.domain.schemas` — align them with "
            "`health_monitoring/backend/app/schemas` when the backend evolves."
        ),
    )
    app.include_router(middleware_health_router)
    app.include_router(_build_health_monitoring_router())
    return app
