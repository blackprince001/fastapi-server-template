import random
from datetime import datetime, timezone


def generate_verification_code() -> str:
    return str(random.randint(100000, 999999))


def is_verification_code_valid(
    verification_code: str, stored_code: str, expires_at: datetime
) -> bool:
    if not verification_code or not stored_code or not expires_at:
        return False
    current_time = datetime.now(timezone.utc)
    return verification_code == stored_code and current_time < expires_at


def is_signon_code_valid(sign_on_code: str, stored_code: str) -> bool:
    if not sign_on_code or not stored_code:
        return False
    return sign_on_code == stored_code
