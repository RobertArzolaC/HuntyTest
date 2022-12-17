import uuid

from pydantic import BaseModel


class UserPayloadSchema(BaseModel):
    name: str
    currency: str
    salary: int
    url: str
    company_id: uuid.UUID


class UserResponseSchema(UserPayloadSchema):
    id: uuid.UUID
