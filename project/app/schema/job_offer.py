import uuid

from pydantic import BaseModel


class JobOfferPayloadSchema(BaseModel):
    name: str
    currency: str
    salary: int
    url: str
    company_id: uuid.UUID


class JobOfferResponseSchema(JobOfferPayloadSchema):
    id: uuid.UUID
