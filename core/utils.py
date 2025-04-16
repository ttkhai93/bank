import logging
from datetime import datetime, timedelta

import jwt
import bcrypt

from core.errors import ClientError
from settings import settings

logger = logging.getLogger(__name__)


def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_password.encode(), salt)
    return hashed_password.decode()


def check_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
    except ValueError as exc:
        logger.debug("Exception happens in check_password: %s", exc)
        return False


def create_access_token(user_id: str) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ACCESS_TOKEN_ALGORITHM)


def verify_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ACCESS_TOKEN_ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise ClientError("Access token has expired")
    except jwt.InvalidTokenError as exc:
        logger.debug(exc)
        raise ClientError("Invalid access token")
