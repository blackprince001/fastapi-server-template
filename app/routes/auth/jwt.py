from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from jose import jwt

from app.core.config import settings


def create_access_token(
    data: Dict[str, Any],
    expire_time: timedelta | None = None,
) -> str:
    to_encode = data.copy()

    if expire_time:
        expires_at = datetime.now(timezone.utc) + expire_time
    else:
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update(exp=expires_at, iat=datetime.now(timezone.utc))

    return jwt.encode(to_encode, key=settings.secret_key, algorithm="HS256")
