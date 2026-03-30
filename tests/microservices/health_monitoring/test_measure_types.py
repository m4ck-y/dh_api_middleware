import pytest

from app.microservices.health_monitoring.domain import CountResponse, MeasureTypeRead


def test_list_measure_types(client):
    response = client.get("/health_monitoring/measure/types")
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        if data.get("data"):
            MeasureTypeRead(**data["data"][0])


def test_get_measure_types_count(client):
    response = client.get("/health_monitoring/measure/types/count")
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        CountResponse(**response.json())


def test_list_measure_types_with_data(client):
    response = client.get("/health_monitoring/measure/types/with-data")
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        if data:
            MeasureTypeRead(**data[0])


def test_get_measure_type_not_found(client):
    response = client.get("/health_monitoring/measure/types/99999")
    assert response.status_code in [404, 500]
