from src.domain.repositories import asset_repo


async def get_assets(**kwargs):
    return await asset_repo.get(**kwargs)


async def create_asset(asset: dict):
    return await asset_repo.create(asset)
