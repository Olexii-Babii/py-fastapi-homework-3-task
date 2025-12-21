from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, field_validator

from database import accounts_validators


class UserBase(BaseModel):
    email: EmailStr


class UserRegistrationRequestSchema(UserBase):
    password: str


    @field_validator("email")
    @classmethod
    def validate_email(cls, email: EmailStr):
        return accounts_validators.validate_email(str(email))

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str):
        return accounts_validators.validate_password_strength(password)

class UserRegistrationResponseSchema(UserBase):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class UserActivationRequestSchema(BaseModel):
    pass


class MessageResponseSchema(BaseModel):
    pass


class PasswordResetRequestSchema(BaseModel):
    pass


class PasswordResetCompleteRequestSchema(BaseModel):
    pass


class UserLoginResponseSchema(BaseModel):
    pass


class UserLoginRequestSchema(BaseModel):
    pass


class TokenRefreshRequestSchema(BaseModel):
    pass


class TokenRefreshResponseSchema(BaseModel):
    pass
