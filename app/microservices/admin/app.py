"""Admin API - High-privilege database operations.

## Test UI

Preview: [{service_url}]({service_url})

## Overview

Proxies admin operations to dh_admin backend.
Provides endpoints for schema recreation and DB seeding.

## Endpoints

- POST /v1/db/recreate — Drop and recreate all schemas
- POST /v1/db/seed-all — Seed catalogs + admin user

## Backend

Proxies to: [{service_url}/docs]({service_url}/docs)
"""

from __future__ import annotations

from fastapi import APIRouter, FastAPI

from app.http_client import request
from app.settings import settings

ADMIN_URL = settings.SERVICE_ADMIN_URL.rstrip("/")
_DESC = __doc__.replace("{service_url}", ADMIN_URL) if ADMIN_URL else __doc__


router = APIRouter(tags=["Admin"])


@router.post("/v1/db/recreate")
async def recreate_schemas():
    status, data = await request(ADMIN_URL, "POST", "v1/db/recreate")
    return data


@router.post("/v1/db/seed-all")
async def seed_all():
    status, data = await request(ADMIN_URL, "POST", "v1/db/seed-all")
    return data


def create_app(root_path: str = "") -> FastAPI:
    app = FastAPI(
        title="Admin API",
        version="0.1.0",
        description=_DESC,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        root_path=root_path,
    )

    app.include_router(router)

    return app