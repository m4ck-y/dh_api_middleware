"""Onboarding API - Self-registration flow.

## Test UI

Preview: [{service_url}]({service_url})

## Overview

Orchestrates the multi-step onboarding process: waitlist, personal info, OTP, password, address, documents, submit.

## Endpoints

- Waitlist: register, list, check email, invite
- Onboarding: start, personal-info, otp send/verify, password, address, documents, submit
- Onboarding Legacy: registro, personal_identifier, direccion, ine, comprobante

## Backend

Proxies to: [{service_url}/docs]({service_url}/docs)
"""

from __future__ import annotations

from fastapi import FastAPI

from app.settings import settings

ONBOARDING_URL = settings.SERVICE_ONBOARDING_URL.rstrip("/")
_DESC = __doc__.replace("{service_url}", ONBOARDING_URL) if ONBOARDING_URL else __doc__


def create_app(root_path: str = "") -> FastAPI:
    app = FastAPI(
        title="Onboarding API",
        version="0.1.0",
        description=_DESC,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        root_path=root_path,
    )

    from app.microservices.onboarding.routes.v1 import waitlist, onboarding, legacy

    for m in [waitlist, onboarding, legacy]:
        app.include_router(m.router)

    return app
