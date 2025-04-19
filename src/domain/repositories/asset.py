from src.infrastructure import EntityRepository
from ..entities import asset


class AssetRepository(EntityRepository):
    entity = asset
