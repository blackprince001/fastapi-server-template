from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings

user_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.api_version}/users/verify-login",
    scheme_name="Users",
)
