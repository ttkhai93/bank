from src.infrastructure.database.repository import EntityRepository
from ..entities import asset


class AssetRepository(EntityRepository):
    entity = asset
