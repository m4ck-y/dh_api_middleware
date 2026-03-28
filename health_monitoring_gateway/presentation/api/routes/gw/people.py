"""People endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from health_monitoring_gateway.domain.schemas import (
    PersonCreate,
    PersonRead,
    PersonUpdate,
    CountResponse,
    MessageResponse,
)
from health_monitoring_gateway.infrastructure.http_client import request

router = APIRouter(tags=["People"])


@router.get("/people", response_model=list[PersonRead])
async def list_people():
    status, data = await request("GET", "people")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/people/count", response_model=CountResponse)
async def people_count():
    status, data = await request("GET", "people/count")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/people/{person_id}", response_model=PersonRead)
async def get_person(person_id: int):
    status, data = await request("GET", f"people/{person_id}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/people", response_model=PersonRead, status_code=201)
async def create_person(payload: PersonCreate):
    status, data = await request("POST", "people", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.put("/people/{person_id}", response_model=PersonRead)
async def update_person(person_id: int, payload: PersonCreate):
    status, data = await request(
        "PUT", f"people/{person_id}", json=payload.model_dump()
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.patch("/people/{person_id}", response_model=PersonRead)
async def patch_person(person_id: int, payload: PersonUpdate):
    status, data = await request(
        "PATCH", f"people/{person_id}", json=payload.model_dump(exclude_unset=True)
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/people/{person_id}", response_model=MessageResponse)
async def delete_person(person_id: int):
    status, data = await request("DELETE", f"people/{person_id}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
