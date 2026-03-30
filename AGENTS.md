# AGENTS.md — AI Developer Assistant Rules

## Quick Reference

- **Stack**: Python 3.13+, FastAPI, httpx, uv
- **No database**: Stateless HTTP proxy only
- **Env vars**: `SERVICE_<NAME>_URL`, `HOST`, `PORT`

## Key Patterns

### Add new microservice
1. Create `app/microservices/<name>/` with `app.py`, `domain/`, `routes/`
2. Add URL constant: `NAME_URL = settings.SERVICE_NAME_URL`
3. Add module docstring with Swagger description (see below)
4. Add routes in `routes/` with proper response_model
5. Mount in `gateway.py`: `app.mount("/name", create_app())`

### Routes pattern (ALWAYS use response_model)
```python
from fastapi import APIRouter, HTTPException

from app.http_client import request
from app.microservices.my_service.app import MY_SERVICE_URL
from app.microservices.my_service.domain import MyResponseSchema

router = APIRouter(tags=["My Endpoint"])

@router.get("/endpoint", response_model=list[MyResponseSchema])
async def get_something():
    status, data = await request(MY_SERVICE_URL, "GET", "path")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
```

### Schemas (domain/)
- Create separate files per domain entity in `domain/`
- Schema fields MUST match backend response field names
- If backend returns `id_measure_type`, schema must have `id_measure_type: int`

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

## References

- [docs/](../docs/) — Full documentation
- [dev-style-guide](../dev-style-guide/) — General standards
