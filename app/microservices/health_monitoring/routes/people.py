"""People endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.http_client import request
from app.microservices.health_monitoring.app import HEALTH_MONITORING_URL
from app.microservices.health_monitoring.domain import (
    CountResponse,
    MessageResponse,
    PersonCreate,
    PersonRead,
    PersonUpdate,
)

router = APIRouter(tags=["People"])


@router.get("/people", response_model=list[PersonRead])
async def list_people():
    status, data = await request(HEALTH_MONITORING_URL, "GET", "people")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/people/count", response_model=CountResponse)
async def people_count():
    status, data = await request(HEALTH_MONITORING_URL, "GET", "people/count")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/people/{person_id}", response_model=PersonRead)
async def get_person(person_id: int):
    status, data = await request(HEALTH_MONITORING_URL, "GET", f"people/{person_id}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/people", response_model=PersonRead, status_code=201)
async def create_person(payload: PersonCreate):
    status, data = await request(
        HEALTH_MONITORING_URL, "POST", "people", json=payload.model_dump()
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.put("/people/{person_id}", response_model=PersonRead)
async def update_person(person_id: int, payload: PersonCreate):
    status, data = await request(
        HEALTH_MONITORING_URL, "PUT", f"people/{person_id}", json=payload.model_dump()
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.patch("/people/{person_id}", response_model=PersonRead)
async def patch_person(person_id: int, payload: PersonUpdate):
    status, data = await request(
        HEALTH_MONITORING_URL,
        "PATCH",
        f"people/{person_id}",
        json=payload.model_dump(exclude_unset=True),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/people/{person_id}", response_model=MessageResponse)
async def delete_person(person_id: int):
    status, data = await request(HEALTH_MONITORING_URL, "DELETE", f"people/{person_id}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
