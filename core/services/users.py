from ..repositories import UserRepository


class UserService:
    @staticmethod
    async def get_users():
        return await UserRepository.search()
