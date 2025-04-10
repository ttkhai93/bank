from ..repositories import UserRepository


class UserService:
    @staticmethod
    async def get_users(**kwargs):
        return await UserRepository.get(**kwargs)
