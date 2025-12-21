from datetime import datetime, timezone
from typing import cast

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload

from crud import accounts as crud
import schemas
from config import get_jwt_auth_manager, get_settings, BaseAppSettings
from database import (
    get_db,
    UserModel,
    UserGroupModel,
    UserGroupEnum,
    ActivationTokenModel,
    PasswordResetTokenModel,
    RefreshTokenModel
)
from exceptions import BaseSecurityError
from security.interfaces import JWTAuthManagerInterface

router = APIRouter()

@router.post("/register", response_model=schemas.UserRegistrationResponseSchema, status_code=status.HTTP_201_CREATED)
async def register(user: schemas.UserRegistrationRequestSchema, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_email(db=db, email=user.email)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A user with this email {user.email} already exists."
        )

    new_user = await crud.create_user(db=db, user=user)
    await crud.create_activation_token(db=db, user_id=new_user.id)

    return new_user
