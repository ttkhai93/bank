import logging

import bcrypt

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
