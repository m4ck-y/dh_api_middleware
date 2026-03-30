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
├── app/
│   ├── main.py                  # Entry point
│   ├── gateway.py              # Main app factory
│   ├── http_client.py         # Shared HTTP client
│   ├── settings/
│   │   ├── __init__.py
│   │   └── env.py            # pydantic-settings
│   ├── internal/
│   │   └── health.py         # Gateway health endpoint
│   └── microservices/
│       ├── __init__.py
│       └── health_monitoring/
│           ├── __init__.py
│           ├── app.py         # Sub-app factory
│           ├── domain/        # Pydantic schemas
│           │   ├── __init__.py
│           │   ├── person.py
│           │   ├── measurement.py
│           │   └── ...
│           └── routes/        # Endpoint handlers
```

## Adding a New Microservice

1. Create folder: `app/microservices/my_service/`
2. Create `app.py` with module docstring for Swagger
3. Create routes in `routes/` folder (ALWAYS use response_model)
4. Create schemas in `domain/` matching backend field names
5. Mount in `app/gateway.py`
6. Add URL to `.env`

## Routes & Schemas Rules

- **ALWAYS use response_model** for Swagger documentation
- **Schema field names must match backend** exactly (e.g., `id_measure_type`, not `measure_type_id`)
- Create separate schema files per entity in `domain/`

## Environment Variables

### Gateway Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Host to bind |
| `PORT` | `8000` | Port to bind |

### Microservices

Format: `SERVICE_<SERVICE_NAME>_URL`

| Variable | Description |
|----------|-------------|
| `SERVICE_HEALTH_MONITORING_URL` | Health Monitoring backend (required) |
| `SERVICE_MY_SERVICE_URL` | Other service (add as needed) |

## Development

```bash
cd api_middleware
cp .env.example .env
# Edit .env with your service URLs
uv sync
uv run uvicorn app.main:app --reload
```

## API Documentation

- **Main gateway**: `http://localhost:8000/docs`
- **Health Monitoring**: `http://localhost:8000/health_monitoring/docs`
- **Health check**: `GET /health`
