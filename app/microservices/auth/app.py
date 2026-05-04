"""Auth API - Authentication and user profile.

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


def create_app() -> FastAPI:
    app = FastAPI(
        title="Auth API",
        version="0.1.0",
        description=__doc__,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    from app.microservices.auth.routes.auth import router as auth_router

    auth_router.prefix = "/v1/auth"
    app.include_router(auth_router)

    return app
