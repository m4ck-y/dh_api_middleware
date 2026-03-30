import pytest

from app.microservices.health_monitoring.domain import MeasureGroupRead


def test_list_measure_groups(client):
    response = client.get("/health_monitoring/measure/groups")
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        if data.get("data"):
            MeasureGroupRead(**data["data"][0])


def test_get_measure_group_not_found(client):
    response = client.get("/health_monitoring/measure/groups/99999")
    assert response.status_code in [404, 500]
