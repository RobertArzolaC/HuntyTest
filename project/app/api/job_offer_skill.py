from typing import List

from app import constant
from app.schema.job_offer_skill import (
    JobOfferSkillPayloadSchema,
    JobOfferSkillResponseSchema,
)
from app.services.job_offer_skill import (
    add_job_offer_skill,
    edit_job_offer_skill,
    get_job_offer_skill,
    get_job_offer_skills,
    remove_job_offer_skill,
)
from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.post(
    "/", response_model=JobOfferSkillResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_job_offer_skill(
    payload: JobOfferSkillPayloadSchema,
) -> JobOfferSkillResponseSchema:
    return await add_job_offer_skill(payload)


@router.get("/{id}/", response_model=JobOfferSkillResponseSchema)
async def read_job_offer_skill(id: str) -> JobOfferSkillResponseSchema:
    skill = await get_job_offer_skill(id)
    if not skill:
        raise HTTPException(status_code=404, detail=constant.JOB_OFFER_SKILL_NOT_FOUND)

    return skill


@router.get("/", response_model=List[JobOfferSkillResponseSchema])
async def read_all_job_offer_skills() -> List[JobOfferSkillResponseSchema]:
    return await get_job_offer_skills()


@router.delete("/{id}/", response_model=JobOfferSkillResponseSchema)
async def delete_job_offer_skill(id: str) -> JobOfferSkillResponseSchema:
    skill = await get_job_offer_skill(id)
    if not skill:
        raise HTTPException(status_code=404, detail=constant.JOB_OFFER_SKILL_NOT_FOUND)

    await remove_job_offer_skill(id)

    return skill


@router.put("/{id}/", response_model=JobOfferSkillResponseSchema)
async def update_job_offer_skill(
    id: str, payload: JobOfferSkillPayloadSchema
) -> JobOfferSkillResponseSchema:
    skill = await edit_job_offer_skill(id, payload)
    if not skill:
        raise HTTPException(status_code=404, detail=constant.JOB_OFFER_SKILL_NOT_FOUND)

    return skill
