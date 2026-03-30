# AGENTS.md — AI Developer Assistant Rules

## Quick Reference

- **Stack**: Python 3.13+, FastAPI, httpx, uv
- **No database**: Stateless HTTP proxy only
- **Env vars**: `SERVICE_<NAME>_URL`, `HOST`, `PORT`

## API Response Format

All endpoints use one of these response structures:

### Single Record (`ApiResponseSingle[T]`)
```python
{
    "status_code": 200,
    "internal_code": 0,
    "message": "Success message",
    "data": {...},  # Single object
    "pagination": None
}
```

### List with Pagination (`ApiResponsePaginated[T]`)
```python
{
    "status_code": 200,
    "internal_code": 0,
    "message": "Success message",
    "data": [...],  # List of objects
    "pagination": {
        "limit": 100,
        "pages": 5,
        "total": 450,
        "page": 1
    }
}
```

### Query Parameters for List Endpoints
- `page` - Page number (default: 1)
- `limit` - Items per page (default: 100, max: 100)

## Key Patterns

### Add new microservice
1. Create `app/microservices/<name>/` with `app.py`, `domain/`, `routes/`
2. Add URL constant: `NAME_URL = settings.SERVICE_NAME_URL`
3. Add module docstring with Swagger description (see below)
4. Add routes in `routes/` with proper response_model
5. Mount in `gateway.py`: `app.mount("/name", create_app())`

### Routes pattern - List endpoints with pagination
```python
from fastapi import APIRouter, HTTPException, Query

from app.http_client import request
from app.microservices.my_service.app import MY_SERVICE_URL
from app.microservices.health_monitoring.domain import MyResponseSchema
from app.shared.domain import ApiResponsePaginated

router = APIRouter(tags=["My Endpoint"])

@router.get("/endpoint", response_model=ApiResponsePaginated[list[MyResponseSchema]])
async def list_endpoint(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(100, ge=1, le=100, description="Items per page"),
):
    params = {"page": page, "limit": limit}
    status, data = await request(MY_SERVICE_URL, "GET", "endpoint", params=params)
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
```

### Routes pattern - Single record endpoint
```python
from fastapi import APIRouter, HTTPException

from app.http_client import request
from app.microservices.my_service.app import MY_SERVICE_URL
from app.microservices.health_monitoring.domain import MyResponseSchema
from app.shared.domain import ApiResponseSingle

router = APIRouter(tags=["My Endpoint"])

@router.get("/endpoint/{id}", response_model=ApiResponseSingle[MyResponseSchema])
async def get_endpoint(id: int):
    status, data = await request(MY_SERVICE_URL, "GET", f"endpoint/{id}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
```

### Schemas (domain/)
- Create separate files per domain entity in `domain/`
- Schema fields MUST match backend response field names
- If backend returns `id_measure_type`, schema must have `id_measure_type: int`
- Use `ApiResponsePaginated` for list endpoints with pagination
- Use `ApiResponseSingle` for single record endpoints

### Shared schemas location
- `app/shared/domain/api_response.py` - `ApiResponseBase`, `ApiResponseSingle`, `ApiResponsePaginated`, `PaginationResponse`, `InternalCode`
- `app/shared/domain/common.py` - `CountResponse`, `MessageResponse`, etc.

### Microservice docstring (REQUIRED for Swagger)

Every `app.py` must have a module docstring used as description:

```python
"""Service Name - Brief description.

## Overview

What this service proxies and manages.

## Endpoints

- Endpoint 1
- Endpoint 2

## Backend

Proxies to: `{settings.SERVICE_NAME_URL}`
"""
```

## Important Rules

1. **ALWAYS use response_model** - Required for Swagger documentation
2. **Schema field names must match backend** - If backend returns `id_measure_type`, use that exact name
3. **One schema file per entity** - Keep domain/ organized
4. **Use ApiResponsePaginated for list endpoints** - Wrap paginated list responses
5. **Use ApiResponseSingle for single record endpoints** - Wrap single object responses
6. **Use shared domain** - Import from `app.shared.domain`

## References

- [docs/](../docs/) — Full documentation
- [dev-style-guide](../dev-style-guide/) — General standards
