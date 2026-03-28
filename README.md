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
│  Main /docs   │     │  /health_    │     │  /other_     │
│               │     │  monitoring/  │     │  service/    │
│               │     │  docs        │     │  docs        │
└───────────────┘     └───────────────┘     └───────────────┘
```

## Services & Documentation

| Service | Docs URL | Prefix |
|---------|----------|--------|
| Main Gateway | [/docs](/docs) | `/` |
| Health Monitoring | [/health_monitoring/docs](/health_monitoring/docs) | `/health_monitoring` |

## Structure

```
api_middleware/
├── main.py                    # Entry point
├── app/
│   ├── __init__.py
│   ├── http_client.py         # Shared HTTP client
│   ├── settings/
│   │   ├── __init__.py
│   │   └── env.py            # Microservices URLs
│   ├── gateway.py            # Main app factory
│   ├── main/
│   │   └── health.py         # Gateway health endpoint
│   └── microservices/
│       ├── __init__.py
│       └── health_monitoring/
│           ├── __init__.py
│           ├── app.py         # Sub-app factory
│           ├── domain/
│           │   └── schemas.py # Pydantic schemas
│           └── routes/        # Endpoint handlers
│               ├── people.py
│               ├── measurements.py
│               └── ...
```

## Adding a New Microservice

1. Create folder: `app/microservices/my_service/`
2. Create `app.py` with:

```python
from fastapi import FastAPI

def create_app() -> FastAPI:
    app = FastAPI(
        title="My Service API",
        docs_url="/docs",
    )
    # Add routers
    return app
```

3. Mount in `app/gateway.py`:

```python
from app.microservices.my_service import create_app
app.mount("/my_service", create_app())
```

4. Add URL in environment (see below)

## Environment Variables

### Gateway Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `GATEWAY_HOST` | `0.0.0.0` | Host to bind |
| `GATEWAY_PORT` | `8080` | Port to bind |

### Microservices

Format: `SERVICE_<SERVICE_NAME>_URL`

| Variable | Default | Description |
|----------|---------|-------------|
| `SERVICE_HEALTH_MONITORING_URL` | `http://127.0.0.1:8000/api/health-monitoring` | Health Monitoring backend |
| `SERVICE_OTHER_SERVICE_URL` | - | Other service (add as needed) |

**Pattern**: `SERVICE_<NOMBRE_MAYUSCULA>_URL`

Example for new service:
```bash
SERVICE_MY_NEW_SERVICE_URL=http://localhost:8001
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
cp .env.example .env
# Edit .env with your service URLs
uv sync
uv run uvicorn main:app --host 0.0.0.0 --port 8080
# or: uv run python main.py
```

## API Documentation

- **Main gateway**: `http://localhost:8080/docs`
- **Health Monitoring**: `http://localhost:8080/health_monitoring/docs`
- **Health check**: `GET /health`
