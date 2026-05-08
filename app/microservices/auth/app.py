"""Auth API - Authentication and user profile.

## Test UI

Preview: [{service_url}]({service_url})

## Overview

Handles login, logout, token refresh, and enriched user profile (/me).
Uses HttpOnly cookies for stateless JWT.

## Endpoints

- POST /login
- POST /refresh
- POST /logout
- GET /me

## Backend

Proxies to: [{service_url}/docs]({service_url}/docs)
"""

from __future__ import annotations

from fastapi import FastAPI

from app.settings import settings

AUTH_URL = settings.SERVICE_AUTH_URL.rstrip("/")
_DESC = __doc__.replace("{service_url}", AUTH_URL) if AUTH_URL else __doc__


def create_app(root_path: str = "") -> FastAPI:
    app = FastAPI(
        title="Auth API",
        version="0.1.0",
        description=_DESC,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        root_path=root_path,
    )

    from app.microservices.auth.routes.v1.auth import router as auth_router

    app.include_router(auth_router)

    return app
