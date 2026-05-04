"""MFA API - OTP Challenge Service.

## Test UI

Preview: [{service_url}]({service_url})

## Overview

Generates and verifies one-time password challenges.

## Endpoints

- POST /challenges — create OTP challenge
- POST /challenges/{uuid_challenge}/verify
- POST /challenges/{uuid_challenge}/resend

## Backend

Proxies to: `{settings.SERVICE_MFA_URL}`
"""

from __future__ import annotations

from fastapi import FastAPI

from app.settings import settings

MFA_URL = settings.SERVICE_MFA_URL.rstrip("/")
_DESC = __doc__.replace("{service_url}", MFA_URL) if MFA_URL else __doc__


def create_app() -> FastAPI:
    app = FastAPI(
        title="MFA API",
        version="0.1.0",
        description=_DESC,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    from app.microservices.mfa.routes import otp

    otp.router.prefix = "/v1/otp"
    app.include_router(otp.router)

    return app
