from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from jose import JWTError, jwt

from app.core.config import settings
from app.crud.users import get_user
from app.exceptions import NotFoundException, UnauthorizedException
from app.routes.auth.oauth_scheme import security_scheme
from app.routes.deps.database import DatabaseConnection
from app.schemas.users import User


async def get_authenticated_user(
    db_connection: DatabaseConnection,
    token: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> User:
    token = token.credentials

    try:
        payload = jwt.decode(
            token,
            key=settings.secret_key,
            algorithms=["HS256"],
        )
    except JWTError:
        raise UnauthorizedException()

    try:
        user_id: UUID = UUID(payload.get("sub"))
    except (ValueError, TypeError):
        raise UnauthorizedException()

    try:
        return get_user(user_id=user_id, db=db_connection)
    except NotFoundException:
        raise UnauthorizedException()


AuthenticatedUser = Annotated[User, Depends(get_authenticated_user)]
