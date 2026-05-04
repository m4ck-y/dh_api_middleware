"""Auth API - Authentication and user profile.

## Test UI

Preview: [{service_url}]({service_url})

## Overview

Handles login, logout, silent refresh, and enriched user profile (/me).
Uses HttpOnly cookies for stateless JWT.

## Endpoints

- POST /login
- POST /silent-refresh
- POST /logout
- GET /me

## Backend

Proxies to: `{settings.SERVICE_AUTH_URL}`
"""

from __future__ import annotations

from fastapi import FastAPI

from app.settings import settings

AUTH_URL = settings.SERVICE_AUTH_URL.rstrip("/")
_DESC = __doc__.replace("{service_url}", AUTH_URL) if AUTH_URL else __doc__


def create_app() -> FastAPI:
    app = FastAPI(
        title="Auth API",
        version="0.1.0",
        description=_DESC,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    from app.microservices.auth.routes.auth import router as auth_router

    auth_router.prefix = "/v1/auth"
    app.include_router(auth_router)

    return app
