from ..models import transaction
from .base import BaseRepository


class TransactionRepository(BaseRepository):
    table = transaction
