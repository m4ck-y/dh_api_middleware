"""Core API - People Master Service.

## Overview

Manages persons, contact info (email, phone, address), identifiers, and emergency contacts.

## Endpoints

- People CRUD (list, get, create, update, update-status, delete)
- Address CRUD (list, create, update, delete)
- Email CRUD (list, create, update, delete)
- Phone CRUD (list, create, update, delete)
- Identifier CRUD (list, create, update, delete)
- Emergency Contact CRUD (list, create, update, delete)
- GET /check-exists

## Backend

Proxies to: `{settings.SERVICE_CORE_URL}`
"""

from __future__ import annotations

from fastapi import FastAPI

from app.settings import settings

CORE_URL = settings.SERVICE_CORE_URL.rstrip("/")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Core API",
        version="0.1.0",
        description=__doc__,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    from app.microservices.core.routes import people, address, contact, identity, social, validation

    people.router.prefix = "/v1/people"
    address.router.prefix = "/v1/people"
    contact.router.prefix = "/v1/people"
    identity.router.prefix = "/v1/people"
    social.router.prefix = "/v1/people"
    validation.router.prefix = "/v1/people"

    for m in [people, address, contact, identity, social, validation]:
        app.include_router(m.router)

    return app
