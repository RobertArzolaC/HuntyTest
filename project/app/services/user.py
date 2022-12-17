from typing import List, Union

from app.models.jobs import User, UserSchema
from app.schema.user import UserPayloadSchema


async def add_user(payload: UserPayloadSchema) -> UserSchema:
    user = User(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        years_of_experience=payload.years_of_experience,
    )
    await user.save()
    return user


async def get_user(id: str) -> Union[dict, None]:
    return await User.filter(id=id).first().values() or None


async def get_users() -> List:
    return await User.all().values()


async def remove_user(id: str) -> int:
    return await User.filter(id=id).first().delete()


async def edit_user(id: str, payload: UserPayloadSchema) -> Union[dict, None]:
    user = await User.filter(id=id).update(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        years_of_experience=payload.years_of_experience,
    )
    if user:
        updated_user = await User.filter(id=id).first().values()
        return updated_user
    return None
