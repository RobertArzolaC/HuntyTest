from typing import List

from app import constant
from app.schema.job_offer import JobOfferPayloadSchema, JobOfferResponseSchema
from app.services.job_offer import (
    add_job_offer,
    edit_job_offer,
    get_job_offer,
    get_job_offers,
    get_job_offers_by_ids,
    remove_job_offer,
)
from app.services.job_offer_skill import get_job_offers_by_skills
from app.services.user import get_user
from app.services.user_skill import get_skills_by_user_id
from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.post(
    "/", response_model=JobOfferResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_job_offer(payload: JobOfferPayloadSchema) -> JobOfferResponseSchema:
    return await add_job_offer(payload)


@router.get("/{id}/", response_model=JobOfferResponseSchema)
async def read_job_offer(id: str) -> JobOfferResponseSchema:
    job_offer = await get_job_offer(id)
    if not job_offer:
        raise HTTPException(status_code=404, detail=constant.JOB_OFFER_NOT_FOUND)

    return job_offer


@router.get("/", response_model=List[JobOfferResponseSchema])
async def read_all_job_offers() -> List[JobOfferResponseSchema]:
    return await get_job_offers()


@router.delete("/{id}/", response_model=JobOfferResponseSchema)
async def delete_job_offer(id: str) -> JobOfferResponseSchema:
    job_offer = await get_job_offer(id)
    if not job_offer:
        raise HTTPException(status_code=404, detail=constant.JOB_OFFER_NOT_FOUND)

    await remove_job_offer(id)

    return job_offer


@router.put("/{id}/", response_model=JobOfferResponseSchema)
async def update_job_offer(
    id: str, payload: JobOfferPayloadSchema
) -> JobOfferResponseSchema:
    job_offer = await edit_job_offer(id, payload)
    if not job_offer:
        raise HTTPException(status_code=404, detail=constant.JOB_OFFER_NOT_FOUND)

    return job_offer


@router.get("/by_user/{user_id}", response_model=List[JobOfferResponseSchema])
async def read_all_job_offers_by_user(user_id: str) -> List[JobOfferResponseSchema]:
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail=constant.USER_NOT_FOUND)

    skill_id_list = await get_skills_by_user_id(user_id)
    job_offer_id_list = await get_job_offers_by_skills(skill_id_list)

    return await get_job_offers_by_ids(job_offer_id_list)
