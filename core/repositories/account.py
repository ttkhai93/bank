from ..models import account
from .base import BaseRepository


class AccountRepository(BaseRepository):
    table = account
