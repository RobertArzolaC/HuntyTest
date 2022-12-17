from typing import List, Union

from app.models.jobs import Company, CompanySchema
from app.schema.company import CompanyPayloadSchema


async def add_company(payload: CompanyPayloadSchema) -> CompanySchema:
    company = Company(name=payload.name)
    await company.save()
    return company


async def get_company(id: str) -> Union[dict, None]:
    return await Company.filter(id=id).first().values() or None


async def get_companies() -> List:
    return await Company.all().values()


async def remove_company(id: str) -> int:
    return await Company.filter(id=id).first().delete()


async def edit_company(id: str, payload: CompanyPayloadSchema) -> Union[dict, None]:
    company = await Company.filter(id=id).update(name=payload.name)
    if company:
        updated_company = await Company.filter(id=id).first().values()
        return updated_company
    return None
