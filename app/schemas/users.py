from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str
    created_at: datetime

    model_config = {"from_attributes": True}


class UserResponse(User):
    id: UUID
    name: str
    email: str
    created_at: datetime


class UserLoginCredential(UserCreate):
    email: str
    password: str
