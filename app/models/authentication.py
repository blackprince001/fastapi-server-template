import datetime
from uuid import UUID, uuid4

from sqlalchemy import UUID as UUIDType
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class Authentication(Base):
    __tablename__ = "authentication"

    id: Mapped[UUID] = mapped_column(UUIDType, primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        unique=True,
    )
    verification_code: Mapped[str] = mapped_column(String, nullable=True)
    verification_code_expires_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    sign_on_code: Mapped[str] = mapped_column(String, nullable=True)
    sign_on_code_expires_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
