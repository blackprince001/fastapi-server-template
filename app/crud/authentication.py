import base64
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.core.security import (
    generate_verification_code,
    is_signon_code_valid,
    is_verification_code_valid,
)
from app.crud.users import create_user
from app.models.authentication import Authentication
from app.models.users import User
from app.schemas.users import UserCreate


def create_authentication(db: Session, email: str) -> Authentication:
    verification_code = generate_verification_code()

    db_auth = Authentication(
        email=email,
        verification_code=verification_code,
        verification_code_expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
        sign_on_code=None,
        sign_on_code_expires_at=None,
    )

    db.add(db_auth)
    db.commit()
    db.refresh(db_auth)

    return db_auth


def get_auth(db: Session, auth_id: UUID) -> Optional[Authentication]:
    return (
        db.query(Authentication)
        .filter(Authentication.id == auth_id)
        .order_by(desc(Authentication.created_at))
        .first()
    )


def get_user_authentication_by_email(
    db: Session, email: str
) -> Optional[Authentication]:
    return (
        db.query(Authentication)
        .filter(Authentication.email == email)
        .order_by(desc(Authentication.created_at))
        .first()
    )


def verify_user(db: Session, email: str, verification_code: str) -> bool:
    auth = get_user_authentication_by_email(db, email)
    if not auth:
        return False

    base64_string = (
        base64.urlsafe_b64encode(secrets.token_bytes(16)).decode("utf-8").rstrip("=")
    )

    user_data = UserCreate(name=base64_string, email=email)
    user = create_user(db, user=user_data)

    if is_verification_code_valid(
        verification_code, auth.verification_code, auth.verification_code_expires_at
    ):
        auth.verification_code = None
        auth.verification_code_expires_at = None

        user.is_verified = True
        db.commit()

        return True

    return False


def verify_login(db: Session, email: str, sign_on_code: str) -> bool:
    auth = get_user_authentication_by_email(db, email)

    if not auth:
        return False

    if is_signon_code_valid(sign_on_code, auth.sign_on_code):
        auth.sign_on_code = None
        auth.sign_on_code_expires_at = None
        db.commit()

        return True

    return False


def create_signin_code(db: Session, user: User) -> Authentication:
    auth = get_user_authentication_by_email(db, user.email)

    auth.sign_on_code = generate_verification_code()
    auth.sign_on_code_expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)

    db.commit()

    return auth
