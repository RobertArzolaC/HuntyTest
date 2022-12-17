import uuid

from pydantic import BaseModel


class SkillPayloadSchema(BaseModel):
    name: str


class SkillResponseSchema(SkillPayloadSchema):
    id: uuid.UUID
