from ..repositories import AssetRepository


class AssetService:
    async def get_assets(self, **kwargs):
        return await AssetRepository.get(**kwargs)

    async def create_asset(self, asset: dict):
        return await AssetRepository.create(asset)
