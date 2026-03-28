# API Gateway — Middleware

## Purpose

**Central gateway/middleware for multiple microservices.** The frontend points here instead of calling each microservice directly.

## Why This Exists

- **Single entry point**: Frontend only needs to know one URL instead of multiple service URLs.
- **Security**: If the gateway is compromised, the attacker only accesses this proxy—not the actual services with business logic and databases.
- **No database**: This gateway is stateless and has no database access. It's a pure HTTP proxy.
- **Separate docs**: Each microservice has its own `/<service>/docs`.

## Architecture

```
                    ┌─────────────────────────┐
                    │   Frontend/Client       │
                    └───────────┬─────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │    API Gateway          │  ← This project
                    │  (no DB, proxy only)   │
                    └───────────┬─────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│  Main /docs  │     │  /health_     │     │  /other_     │
│               │     │  monitoring/   │     │  service/    │
│               │     │  docs         │     │  docs        │
└───────────────┘     └───────────────┘     └───────────────┘
```

## Services & Documentation

| Service | Docs URL | Prefix |
|---------|----------|--------|
| Main Gateway | [/docs](/docs) | `/` |
| Health Monitoring | [/health_monitoring/docs](/health_monitoring/docs) | `/health_monitoring` |

## Adding a New Microservice

1. Create a new route file: `presentation/api/routes/my_service.py`

```python
from fastapi import FastAPI

def create_my_service_app() -> FastAPI:
    app = FastAPI(
        title="My Service API",
        description="My microservice description",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    # Add routers here
    return app
```

2. Mount it in `factory.py`:

```python
from my_service import create_my_service_app

app.mount("/my_service", create_my_service_app())
```

## Security Notes

- This gateway has **NO database access**
- It's a stateless HTTP proxy
- No business logic here—just forwarding requests

## Stack

- Python 3.13+
- FastAPI, Uvicorn, httpx
- Managed with **uv**

## Development

```bash
cd api_middleware
uv sync
uv run uvicorn main:app --host 0.0.0.0 --port 8080
# or: uv run python main.py
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HEALTH_MONITORING_BACKEND_BASE_URL` | `http://127.0.0.1:8000/api/health-monitoring` | Health Monitoring backend URL |
| `GATEWAY_HOST` | `0.0.0.0` | Host to bind |
| `GATEWAY_PORT` | `8080` | Port to bind |

## API Documentation

- **Main gateway**: `http://localhost:8080/docs`
- **Health Monitoring**: `http://localhost:8080/health_monitoring/docs`
- **Health check**: `GET /health`

## Structure

```
api_middleware/
├── main.py                          # Entry point
└── health_monitoring_gateway/
    ├── domain/schemas/              # Pydantic schemas
    ├── infrastructure/             # HTTP client
    └── presentation/api/
        ├── factory.py               # Creates app & mounts sub-apps
        └── routes/
            ├── health_monitoring.py # Sub-app factory
            ├── middleware_health.py # Gateway health
            └── gw/                  # Health Monitoring routes
```
