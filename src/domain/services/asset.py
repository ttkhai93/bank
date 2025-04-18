from src.domain.repositories import AssetRepository


async def get_assets(**kwargs):
    return await AssetRepository.get(**kwargs)


async def create_asset(asset: dict):
    return await AssetRepository.create(asset)
