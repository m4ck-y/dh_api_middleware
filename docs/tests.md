# Tests

## Structure

```
tests/
├── conftest.py              # Test fixtures
├── internal/
│   └── test_gateway.py     # Gateway endpoints tests
└── microservices/
    └── health_monitoring/
        ├── test_health.py
        ├── test_people.py
        ├── test_measurements.py
        ├── test_measure_types.py
        ├── test_measure_groups.py
        ├── test_units.py
        └── test_relations.py
```

## Running Tests

```bash
export SERVICE_HEALTH_MONITORING_URL=http://127.0.0.1:8001/api/health-monitoring
pytest tests/
```

## Schema Validation

Tests validate response against Pydantic schemas:

```python
from app.microservices.health_monitoring.domain import PersonRead

def test_list_people(client):
    response = client.get("/health_monitoring/people")
    assert response.status_code == 200
    data = response.json()
    if data:
        PersonRead(**data[0])  # Validates schema matches backend
```

This catches mismatches between middleware schemas and backend responses.

## Important Rules

- **GET only** - No write operations to avoid affecting database
- **Always validate schema** - Use Pydantic models to validate response
