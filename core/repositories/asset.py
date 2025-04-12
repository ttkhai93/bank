from ..models import asset
from .base import BaseRepository


class AssetRepository(BaseRepository):
    table = asset
