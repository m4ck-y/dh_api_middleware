import pytest

from app.microservices.health_monitoring.domain import (
    ApiResponsePaginated,
    MeasureGroupRead,
    MeasureTypeGroupRelation,
    MeasureTypeRead,
)


def test_list_type_group_relations(client):
    response = client.get("/health_monitoring/measure/types-groups")
    assert response.status_code in [200]
    if response.status_code == 200:
        data = response.json()
        ApiResponsePaginated(**data)
        for item in data["data"]:
            MeasureTypeGroupRelation(**item)


def test_groups_for_type(client):
    response = client.get("/health_monitoring/measure/types/1/groups")
    assert response.status_code in [200]
    if response.status_code == 200:
        data = response.json()
        ApiResponsePaginated(**data)
        for item in data["data"]:
            MeasureGroupRead(**item)


def test_groups_for_type_not_found(client):
    response = client.get("/health_monitoring/measure/types/99999/groups")
    assert response.status_code in [404]


def test_types_for_group(client):
    response = client.get("/health_monitoring/measure/groups/1/types")
    assert response.status_code in [200]
    if response.status_code == 200:
        data = response.json()
        ApiResponsePaginated(**data)
        for item in data["data"]:
            MeasureTypeRead(**item)


def test_types_for_group_not_found(client):
    response = client.get("/health_monitoring/measure/groups/99999/types")
    assert response.status_code in [404]
