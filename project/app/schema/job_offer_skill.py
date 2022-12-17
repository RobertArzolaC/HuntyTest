import uuid

from pydantic import BaseModel


class JobOfferSkillPayloadSchema(BaseModel):
    job_offer_id: uuid.UUID
    skill_id: uuid.UUID
    years_of_experience: int


class JobOfferSkillResponseSchema(JobOfferSkillPayloadSchema):
    id: uuid.UUID
