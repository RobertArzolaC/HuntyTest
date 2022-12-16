import uuid

from pydantic import BaseModel


class UserPayloadSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    years_of_experience: int


class UserResponseSchema(UserPayloadSchema):
    id: uuid.UUID
