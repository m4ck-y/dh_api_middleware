"""Onboarding API - Self-registration flow.

## Overview

Orchestrates the multi-step onboarding process: waitlist, personal info, OTP, password, address, documents, submit.

## Endpoints

- Waitlist: register, list, check email, invite
- Onboarding: start, personal-info, otp send/verify, password, address, documents, submit
- Onboarding Legacy: registro, curp, direccion, ine, comprobante

## Backend

Proxies to: `{settings.SERVICE_ONBOARDING_URL}`
"""

from __future__ import annotations

from fastapi import FastAPI

from app.settings import settings

ONBOARDING_URL = settings.SERVICE_ONBOARDING_URL.rstrip("/")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Onboarding API",
        version="0.1.0",
        description=__doc__,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    from app.microservices.onboarding.routes import waitlist, onboarding, legacy

    waitlist.router.prefix = "/v1/waitlist"
    onboarding.router.prefix = "/v1/onboarding"
    legacy.router.prefix = "/v1/onboarding/legacy"

    for m in [waitlist, onboarding, legacy]:
        app.include_router(m.router)

    return app
