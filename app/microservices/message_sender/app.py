"""Message Sender (PulseCore) - Multi-channel Messaging Service.

## Test UI

Preview: [{service_url}]({service_url})

## Overview

Centralized API for multi-channel communication management.

## Capabilities

- **OTP Messaging** - Secure identity verification.
- **Onboarding (Welcome)** - Personalized user welcome notifications.
- **Waitlist Tracking** - Registration confirmation for waitlists.
- **Audit Logs** - Centralized tracking of every message dispatched.

## Backend

Proxies to: `{settings.SERVICE_MESSAGE_SENDER_URL}`
"""

from __future__ import annotations

from fastapi import FastAPI

from app.settings import settings

MESSAGE_SENDER_URL = settings.SERVICE_MESSAGE_SENDER_URL.rstrip("/")
_DESC = __doc__.replace("{service_url}", MESSAGE_SENDER_URL) if MESSAGE_SENDER_URL else __doc__


def create_app(root_path: str = "") -> FastAPI:
    """Create Message Sender sub-app with its own /docs."""
    app = FastAPI(
        title="PulseCore - Multi-channel Messaging API",
        version="1.1.0",
        description=_DESC,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        root_path=root_path,
    )

    from app.microservices.message_sender.routes import audit, otp, waitlist

    app.include_router(otp.router)
    app.include_router(waitlist.router)
    app.include_router(audit.router)

    return app
