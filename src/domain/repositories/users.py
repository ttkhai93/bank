from src.infrastructure import EntityRepository
from ..entities import users


class UserRepository(EntityRepository):
    entity = users
