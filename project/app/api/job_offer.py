from typing import List

from fastapi import APIRouter, HTTPException, status

from app import constant
from app.services.job_offer import add_job_offer, get_job_offer, get_job_offers, remove_job_offer, edit_job_offer
from app.schema.job_offer import UserPayloadSchema, UserResponseSchema

router = APIRouter()


@router.post("/", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_job_offer(payload: UserPayloadSchema) -> UserResponseSchema:
    return await add_job_offer(payload)


@router.get("/{id}/", response_model=UserResponseSchema)
async def read_job_offer(id: str) -> UserResponseSchema:
    job_offer = await get_job_offer(id)
    if not job_offer:
        raise HTTPException(status_code=404, detail=constant.JOB_OFFER_NOT_FOUND)

    return job_offer


@router.get("/", response_model=List[UserResponseSchema])
async def read_all_job_offers() -> List[UserResponseSchema]:
    return await get_job_offers()


@router.delete("/{id}/", response_model=UserResponseSchema)
async def delete_job_offer(id: str) -> UserResponseSchema:
    job_offer = await get_job_offers(id)
    if not job_offer:
        raise HTTPException(status_code=404, detail=constant.JOB_OFFER_NOT_FOUND)

    await remove_job_offer(id)

    return job_offer


@router.put("/{id}/", response_model=UserResponseSchema)
async def update_job_offer(id: str, payload: UserPayloadSchema) -> UserResponseSchema:
    job_offer = await edit_job_offer(id, payload)
    if not job_offer:
        raise HTTPException(status_code=404, detail=constant.JOB_OFFER_NOT_FOUND)

    return job_offer
