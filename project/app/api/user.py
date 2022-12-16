from typing import List

from fastapi import APIRouter, HTTPException, status

from app import constant
from app.services.user import add_user, edit_user, get_user, get_users, remove_user
from app.schema.user import UserPayloadSchema, UserResponseSchema

router = APIRouter()


@router.post("/", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserPayloadSchema) -> UserResponseSchema:
    return await add_user(payload)


@router.get("/{id}/", response_model=UserResponseSchema)
async def read_user(id: str) -> UserResponseSchema:
    job_offer = await get_user(id)
    if not job_offer:
        raise HTTPException(status_code=404, detail=constant.USER_NOT_FOUND)

    return job_offer


@router.get("/", response_model=List[UserResponseSchema])
async def read_all_users() -> List[UserResponseSchema]:
    return await get_users()


@router.delete("/{id}/", response_model=UserResponseSchema)
async def delete_user(id: str) -> UserResponseSchema:
    job_offer = await get_users(id)
    if not job_offer:
        raise HTTPException(status_code=404, detail=constant.USER_NOT_FOUND)

    await remove_user(id)

    return job_offer


@router.put("/{id}/", response_model=UserResponseSchema)
async def update_user(id: str, payload: UserPayloadSchema) -> UserResponseSchema:
    job_offer = await edit_user(id, payload)
    if not job_offer:
        raise HTTPException(status_code=404, detail=constant.USER_NOT_FOUND)

    return job_offer
