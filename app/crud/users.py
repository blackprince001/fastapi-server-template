from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.security import get_hash
from app.models.users import User
from app.schemas.users import UserCreate


async def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(**user.model_dump())

    db_user.hashed_password = get_hash(user.password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


async def get_user(db: Session, user_id: UUID) -> User:
    return db.query(User).where(User.id == user_id).first()


async def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).where(User.email == email).first()


async def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()
