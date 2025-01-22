from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    hashed_password: str
    created_at: datetime


class UserResponse(User):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: EmailStr
    created_at: datetime


class UserLoginCredential(UserCreate):
    email: EmailStr
    password: str
