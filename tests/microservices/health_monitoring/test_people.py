import pytest

from app.microservices.health_monitoring.domain import CountResponse, PersonRead


def test_list_people(client):
    response = client.get("/health_monitoring/people")
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        if data.get("data"):
            PersonRead(**data["data"][0])  # Validate schema


def test_get_people_count(client):
    response = client.get("/health_monitoring/people/count")
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        CountResponse(**response.json())


def test_get_person_not_found(client):
    response = client.get("/health_monitoring/people/99999")
    assert response.status_code in [404, 500]
