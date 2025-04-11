from ..repositories import UserRepository


class UserService:
    @staticmethod
    async def get_users(**kwargs):
        return await UserRepository.get(**kwargs)

    @staticmethod
    async def create_user(user):
        return await UserRepository.create(user)
