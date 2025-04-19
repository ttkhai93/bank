from src.domain.repositories import UserRepository


async def get_users(**kwargs):
    return await UserRepository.get(**kwargs)


async def create_user(user: dict):
    return await UserRepository.create(user)
