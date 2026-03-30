import pytest

from app.microservices.health_monitoring.domain import (
    ApiResponsePaginated,
    ApiResponseSingle,
    CountResponse,
    UnitRead,
)


def test_list_units(client):
    response = client.get("/health_monitoring/units")
    assert response.status_code in [200]
    if response.status_code == 200:
        data = response.json()
        ApiResponsePaginated(**data)
        for item in data["data"]:
            UnitRead(**item)


def test_get_units_count(client):
    response = client.get("/health_monitoring/units/count")
    assert response.status_code in [200]
    if response.status_code == 200:
        CountResponse(**response.json())


def test_get_unit(client):
    response = client.get("/health_monitoring/units/1")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        ApiResponseSingle(**data)
        UnitRead(**data["data"])


def test_get_unit_not_found(client):
    response = client.get("/health_monitoring/units/99999")
    assert response.status_code in [404]
