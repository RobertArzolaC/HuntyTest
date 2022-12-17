from typing import List

from app import constant
from app.schema.user_skill import UserSkillPayloadSchema, UserSkillResponseSchema
from app.services.user_skill import (
    add_user_skill,
    edit_user_skill,
    get_user_skill,
    get_user_skills,
    remove_user_skill,
)
from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.post(
    "/", response_model=UserSkillResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_user_skill(payload: UserSkillPayloadSchema) -> UserSkillResponseSchema:
    return await add_user_skill(payload)


@router.get("/{id}/", response_model=UserSkillResponseSchema)
async def read_user_skill(id: str) -> UserSkillResponseSchema:
    skill = await get_user_skill(id)
    if not skill:
        raise HTTPException(status_code=404, detail=constant.USER_SKILL_NOT_FOUND)

    return skill


@router.get("/", response_model=List[UserSkillResponseSchema])
async def read_all_user_skills() -> List[UserSkillResponseSchema]:
    return await get_user_skills()


@router.delete("/{id}/", response_model=UserSkillResponseSchema)
async def delete_user_skill(id: str) -> UserSkillResponseSchema:
    skill = await get_user_skill(id)
    if not skill:
        raise HTTPException(status_code=404, detail=constant.USER_SKILL_NOT_FOUND)

    await remove_user_skill(id)

    return skill


@router.put("/{id}/", response_model=UserSkillResponseSchema)
async def update_user_skill(
    id: str, payload: UserSkillPayloadSchema
) -> UserSkillResponseSchema:
    skill = await edit_user_skill(id, payload)
    if not skill:
        raise HTTPException(status_code=404, detail=constant.USER_SKILL_NOT_FOUND)

    return skill
