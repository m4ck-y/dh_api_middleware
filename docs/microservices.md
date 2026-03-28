# Adding Microservices

## Steps

### 1. Create Service Folder

```
app/microservices/my_service/
├── app.py
├── domain/
│   └── schemas.py
└── routes/
    ├── __init__.py
    └── my_endpoint.py
```

### 2. Create Sub-App Factory

`app/microservices/my_service/app.py`:

```python
from fastapi import FastAPI

def create_app() -> FastAPI:
    app = FastAPI(
        title="My Service API",
        version="0.1.0",
        description="My service description",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    # Import and include routers
    from app.microservices.my_service.routes import my_endpoint
    app.include_router(my_endpoint.router)
    
    return app
```

### 3. Create Routes

`app/microservices/my_service/routes/my_endpoint.py`:

```python
from fastapi import APIRouter, HTTPException
from app.http_client import request
from app.microservices.my_service.app import MY_SERVICE_URL

router = APIRouter(tags=["My Endpoint"])

@router.get("/my-endpoint")
async def get_something():
    status, data = await request(MY_SERVICE_URL, "GET", "endpoint")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
```

### 4. Add URL to Environment

`.env`:

```bash
SERVICE_MY_SERVICE_URL=http://localhost:8001
```

### 5. Mount in Gateway

`app/gateway.py`:

```python
from app.microservices.my_service import create_app
app.mount("/my_service", create_app())
```

## Service Template

Use `app/microservices/health_monitoring/` as reference.
