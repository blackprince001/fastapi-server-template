from datetime import datetime, timedelta, timezone
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.security import (
    generate_verification_code,
    is_signon_code_valid,
    is_verification_code_valid,
)
from app.models.users import User
from app.schemas.users import UserCreate


def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(**user.model_dump())

    verification_code = generate_verification_code()

    db_user.verification_code = verification_code
    db_user.verification_code_expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=10
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user(db: Session, user_id: UUID) -> User:
    return db.query(User).where(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).where(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def verify_user(db: Session, email: str, verification_code: str) -> bool:
    user = get_user_by_email(db, email)
    if not user:
        return False

    if is_verification_code_valid(
        verification_code, user.verification_code, user.verification_code_expires_at
    ):
        user.verification_code = None
        user.verification_code_expires_at = None
        db.commit()
        return True

    return False


def verify_login(db: Session, email: str, sign_on_code: str) -> bool:
    user = get_user_by_email(db, email)

    if not user:
        return False

    if is_signon_code_valid(sign_on_code, user.sign_on_code):
        user.sign_on_code = None
        db.commit()

        return True

    return False


def create_signin_code(db: Session, user: User):
    user.sign_on_code = generate_verification_code()
    db.commit
