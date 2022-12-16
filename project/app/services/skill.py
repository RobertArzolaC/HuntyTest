from typing import List, Union
from app.models.jobs import Skill, SkillSchema
from app.schema.skill import SkillPayloadSchema


async def add_skill(payload: SkillPayloadSchema) -> SkillSchema:
    skill = Skill(name=payload.name)
    await skill.save()
    return skill


async def get_skill(id: str) -> Union[dict, None]:
    return await Skill.filter(id=id).first().values() or None


async def get_skills() -> List:
    return await Skill.all().values()


async def remove_skill(id: str) -> int:
    return await Skill.filter(id=id).first().delete()


async def edit_skill(id: str, payload: SkillPayloadSchema) -> Union[dict, None]:
    skill = await Skill.filter(id=id).update(name=payload.name)
    if skill:
        updated_skill = await Skill.filter(id=id).first().values()
        return updated_skill
    return None
