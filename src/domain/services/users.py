from src.domain.repositories import UserRepository
from src.api.security.password import hash_password, check_password


async def get_users(**kwargs):
    return await UserRepository.get(**kwargs)


async def create_user(user: dict):
    user["password"] = hash_password(user["password"])
    return await UserRepository.create(user)


async def get_user_by_login_credentials(email: str, password: str):
    users = await UserRepository.get(email=email)
    if not users:
        return None

    user = users[0]
    if not check_password(password, user["password"]):
        return None

    return user
