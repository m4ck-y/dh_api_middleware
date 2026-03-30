# Adding Microservices

## Steps

### 1. Create Service Folder

```
app/microservices/my_service/
├── app.py
├── domain/
│   ├── __init__.py
│   └── my_entity.py
└── routes/
    ├── __init__.py
    └── my_endpoint.py
```

### 2. Create Sub-App Factory

`app/microservices/my_service/app.py`:

```python
"""My Service API - Brief description.

## Overview

What this service proxies and manages.

## Endpoints

- Endpoint 1
- Endpoint 2

## Backend

Proxies to: `{settings.SERVICE_MY_SERVICE_URL}`
"""

from fastapi import FastAPI
from app.settings import settings

MY_SERVICE_URL = settings.SERVICE_MY_SERVICE_URL.rstrip("/")


def create_app() -> FastAPI:
    app = FastAPI(
        title="My Service API",
        version="0.1.0",
        description=__doc__,
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    from app.microservices.my_service.routes import my_endpoint
    app.include_router(my_endpoint.router)
    
    return app
```

### 3. Create Schemas

`app/microservices/my_service/domain/my_entity.py`:

```python
from pydantic import BaseModel

class MyEntity(BaseModel):
    # Field names MUST match backend response exactly
    id: int
    name: str
```

`app/microservices/my_service/domain/__init__.py`:

```python
from app.microservices.my_service.domain.my_entity import MyEntity

__all__ = ["MyEntity"]
```

### 4. Create Routes

`app/microservices/my_service/routes/my_entity.py`:

```python
from fastapi import APIRouter, HTTPException, Query
from app.http_client import request
from app.microservices.my_service.app import MY_SERVICE_URL
from app.microservices.health_monitoring.domain import MyEntity  # Use from health_monitoring or your service
from app.shared.domain import ApiResponsePaginated

router = APIRouter(tags=["My Entity"])

# List endpoints return ApiResponsePaginated with pagination
@router.get("/my-entity", response_model=ApiResponsePaginated[list[MyEntity]])
async def list_my_entities(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    params = {"page": page, "limit": limit}
    status, data = await request(MY_SERVICE_URL, "GET", "my-entity", params=params)
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data

# Single record endpoints return ApiResponseSingle
@router.get("/my-entity/{entity_id}", response_model=ApiResponseSingle[MyEntity])
async def get_my_entity(entity_id: int):
    status, data = await request(MY_SERVICE_URL, "GET", f"my-entity/{entity_id}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
```

**Note:** All list endpoints use `ApiResponsePaginated[T]` and single endpoints use `ApiResponseSingle[T]` for consistent response format.

### 5. Add URL to Environment

`.env`:

```bash
SERVICE_MY_SERVICE_URL=http://localhost:8001
```

### 6. Mount in Gateway

`app/gateway.py`:

```python
from app.microservices.my_service import create_app
app.mount("/my_service", create_app())
```

## Important Rules

1. **ALWAYS use response_model** for Swagger documentation
2. **Schema field names must match backend exactly** (e.g., `id_measure_type`, not `measure_type_id`)
3. **Module docstring required** in `app.py` for Swagger description

## Service Template

Use `app/microservices/health_monitoring/` as reference.
