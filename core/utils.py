from bcrypt import hashpw, gensalt


def hash_password(plain_password: str) -> str:
    salt = gensalt()
    hashed_password = hashpw(plain_password.encode(), salt)
    return hashed_password.decode()
