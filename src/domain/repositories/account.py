from .base import BaseRepository
from ..models import account


class AccountRepository(BaseRepository):
    entity = account
