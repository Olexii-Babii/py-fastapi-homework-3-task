from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import schemas
from database import UserModel, UserGroupModel, ActivationTokenModel
from security.passwords import hash_password


async def create_user(db: AsyncSession, user: schemas.UserRegistrationRequestSchema):
    hashed = hash_password(user.password)
    group = await db.scalar(select(UserGroupModel).where(UserGroupModel.name == "USER"))
    db_user = UserModel(
        email=str(user.email),
        _hashed_password=hashed,
        group_id=group.id
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user


async def get_user_by_email(db: AsyncSession, email: str):
    return await db.scalar(select(UserModel).where(UserModel.email == email))


async def create_activation_token(db: AsyncSession, user_id: int):
    activation_token = ActivationTokenModel(
        user_id=user_id
    )
    db.add(activation_token)
    await db.commit()
    await db.refresh(activation_token)

    return activation_token