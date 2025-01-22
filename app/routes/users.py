from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import settings
from app.core.security import string_matches_hashed
from app.crud.users import create_user, get_user_by_email, get_users
from app.exceptions import UnauthorizedException
from app.routes.auth.jwt import create_access_token
from app.routes.deps.auth import AuthenticatedUser
from app.routes.deps.database import DatabaseConnection
from app.schemas.token import Token
from app.schemas.users import User, UserCreate, UserResponse

router = APIRouter(prefix="/users")


@router.post(
    "/",
    response_model=UserResponse,
    name="Create New user with UserCreate Information",
    status_code=status.HTTP_201_CREATED,
)
async def create_new_user(user: UserCreate, db: DatabaseConnection):
    return create_user(db=db, user=user)


@router.post(
    "/authenticate",
    name="Log In For Access Token",
    status_code=status.HTTP_200_OK,
)
async def authenticate_super_admin(
    db_connection: DatabaseConnection,
    credentials: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    user = get_user_by_email(db_connection, credentials.username)

    if user is None:
        raise UnauthorizedException()

    if not string_matches_hashed(
        plain=credentials.password,
        hashed=user.hashed_password,
    ):
        raise UnauthorizedException()

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expire_time=timedelta(minutes=settings.token_expiry_time),
    )

    return Token(access_token=access_token, token_type="bearer")


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
