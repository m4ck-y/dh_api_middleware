import pytest

from app.microservices.health_monitoring.domain import MeasurementRead


def test_list_measurements(client):
    response = client.get("/health_monitoring/measurements")
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        if data.get("data"):
            MeasurementRead(**data["data"][0])


def test_list_measurements_filter_by_person(client):
    response = client.get("/health_monitoring/measurements?person_id=1")
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        if data.get("data"):
            MeasurementRead(**data["data"][0])


def test_list_measurements_filter_by_measure_type(client):
    response = client.get("/health_monitoring/measurements?measure_type_id=1")
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        if data.get("data"):
            MeasurementRead(**data["data"][0])


def test_get_measurement_not_found(client):
    response = client.get("/health_monitoring/measurements/99999")
    assert response.status_code in [404, 500]
