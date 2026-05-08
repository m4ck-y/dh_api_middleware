# API Gateway — Middleware

## Purpose

**Central gateway/middleware for multiple microservices.** The frontend points here instead of calling each microservice directly.

## Why This Exists

- **Explicit Contract (Interface)**: The gateway acts as the strict contract between the frontend and the backends. All schemas and inputs/outputs are explicitly defined here, generating a unified Swagger documentation.
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
                    │  (no DB, proxy only)    │
                    └───────────┬─────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│  Main /docs   │     │  /health_     │     │  /other_      │
│               │     │  monitoring/  │     │  service/     │
│               │     │  docs         │     │  docs         │
└───────────────┘     └───────────────┘     └───────────────┘
```

## Services & Documentation

> All URLs prefixed by `ROOT_PATH` (`/api/middleware` by default).

| Service | Status | Docs URL | Prefix |
|---------|--------|----------|--------|
| Main Gateway | RELEASED | `<ROOT_PATH>/docs` | `/` |
| Auth | RELEASED | `<ROOT_PATH>/auth/docs` | `/auth` |
| IAM | RELEASED | `<ROOT_PATH>/iam/docs` | `/iam` |
| Core | RELEASED | `<ROOT_PATH>/core/docs` | `/core` |
| MFA | RELEASED | `<ROOT_PATH>/mfa/docs` | `/mfa` |
| Onboarding | RELEASED | `<ROOT_PATH>/onboarding/docs` | `/onboarding` |
| Storage | RELEASED | `<ROOT_PATH>/storage/docs` | `/storage` |
| Admin | RELEASED | `<ROOT_PATH>/admin/docs` | `/admin` |
| Health Monitoring | RELEASED | `<ROOT_PATH>/health_monitoring/docs` | `/health_monitoring` |
| Message Sender | TESTING | `<ROOT_PATH>/message_sender/docs` | `/message_sender` |
| Logger Tracer | TESTING | `<ROOT_PATH>/logger_tracer/docs` | `/logger_tracer` |
| Catalogs | PENDING | — | `/catalogs` |
| Organizations | PENDING | — | `/organizations` |

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
│       ├── auth/
│       ├── iam/
│       ├── core/
│       ├── mfa/
│       ├── onboarding/
│       ├── storage/
│       ├── admin/
│       ├── health_monitoring/
│       ├── message_sender/
│       └── logger_tracer/
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
| `ROOT_PATH` | `"/api/middleware"` | Gateway root path (striped by ASGI before routing) |

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

- **Main gateway**: `http://localhost:8000/middleware/docs`
- **Health Monitoring**: `http://localhost:8000/middleware/health_monitoring/docs`
- **Health check**: `GET /middleware/health`

## Systemd Service Management

### 1. Copiar definición del servicio

```bash
sudo cp /home/m4ck-y/.me/dh/api_middleware/docs/api_middleware.service /etc/systemd/system/
```

O crearlo manualmente:

```bash
sudo nano /etc/systemd/system/dh_api_middleware.service
```

### 2. Gestionar el servicio

```bash
sudo systemctl daemon-reload
sudo systemctl enable api_middleware
sudo systemctl start api_middleware
sudo systemctl status api_middleware
journalctl -u api_middleware -f
```
