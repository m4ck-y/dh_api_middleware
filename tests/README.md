# Tests - API Middleware

## Structure

```
tests/
├── conftest.py              # Test fixtures
├── internal/
│   └── test_gateway.py     # Gateway endpoints tests
└── microservices/
    └── health_monitoring/
        ├── test_people.py
        ├── test_measurements.py
        ├── test_measure_types.py
        ├── test_measure_groups.py
        ├── test_units.py
        ├── test_relations.py
        └── test_health.py
```

## Important Note

These tests are **read-only (GET only)** to avoid affecting the real database.

Tests verify that endpoints respond correctly but do not perform write operations (POST, PUT, PATCH, DELETE).

## Schema Validation

Tests validate that response data matches the middleware schemas using Pydantic:

```python
from app.microservices.health_monitoring.domain import PersonRead

def test_list_people(client):
    response = client.get("/health_monitoring/people")
    assert response.status_code == 200
    data = response.json()
    if data:
        PersonRead(**data[0])  # Validates schema
```

This ensures the middleware schema matches the backend response.

## Running Tests

```bash
# Set the health monitoring backend URL
export SERVICE_HEALTH_MONITORING_URL=http://127.0.0.1:8001/api/health-monitoring
pytest tests/
```
