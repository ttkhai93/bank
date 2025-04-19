from datetime import datetime, timedelta

import jwt

from src.exceptions import UnauthorizedError
from src.settings import jwt_settings


def create_access_token(user_id: str) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.now() + timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, jwt_settings.SECRET_KEY, algorithm=jwt_settings.ACCESS_TOKEN_ALGORITHM)


def verify_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, jwt_settings.SECRET_KEY, algorithms=[jwt_settings.ACCESS_TOKEN_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise UnauthorizedError("Access token has expired")
    except jwt.InvalidTokenError:
        raise UnauthorizedError("Invalid access token")
