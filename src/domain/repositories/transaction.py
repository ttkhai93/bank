from .base import BaseRepository
from ..models import transaction


class TransactionRepository(BaseRepository):
    entity = transaction
