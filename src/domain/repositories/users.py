from .base import BaseRepository
from ..models import users


class UserRepository(BaseRepository):
    table = users
