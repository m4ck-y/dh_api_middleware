# Presentation API

## Overview

FastAPI application factory and route registration.

## Files

- [factory.py](factory.py) - Main app creation with sub-app mounting
- [routes/](routes/) - Route definitions

## Purpose

Creates FastAPI app and mounts sub-apps. Each microservice has its own sub-app with `/docs`.

## Adding New Services

1. Create route file in `routes/`:

```python
from fastapi import FastAPI

def create_my_service_app() -> FastAPI:
    app = FastAPI(title="My Service", docs_url="/docs")
    # Add routers
    return app
```

2. Mount in `factory.py`:

```python
from routes.my_service import create_my_service_app
app.mount("/my_service", create_my_service_app())
```
