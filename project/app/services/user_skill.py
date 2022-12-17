from typing import List, Union

from app.models.jobs import UserSkill, UserSkillSchema
from app.schema.user_skill import UserSkillPayloadSchema


async def add_user_skill(payload: UserSkillPayloadSchema) -> UserSkillSchema:
    user_skill = UserSkill(
        user_id=payload.user_id,
        skill_id=payload.skill_id,
        years_of_experience=payload.years_of_experience,
    )
    await user_skill.save()
    return user_skill


async def get_user_skill(id: str) -> Union[dict, None]:
    return await UserSkill.filter(id=id).first().values() or None


async def get_user_skills() -> List:
    return await UserSkill.all().values()


async def remove_user_skill(id: str) -> int:
    return await UserSkill.filter(id=id).first().delete()


async def edit_user_skill(
    id: str, payload: UserSkillPayloadSchema
) -> Union[dict, None]:
    user_skill = await UserSkill.filter(id=id).update(
        user_id=payload.user_id,
        skill_id=payload.skill_id,
        years_of_experience=payload.years_of_experience,
    )
    if user_skill:
        updated_skill = await UserSkill.filter(id=id).first().values()
        return updated_skill
    return None


async def get_user_skill_user_id(user_id: str) -> Union[dict, None]:
    return await UserSkill.filter(user_id=user_id).first().values() or None
