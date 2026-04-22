"""API Gateway - Central HTTP proxy for microservices.

## Overview

Stateless gateway that proxies requests to backend services.
Frontend points here instead of individual microservices.

## Security

- **NO database**: Pure HTTP proxy
- If compromised, attacker only accesses this proxy

## Services

| Service | Docs | Prefix |
|---------|------|--------|
| Main | [/docs](/docs) | `/` |
| Health Monitoring | [/health_monitoring/docs](/health_monitoring/docs) | `/health_monitoring` |
| Message Sender | [/message_sender/docs](/message_sender/docs) | `/message_sender` |
| Logger Tracer | [/logger_tracer/docs](/logger_tracer/docs) | `/logger_tracer` |

## Environment

Configure services with `SERVICE_<NAME>_URL` environment variables.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    """Create main gateway application."""
    app = FastAPI(
        title="API Gateway",
        version="0.1.0",
        description=__doc__,
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

    from app.microservices.health_monitoring.app import (
        create_app as create_health_monitoring,
    )
    from app.microservices.message_sender.app import (
        create_app as create_message_sender,
    )
    from app.microservices.logger_tracer.app import (
        create_app as create_logger_tracer,
    )

    app.mount("/health_monitoring", create_health_monitoring())
    app.mount("/message_sender", create_message_sender())
    app.mount("/logger_tracer", create_logger_tracer())

    return app
