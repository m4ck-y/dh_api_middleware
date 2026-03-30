import pytest

from app.microservices.health_monitoring.domain import (
    ApiResponsePaginated,
    ApiResponseSingle,
    MeasureGroupRead,
)


def test_list_measure_groups(client):
    response = client.get("/health_monitoring/measure/groups")
    assert response.status_code in [200]
    if response.status_code == 200:
        data = response.json()
        ApiResponsePaginated(**data)
        for item in data["data"]:
            MeasureGroupRead(**item)


def test_get_measure_group(client):
    response = client.get("/health_monitoring/measure/groups/1")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        ApiResponseSingle(**data)
        MeasureGroupRead(**data["data"])


def test_get_measure_group_not_found(client):
    response = client.get("/health_monitoring/measure/groups/99999")
    assert response.status_code in [404]
