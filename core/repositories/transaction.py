from .base import BaseRepository
from ..models import transaction


class TransactionRepository(BaseRepository):
    table = transaction
