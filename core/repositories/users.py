from ..models import users
from .base import BaseRepository


class UserRepository(BaseRepository):
    table = users
