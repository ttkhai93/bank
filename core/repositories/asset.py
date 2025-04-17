from .base import BaseRepository
from ..models import asset


class AssetRepository(BaseRepository):
    table = asset
