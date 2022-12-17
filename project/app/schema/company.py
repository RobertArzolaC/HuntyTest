import uuid

from pydantic import BaseModel


class CompanyPayloadSchema(BaseModel):
    name: str


class CompanyResponseSchema(CompanyPayloadSchema):
    id: uuid.UUID
