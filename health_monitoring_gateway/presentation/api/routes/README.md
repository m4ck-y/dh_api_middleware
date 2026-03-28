# Presentation API Routes

## Overview

FastAPI route definitions and handlers.

## Files

- [health_monitoring.py](health_monitoring.py) - Health Monitoring sub-app factory
- [middleware_health.py](middleware_health.py) - Gateway health endpoint
- [gw/](gw/) - Health Monitoring endpoint handlers

## Purpose

Contains API route handlers. Each microservice has its own sub-app with `/docs`.

## Adding New Service

Create a new file (e.g., `my_service.py`) and export:

```python
from fastapi import FastAPI

def create_my_service_app() -> FastAPI:
    app = FastAPI(title="My Service", docs_url="/docs")
    # Add routers
    return app
```

Then mount in `factory.py`: `app.mount("/my_service", create_my_service_app())`
