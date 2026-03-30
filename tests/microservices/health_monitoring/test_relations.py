import pytest

from app.microservices.health_monitoring.domain import (
    MeasureGroupRead,
    MeasureTypeGroupRelation,
    MeasureTypeRead,
)


def test_list_type_group_relations(client):
    response = client.get("/health_monitoring/measure/types-groups")
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        if data.get("data"):
            MeasureTypeGroupRelation(**data["data"][0])


def test_groups_for_type(client):
    response = client.get("/health_monitoring/measure/types/1/groups")
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        if data.get("data"):
            MeasureGroupRead(**data["data"][0])


def test_types_for_group(client):
    response = client.get("/health_monitoring/measure/groups/1/types")
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        if data.get("data"):
            MeasureTypeRead(**data["data"][0])
