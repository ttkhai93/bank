import logging
from datetime import datetime, timedelta

import jwt
import bcrypt

from core.errors import UnauthorizedError
from settings import app_settings

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
        "exp": datetime.now() + timedelta(minutes=app_settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, app_settings.SECRET_KEY, algorithm=app_settings.ACCESS_TOKEN_ALGORITHM)


def verify_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, app_settings.SECRET_KEY, algorithms=[app_settings.ACCESS_TOKEN_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise UnauthorizedError("Access token has expired")
    except jwt.InvalidTokenError as exc:
        logger.debug(exc)
        raise UnauthorizedError("Invalid access token")
