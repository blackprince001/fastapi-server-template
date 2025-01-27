from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class User(BaseModel):
    id: int
    name: str
    email: EmailStr

    created_at: datetime

    sign_on_code: str | None

    verification_code: str | None
    verification_code_expires_at: datetime | None


class UserResponse(User):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: EmailStr
    created_at: datetime


class UserLoginCredential(BaseModel):
    email: EmailStr


class UserVerifyLoginCredential(BaseModel):
    email: EmailStr
    sign_on_code: str
