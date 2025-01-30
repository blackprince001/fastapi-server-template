from uuid import UUID, uuid4

from sqlalchemy import UUID as UUIDType
from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(UUIDType, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # role: Mapped[UserRole] = mapped_column(
    #     Enum(UserRole, values_callable=lambda roles: [x.value for x in roles]),
    #     unique=False,
    #     default=UserRole.AGGREGATOR,
    # )
