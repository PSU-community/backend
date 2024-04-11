from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import TypedDict

import bcrypt
import jwt

from ..settings import settings


class TokenTypes(Enum):
    ACCESS = "access"
    REFRESH = "refresh"

    def __eq__(self, other):
        if isinstance(other, str):
            return other == self.value
        return super().__eq__(other)


class TokenData(TypedDict):
    type: str
    sub: str


def get_password_hash(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def verify_password_hash(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)


def create_jwt(*, type: TokenTypes, user_id: int, expire_delta: timedelta) -> str:
    payload = {
        "type": type.value,
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + expire_delta,
    }
    return jwt.encode(payload, settings.auth_jwt.PRIVATE_KEY, algorithm=settings.auth_jwt.algorithm)


def create_access_token(user_id: int):
    return create_jwt(type=TokenTypes.ACCESS, user_id=user_id, expire_delta=timedelta(minutes=15))


def create_refresh_token(user_id: int) -> str:
    return create_jwt(type=TokenTypes.REFRESH, user_id=user_id, expire_delta=timedelta(days=30))


def decode_access_token(token: str) -> dict:
    return TokenData(**jwt.decode(token, settings.auth_jwt.PUBLIC_KEY, algorithms=[settings.auth_jwt.algorithm]))
