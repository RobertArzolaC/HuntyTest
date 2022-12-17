from typing import List

from app import constant
from app.schema.company import CompanyResponseSchema, UserPayloadSchema
from app.services.company import (
    add_company,
    edit_company,
    get_companies,
    get_company,
    remove_company,
)
from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.post(
    "/", response_model=CompanyResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_company(payload: UserPayloadSchema) -> CompanyResponseSchema:
    return await add_company(payload)


@router.get("/{id}/", response_model=CompanyResponseSchema)
async def read_company(id: str) -> CompanyResponseSchema:
    company = await get_company(id)
    if not company:
        raise HTTPException(status_code=404, detail=constant.COMPANY_NOT_FOUND)

    return company


@router.get("/", response_model=List[CompanyResponseSchema])
async def read_all_companies() -> List[CompanyResponseSchema]:
    return await get_companies()


@router.delete("/{id}/", response_model=CompanyResponseSchema)
async def delete_company(id: str) -> CompanyResponseSchema:
    company = await get_company(id)
    if not company:
        raise HTTPException(status_code=404, detail=constant.COMPANY_NOT_FOUND)

    await remove_company(id)

    return company


@router.put("/{id}/", response_model=CompanyResponseSchema)
async def update_company(id: str, payload: UserPayloadSchema) -> CompanyResponseSchema:
    company = await edit_company(id, payload)
    if not company:
        raise HTTPException(status_code=404, detail=constant.COMPANY_NOT_FOUND)

    return company
