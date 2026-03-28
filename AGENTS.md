# AGENTS.md — AI Developer Assistant Rules

## Quick Reference

- **Stack**: Python 3.13+, FastAPI, httpx, uv
- **No database**: Stateless HTTP proxy only
- **Env vars**: `SERVICE_<NAME>_URL`, `HOST`, `PORT`

## Key Patterns

### Add new microservice
1. Create `app/microservices/<name>/` with `app.py`, `domain/`, `routes/`
2. Add `NAME_URL = os.environ["SERVICE_NAME_URL"]` in `app.py`
3. Import URL in routes and use `http_client.request()`
4. Mount in `gateway.py`: `app.mount("/name", create_app())`

### Routes pattern
```python
from app.http_client import request
from app.microservices.my_service.app import MY_SERVICE_URL

@router.get("/endpoint")
async def get_something():
    status, data = await request(MY_SERVICE_URL, "GET", "path")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
```

## References

- [docs/](../docs/) — Full documentation
- [dev-style-guide](../dev-style-guide/) — General standards
