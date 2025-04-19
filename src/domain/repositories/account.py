from src.infrastructure.database.repository import EntityRepository
from ..entities import account


class AccountRepository(EntityRepository):
    entity = account
