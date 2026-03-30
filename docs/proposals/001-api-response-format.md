# API Response Format Proposal

## Overview

Standardize API response format across all microservices.

## Response Structure

```json
{
  "status_code": 200,
  "internal_code": 0,
  "message": "Success message",
  "data": [],
  "pagination": { "limit": 20, "pages": 8, "total": 150, "page": 1 }
}
```

## Internal Codes (Enums)

Cada `status_code` tiene un `internal_code` asociado. Se usan enums para garantizar el mapeo correcto:

```python
from enum import IntEnum

class InternalCode(IntEnum):
    SUCCESS = 0
    
    # Errores de cliente (4xx)
    NOT_FOUND = 1
    VALIDATION_ERROR = 2
    BAD_REQUEST = 3
    UNAUTHORIZED = 4
    FORBIDDEN = 5
    
    # Errores de servidor (5xx)
    SERVER_ERROR = 10
    EXTERNAL_SERVICE_ERROR = 11
    
    # Códigos específicos de negocio
    CODE_USER_PASSWORD_CREATED = 1003
    CODE_USER_ALREADY_EXISTS = 1004
    CODE_MEASUREMENT_NOT_FOUND = 2001
    # ... agregar según necesidad
```

**Mapeo status_code → internal_code:**

| HTTP Status | Internal Code (Enum) | Descripción |
|-------------|----------------------|-------------|
| 200 | `SUCCESS` (0) | OK |
| 201 | `SUCCESS` (0) | Created |
| 204 | `SUCCESS` (0) | No Content |
| 400 | `BAD_REQUEST` (3) | Bad Request |
| 401 | `UNAUTHORIZED` (4) | Unauthorized |
| 403 | `FORBIDDEN` (5) | Forbidden |
| 404 | `NOT_FOUND` (1) | Not Found |
| 422 | `VALIDATION_ERROR` (2) | Validation Error |
| 500 | `SERVER_ERROR` (10) | Internal Server Error |
| 502 | `EXTERNAL_SERVICE_ERROR` (11) | Bad Gateway |

## Pagination Query Params

| Param | Default | Max | Description |
|-------|---------|-----|-------------|
| `page` | 1 | - | Page number |
| `limit` | 20 | 100 | Items per page |

Example: `GET /people?page=2&limit=50`

---

## Schemas

Located in `app/shared/domain/api_response.py`:

```python
from enum import IntEnum
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


class InternalCode(IntEnum):
    SUCCESS = 0
    NOT_FOUND = 1
    VALIDATION_ERROR = 2
    BAD_REQUEST = 3
    UNAUTHORIZED = 4
    FORBIDDEN = 5
    SERVER_ERROR = 10
    EXTERNAL_SERVICE_ERROR = 11
    # Agregar códigos de negocio según necesidad


class PaginationResponse(BaseModel):
    limit: int
    pages: int
    total: int
    page: int


class ApiResponse(BaseModel, Generic[T]):
    status_code: int = 200
    internal_code: int | None = None
    message: str | None = None
    data: Optional[T] = None
    pagination: Optional[PaginationResponse] = None
```

**Un solo schema para todo.** `data` puede ser un objeto, lista, o `null`. `pagination` puede ser `null` o tener valores.

## Ejemplos de Uso

### GET single record

```python
return ApiResponse(
    status_code=200,
    internal_code=InternalCode.SUCCESS,
    message="Person found successfully.",
    data={"id": 1, "name": "John"},
    pagination=None
)
```

### GET list with pagination

```python
return ApiResponse(
    status_code=200,
    internal_code=InternalCode.SUCCESS,
    message="People found successfully.",
    data=[{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}],
    pagination=PaginationResponse(
        limit=20,
        pages=8,
        total=150,
        page=1
    )
)
```

### GET count

```python
return ApiResponse(
    status_code=200,
    internal_code=InternalCode.SUCCESS,
    message="Count retrieved successfully.",
    data={"count": 42},
    pagination=None
)
```

### Error

```python
return ApiResponse(
    status_code=404,
    internal_code=InternalCode.NOT_FOUND,
    message="Person not found.",
    data=None,
    pagination=None
)
```

---

## Status

- [ ] Propose to health_monitoring backend
- [ ] Create response schemas in backend
- [ ] Update middleware schemas
- [ ] Update middleware routes
- [ ] Update tests
