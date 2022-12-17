from typing import List, Union

from app.models.jobs import User, UserSchema
from app.schema.company import UserPayloadSchema


async def add_company(payload: UserPayloadSchema) -> UserSchema:
    company = User(name=payload.name)
    await company.save()
    return company


async def get_company(id: str) -> Union[dict, None]:
    return await User.filter(id=id).first().values() or None


async def get_companies() -> List:
    return await User.all().values()


async def remove_company(id: str) -> int:
    return await User.filter(id=id).first().delete()


async def edit_company(id: str, payload: UserPayloadSchema) -> Union[dict, None]:
    company = await User.filter(id=id).update(name=payload.name)
    if company:
        updated_company = await User.filter(id=id).first().values()
        return updated_company
    return None
