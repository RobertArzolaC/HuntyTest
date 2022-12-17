from typing import List

from app import constant
from app.schema.skill import SkillPayloadSchema, SkillResponseSchema
from app.services.skill import (
    add_skill,
    edit_skill,
    get_skill,
    get_skills,
    remove_skill,
)
from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.post(
    "/", response_model=SkillResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_skill(payload: SkillPayloadSchema) -> SkillResponseSchema:
    return await add_skill(payload)


@router.get("/{id}/", response_model=SkillResponseSchema)
async def read_skill(id: str) -> SkillResponseSchema:
    skill = await get_skill(id)
    if not skill:
        raise HTTPException(status_code=404, detail=constant.SKILL_NOT_FOUND)

    return skill


@router.get("/", response_model=List[SkillResponseSchema])
async def read_all_skills() -> List[SkillResponseSchema]:
    return await get_skills()


@router.delete("/{id}/", response_model=SkillResponseSchema)
async def delete_skill(id: str) -> SkillResponseSchema:
    skill = await get_skill(id)
    if not skill:
        raise HTTPException(status_code=404, detail=constant.SKILL_NOT_FOUND)

    await remove_skill(id)

    return skill


@router.put("/{id}/", response_model=SkillResponseSchema)
async def update_skill(id: str, payload: SkillPayloadSchema) -> SkillResponseSchema:
    skill = await edit_skill(id, payload)
    if not skill:
        raise HTTPException(status_code=404, detail=constant.SKILL_NOT_FOUND)

    return skill
