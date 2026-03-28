# Architecture

## Overview

This is a **stateless HTTP proxy** gateway. It has no database access—only forwards requests to backend services.

## Diagram

```
Client → API Gateway → Health Monitoring Backend
                    → Other Services...
```

## Components

### app/gateway.py
Main FastAPI application factory. Mounts all microservice sub-apps.

### app/http_client.py
Shared HTTP client for making requests to backend services.

### app/settings/env.py
Configuration loader. Reads service URLs from environment.

### app/microservices/<name>/
Each microservice is a sub-app with:
- `app.py`: FastAPI sub-app factory
- `domain/schemas.py`: Pydantic schemas
- `routes/`: Endpoint handlers

## Security

- **No database**: Gateway is purely a proxy
- **Single entry point**: Frontend only knows one URL
- **If compromised**: Attacker only accesses proxy, not actual services
