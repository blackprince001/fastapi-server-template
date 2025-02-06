from typing import List
from uuid import UUID

from fastapi import APIRouter, status

from app.crud.users import get_user, get_users, update_user
from app.routes.deps.auth import AuthenticatedUser
from app.routes.deps.database import DatabaseConnection
from app.schemas.users import (
    User,
    UserResponse,
    UserUpdate,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/current",
    response_model=UserResponse,
    name="Get Currently Authenticated user Details",
    status_code=status.HTTP_200_OK,
)
async def get_current_user(user: AuthenticatedUser) -> User:
    return user


@router.get(
    "/",
    response_model=List[UserResponse],
    name="Get all users in the database with pagination",
    status_code=status.HTTP_200_OK,
)
def read_users(
    db: DatabaseConnection, user: AuthenticatedUser, skip: int = 0, limit: int = 100
):
    users = get_users(db, skip=skip, limit=limit)

    return users


@router.put(
    "/",
    response_model=UserResponse,
    name="Update User in the database with UserUpdate",
    status_code=status.HTTP_200_OK,
)
def update_user_router(
    db: DatabaseConnection, user: AuthenticatedUser, new_user: UserUpdate
):
    db_new_user = update_user(db, user_id=user.id, user_update=new_user)

    return db_new_user


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    name="Get User in the database with id",
    status_code=status.HTTP_200_OK,
)
def get_user_with_id(db: DatabaseConnection, user: AuthenticatedUser, user_id: UUID):
    db_user = get_user(db, user_id)

    return db_user
