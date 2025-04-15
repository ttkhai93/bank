from ..repositories import UserRepository
from ..utils import hash_password, check_password


class UserService:
    async def get_users(self, **kwargs):
        return await UserRepository.get(**kwargs)

    async def create_user(self, user: dict):
        user["password"] = hash_password(user["password"])
        return await UserRepository.create(user)

    async def get_user_by_login_credentials(self, email: str, password: str):
        users = await UserRepository.get(email=email)
        if not users:
            return None

        user = users[0]
        if not check_password(password, user["password"]):
            return None

        return user
