import pytest

from app.microservices.health_monitoring.domain import (
    ApiResponsePaginated,
    ApiResponseSingle,
    CountResponse,
    PersonRead,
)


def test_list_people(client):
    response = client.get("/health_monitoring/people")
    assert response.status_code in [200]
    if response.status_code == 200:
        data = response.json()
        ApiResponsePaginated(**data)
        for item in data["data"]:
            PersonRead(**item)


def test_get_people_count(client):
    response = client.get("/health_monitoring/people/count")
    assert response.status_code in [200]
    if response.status_code == 200:
        CountResponse(**response.json())


def test_get_person(client):
    response = client.get("/health_monitoring/people/1")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        ApiResponseSingle(**data)
        PersonRead(**data["data"])


def test_get_person_not_found(client):
    response = client.get("/health_monitoring/people/99999")
    assert response.status_code in [404]
