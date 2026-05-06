"""API Gateway - Central HTTP proxy for microservices.

## Overview

Stateless gateway that proxies requests to backend services.
Frontend points here instead of individual microservices.

## Security

- **NO database**: Pure HTTP proxy
- If compromised, attacker only accesses this proxy

## Services

| Service | Status | Docs | Prefix |
|---------|--------|------|--------|
| Main | RELEASED | [{base_path}/docs]({base_path}/docs) | `/` |
| Auth | RELEASED | [{base_path}/auth/docs]({base_path}/auth/docs) | `/auth` |
| IAM | RELEASED | [{base_path}/iam/docs]({base_path}/iam/docs) | `/iam` |
| Core | RELEASED | [{base_path}/core/docs]({base_path}/core/docs) | `/core` |
| MFA | RELEASED | [{base_path}/mfa/docs]({base_path}/mfa/docs) | `/mfa` |
| Onboarding | RELEASED | [{base_path}/onboarding/docs]({base_path}/onboarding/docs) | `/onboarding` |
| Health Monitoring | RELEASED | [{base_path}/health_monitoring/docs]({base_path}/health_monitoring/docs) | `/health_monitoring` |
| Message Sender | TESTING | [{base_path}/message_sender/docs]({base_path}/message_sender/docs) | `/message_sender` |
| Logger Tracer | TESTING | [{base_path}/logger_tracer/docs]({base_path}/logger_tracer/docs) | `/logger_tracer` |
| Catalogs | PENDING | — | `/catalogs` |
| Organizations | PENDING | — | `/organizations` |
| Expedient | PENDING | — | `/expedient` |

## Environment

Configure services with `SERVICE_<NAME>_URL` environment variables.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.settings import settings


def create_app() -> FastAPI:
    """Create main gateway application."""
    root_path = settings.ROOT_PATH.rstrip("/")
    app = FastAPI(
        root_path=settings.ROOT_PATH,
        title="API Gateway",
        version="0.1.0",
        description=__doc__.format(base_path=root_path),
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from app.internal.health import router as health_router
    app.include_router(health_router)

    # ── RELEASED ─────────────────────────────────────────────────
    from app.microservices.auth.app import create_app as create_auth
    from app.microservices.iam.app import create_app as create_iam
    from app.microservices.core.app import create_app as create_core
    from app.microservices.mfa.app import create_app as create_mfa
    from app.microservices.onboarding.app import create_app as create_onboarding
    from app.microservices.health_monitoring.app import create_app as create_health_monitoring

    app.mount(f"{root_path}/auth", create_auth())
    app.mount(f"{root_path}/iam", create_iam())
    app.mount(f"{root_path}/core", create_core())
    app.mount(f"{root_path}/mfa", create_mfa())
    app.mount(f"{root_path}/onboarding", create_onboarding())
    app.mount(f"{root_path}/health_monitoring", create_health_monitoring())

    # ── TESTING ──────────────────────────────────────────────────
    from app.microservices.message_sender.app import create_app as create_message_sender
    from app.microservices.logger_tracer.app import create_app as create_logger_tracer

    app.mount(f"{root_path}/message_sender", create_message_sender())
    app.mount(f"{root_path}/logger_tracer", create_logger_tracer())

    # ── PENDING: catalogs, organizations, expedient ──────────────

    return app