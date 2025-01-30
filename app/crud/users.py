from datetime import datetime, timedelta, timezone
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.security import (
    generate_verification_code,
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
