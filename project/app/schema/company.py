import uuid

from pydantic import BaseModel


class UserPayloadSchema(BaseModel):
    name: str


class CompanyResponseSchema(UserPayloadSchema):
    id: uuid.UUID
