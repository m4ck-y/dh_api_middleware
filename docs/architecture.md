# Architecture

## Overview

This is a **stateless HTTP proxy** gateway. It has no database access—only forwards requests to backend services.

## Diagram

```
Client → API Gateway → Health Monitoring Backend
                    → Other Services...
```

## Structure

```
app/
├── main.py              # Entry point
├── gateway.py           # Main FastAPI app factory
├── http_client.py       # Shared HTTP client
├── settings/
│   └── env.py          # pydantic-settings (HOST, PORT, SERVICE_*_URL)
├── internal/
│   └── health.py       # Gateway endpoints (/health)
└── microservices/
    └── health_monitoring/
        ├── app.py       # Sub-app factory
        ├── domain/      # Pydantic schemas (separate files)
        └── routes/     # Endpoint handlers
```

## Components

### app/gateway.py
Main FastAPI application factory. Mounts all microservice sub-apps.

### app/http_client.py
Shared HTTP client for making requests to backend services.

### app/settings/env.py
Configuration using pydantic-settings. Reads HOST, PORT, and SERVICE_*_URL from environment.

### app/internal/
Gateway internal endpoints (not proxied): `/health`

### app/microservices/<name>/
Each microservice is a sub-app with:
- `app.py`: FastAPI sub-app factory + URL constant
- `domain/`: Pydantic schemas (separate files per entity)
- `routes/`: Endpoint handlers

## Security

- **No database**: Gateway is purely a proxy
- **Single entry point**: Frontend only knows one URL
- **If compromised**: Attacker only accesses proxy, not actual services
