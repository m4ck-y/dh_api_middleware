# api-middleware

## Decisión y propósito

Este repositorio es el **punto de entrada HTTP** para integrarse con [Health Monitoring](../health_monitoring): un **middleware/gateway** que **no replica la lógica de negocio** del backend, sino que **expone la misma forma de API** (rutas y contratos documentados) y **delega cada llamada al servicio Health Monitoring por HTTP**.

**Por qué existe**

- Unificar **una URL y un contrato** (`/health_monitoring/...`) para clientes, aunque el backend evolucione o se despliegue aparte.
- Añadir **cortafuegos lógicos** cuando haga falta: autenticación, rate limiting, logging, transformación mínima de cabeceras o cuerpos, sin tocar el código del dominio en `health_monitoring`.
- Mantener **OpenAPI/Swagger en el middleware** usando esquemas Pydantic alineados con el backend, para que la documentación sea usable desde aquí.

**Qué no es**

- No sustituye la base de datos ni las reglas de negocio: esas viven en Health Monitoring.
- No es obligatorio para desarrollar solo el backend; solo tiene sentido cuando el flujo deseado es *cliente → middleware → Health Monitoring*.

## Alcance

| Sí hace | No hace |
|--------|--------|
| Expone rutas bajo `/health_monitoring` equivalentes a las del API de Health Monitoring | Persistencia, ORM ni reglas clínicas |
| Llama al backend por HTTP (`httpx`) con la misma ruta relativa y query | Sustituir la documentación oficial del backend si difieren; hay que alinear `domain/schemas` |
| Documenta request/response en `/docs` con Pydantic | Instalar ni ejecutar PostgreSQL por sí mismo |

Referencia de rutas del backend: [`health_monitoring/backend/docs/endpoints.md`](../health_monitoring/backend/docs/endpoints.md) y el código en [`health_monitoring/backend/app`](../health_monitoring/backend/app).

## Stack

- Python 3.13+ (`.python-version`)
- FastAPI, Uvicorn, httpx (`pyproject.toml`)
- Gestión de dependencias: **uv** + `pyproject.toml`

Convenciones de estructura inspiradas en [`template_backend_python`](../template_backend_python) (capas y nombres explícitos).

## Estructura del código

Paquete **`health_monitoring_gateway`** (bounded context “gateway a Health Monitoring”):

| Capa | Contenido |
|------|-----------|
| `domain/` | Contrato HTTP hacia el backend (`HealthMonitoringBackendPort`, `BackendHttpResponse`), errores de transporte, **DTOs** en `domain/schemas/` (mantenerlos alineados con `health_monitoring/backend/app/schemas`) |
| `application/` | `CallHealthMonitoringBackend`: orquesta la llamada HTTP (métodos permitidos, ruta normalizada) |
| `infrastructure/` | `Settings`, cliente `HttpxHealthMonitoringBackend`, política de cabeceras |
| `presentation/api/` | `factory.py`, `middleware_health`, routers documentados en `routes/gw/` |

Punto de entrada ASGI: `main.py` → `app = create_app()`.

## Superficie HTTP y documentación

- **`GET /health`**: salud **solo del proceso middleware** (no comprueba Health Monitoring).
- **`/health_monitoring/...`**: mismas rutas relativas que el API de Health Monitoring; cada operación **invoca el backend** con método, query y cuerpo adecuados. La documentación interactiva está en **`/docs`** y **`/redoc`**.

Ejemplo: con base del backend `http://localhost:8000/api/health-monitoring` y middleware en el puerto `8080`,  
`GET http://localhost:8080/health_monitoring/people` → `GET http://localhost:8000/api/health-monitoring/people`.

## Variables de entorno

| Variable | Valor por defecto | Uso |
|----------|-------------------|-----|
| `HEALTH_MONITORING_BACKEND_BASE_URL` | `http://127.0.0.1:8000/api/health-monitoring` | URL base del API Health Monitoring (sin barra final obligatoria). Si no está definida, se usa `HEALTH_MONITORING_UPSTREAM_BASE_URL` por compatibilidad. |
| `GATEWAY_HOST` | `0.0.0.0` | Host al arrancar con `python main.py` |
| `GATEWAY_PORT` | `8080` | Puerto al arrancar con `python main.py` |

## Desarrollo local

```bash
cd api_middleware
uv sync
uv run uvicorn main:app --host 0.0.0.0 --port 8080
# alternativa: uv run python main.py
```

Arranca Health Monitoring (o apunta `HEALTH_MONITORING_BACKEND_BASE_URL` al entorno correcto) antes de probar rutas bajo `/health_monitoring`.

Cuando cambien los modelos del backend, actualiza los espejos en `health_monitoring_gateway/domain/schemas/` para que Swagger y validación sigan siendo fieles al contrato.
