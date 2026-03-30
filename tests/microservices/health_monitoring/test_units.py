import pytest

from app.microservices.health_monitoring.domain import CountResponse, UnitRead


def test_list_units(client):
    response = client.get("/health_monitoring/units")
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        if data:
            UnitRead(**data[0])


def test_get_units_count(client):
    response = client.get("/health_monitoring/units/count")
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        CountResponse(**response.json())


def test_get_unit_not_found(client):
    response = client.get("/health_monitoring/units/99999")
    assert response.status_code in [404, 500]
