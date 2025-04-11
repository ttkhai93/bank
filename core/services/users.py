from ..repositories import UserRepository
from ..utils import hash_password


class UserService:
    async def get_users(self, **kwargs):
        return await UserRepository.get(**kwargs)

    async def create_user(self, user: dict):
        user["password"] = hash_password(user["password"])
        return await UserRepository.create(user)
