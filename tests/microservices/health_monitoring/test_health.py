import pytest

from app.microservices.health_monitoring.domain import (
    BackendHealthStatusResponse,
    BackendVersionResponse,
)


def test_backend_health(client):
    response = client.get("/health_monitoring/health")
    assert response.status_code in [200, 502]
    if response.status_code == 200:
        BackendHealthStatusResponse(**response.json())


def test_backend_health_detailed(client):
    response = client.get("/health_monitoring/health/detailed")
    assert response.status_code in [200, 502]


def test_backend_version(client):
    response = client.get("/health_monitoring/version")
    assert response.status_code in [200, 502]
    if response.status_code == 200:
        BackendVersionResponse(**response.json())
