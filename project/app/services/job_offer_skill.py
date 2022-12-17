from typing import List, Union

from app.models.jobs import JobOfferSkill, JobOfferSkillSchema
from app.schema.job_offer_skill import JobOfferSkillPayloadSchema


async def add_job_offer_skill(
    payload: JobOfferSkillPayloadSchema,
) -> JobOfferSkillSchema:
    job_offer_skill = JobOfferSkill(
        job_offer_id=payload.job_offer_id,
        skill_id=payload.skill_id,
        years_of_experience=payload.years_of_experience,
    )
    await job_offer_skill.save()
    return job_offer_skill


async def get_job_offer_skill(id: str) -> Union[dict, None]:
    return await JobOfferSkill.filter(id=id).first().values() or None


async def get_job_offer_skills() -> List:
    return await JobOfferSkill.all().values()


async def remove_job_offer_skill(id: str) -> int:
    return await JobOfferSkill.filter(id=id).first().delete()


async def edit_job_offer_skill(
    id: str, payload: JobOfferSkillPayloadSchema
) -> Union[dict, None]:
    job_offer_skill = await JobOfferSkill.filter(id=id).update(
        job_offer_id=payload.job_offer_id,
        skill_id=payload.skill_id,
        years_of_experience=payload.years_of_experience,
    )
    if job_offer_skill:
        updated_job_offer_skill = await JobOfferSkill.filter(id=id).first().values()
        return updated_job_offer_skill
    return None
