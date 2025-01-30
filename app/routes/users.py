from datetime import timedelta
from typing import List

from fastapi import APIRouter, status

from app.core.config import settings
from app.crud.authentication import (
    create_authentication,
    create_signin_code,
    verify_login,
    verify_user,
)
from app.crud.users import (
    get_user_by_email,
    get_users,
)
from app.exceptions import (
    AlreadyExistsException,
    InvalidVerificationCode,
    NotFoundException,
)
from app.routes.auth.jwt import create_access_token
from app.routes.deps.auth import AuthenticatedUser
from app.routes.deps.database import DatabaseConnection
from app.routes.deps.verification_email_service import (
    send_single_signon_code,
    send_verification_email,
)
from app.schemas.token import Token
from app.schemas.users import (
    User,
    UserCreate,
    UserLoginCredential,
    UserResponse,
    UserVerifyLoginCredential,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    name="Create New user with UserCreate Information",
    status_code=status.HTTP_201_CREATED,
)
async def create_new_user(user: UserCreate, db: DatabaseConnection):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise AlreadyExistsException(detail="User with email already exists")

    auth = create_authentication(db, user.email)
    send_verification_email(user.email, auth.verification_code)

    return {"message": "Verification code sent successfully"}


@router.post(
    "/verify-signup",
    name="Verify User with Verification Code",
    status_code=status.HTTP_200_OK,
)
async def verify_user_with_code(
    db: DatabaseConnection,
    email: str,
    verification_code: str,
):
    if verify_user(db, email, verification_code):
        return {"message": "User verified successfully"}
    else:
        raise InvalidVerificationCode(
            status_code=400, detail="Invalid verification code"
        )


@router.post(
    "/login",
    name="Log In for Single Sign On Code",
    status_code=status.HTTP_200_OK,
)
async def single_sign_on(
    db_connection: DatabaseConnection,
    credentials: UserLoginCredential,
):
    db_user = get_user_by_email(db_connection, credentials.email)

    if db_user is None:
        raise NotFoundException()

    auth = create_signin_code(db_connection, db_user)
    send_single_signon_code(db_user.email, auth.sign_on_code)

    return {"message": "Signin code sent successfully"}


@router.post(
    "/verify-login",
    name="Log In For Access Token",
    status_code=status.HTTP_200_OK,
)
async def authenticate_super_admin(
    db_connection: DatabaseConnection,
    credentials: UserVerifyLoginCredential,
) -> Token:
    db_user = get_user_by_email(db_connection, credentials.email)

    if db_user is None:
        raise NotFoundException()

    verify_login(db_connection, db_user.email, credentials.sign_on_code)

    access_token = create_access_token(
        data={"sub": str(db_user.id)},
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
