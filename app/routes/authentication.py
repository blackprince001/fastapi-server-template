from datetime import timedelta

from fastapi import APIRouter, status

from app.core.config import settings
from app.crud.authentication import (
    create_authentication,
    create_signin_code,
    verify_login,
    verify_user,
)
from app.crud.users import get_user_by_email
from app.exceptions import (
    AlreadyExistsException,
    InvalidVerificationCode,
    NotFoundException,
)
from app.routes.auth.jwt import create_access_token
from app.routes.deps.database import DatabaseConnection
from app.routes.deps.verification_email_service import (
    send_single_signon_code,
    send_verification_email,
)
from app.schemas.token import Token
from app.schemas.users import (
    UserCreate,
    UserLoginCredential,
    UserVerifyLoginCredential,
)

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/",
    name="Create New user with UserCreate Information",
    status_code=status.HTTP_201_CREATED,
)
async def signup(user: UserCreate, db: DatabaseConnection):
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
async def verify_signup(
    db: DatabaseConnection,
    email: str,
    verification_code: str,
) -> Token:
    verified, user = verify_user(db, email, verification_code)

    if verified:
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expire_time=timedelta(minutes=settings.token_expiry_time),
        )
        return Token(access_token=access_token, token_type="bearer")
    else:
        raise InvalidVerificationCode(
            status_code=400, detail="Invalid verification code"
        )


@router.post(
    "/login",
    name="Log In for Single Sign On Code",
    status_code=status.HTTP_200_OK,
)
async def login(
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
async def verify_user_login(
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
