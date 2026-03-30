import pytest

from app.microservices.health_monitoring.domain import (
    ApiResponsePaginated,
    ApiResponseSingle,
    MeasurementRead,
)


def test_list_measurements(client):
    response = client.get("/health_monitoring/measurements")
    assert response.status_code in [200]
    if response.status_code == 200:
        data = response.json()
        ApiResponsePaginated(**data)
        for item in data["data"]:
            MeasurementRead(**item)


def test_list_measurements_filter_by_person(client):
    response = client.get("/health_monitoring/measurements?person_id=1")
    assert response.status_code in [200]
    if response.status_code == 200:
        data = response.json()
        ApiResponsePaginated(**data)
        for item in data["data"]:
            MeasurementRead(**item)


def test_list_measurements_filter_by_measure_type(client):
    response = client.get("/health_monitoring/measurements?measure_type_id=1")
    assert response.status_code in [200]
    if response.status_code == 200:
        data = response.json()
        ApiResponsePaginated(**data)
        for item in data["data"]:
            MeasurementRead(**item)


def test_get_measurement(client):
    response = client.get("/health_monitoring/measurements/1")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        ApiResponseSingle(**data)
        MeasurementRead(**data["data"])


def test_get_measurement_not_found(client):
    response = client.get("/health_monitoring/measurements/99999")
    assert response.status_code in [404]
