import uuid

from pydantic import BaseModel


class UserSkillPayloadSchema(BaseModel):
    user_id: uuid.UUID
    skill_id: uuid.UUID
    years_of_experience: int


class UserSkillResponseSchema(UserSkillPayloadSchema):
    id: uuid.UUID
