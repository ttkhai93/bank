from src.domain.repositories import users_repo


async def get_users(**kwargs):
    return await users_repo.get(**kwargs)


async def create_user(user: dict):
    return await users_repo.create(user)
