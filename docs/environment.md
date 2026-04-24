# Environment Variables

## Gateway Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Host to bind |
| `PORT` | `8000` | Port to bind |
| `BASE_PATH` | `""` | Base path for the gateway (e.g. `/middleware`) |

## Microservices

Format: `SERVICE_<SERVICE_NAME>_URL`

### Pattern

```
SERVICE_<NOMBRE_MAYUSCULO>_URL=http://...
```

### Available Services

| Service | Variable | Default |
|---------|----------|---------|
| Health Monitoring | `SERVICE_HEALTH_MONITORING_URL` | `http://127.0.0.1:8000/api/health-monitoring` |

### Adding New Services

1. Add to `.env`:

```bash
SERVICE_MY_SERVICE_URL=http://localhost:8001
```

2. Create service in `app/microservices/my_service/`

3. Mount in `app/gateway.py`:

```python
from app.microservices.my_service import create_app
app.mount("/my_service", create_app())
```

## Example .env

```bash
HOST=0.0.0.0
PORT=8000
BASE_PATH="/middleware"
SERVICE_HEALTH_MONITORING_URL=http://127.0.0.1:8000/api/health-monitoring
```
