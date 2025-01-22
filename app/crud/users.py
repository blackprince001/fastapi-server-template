from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.security import get_hash
from app.models.users import User
from app.schemas.users import UserCreate


def create_user(db: Session, user: UserCreate) -> User:
    user.password = get_hash(user.password)
    db_user = User(**user.model_dump(exclude="password"))

    db_user.hashed_password = user.password

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
