from src.infrastructure.database.repository import EntityRepository
from ..entities import users


class UserRepository(EntityRepository):
    entity = users
