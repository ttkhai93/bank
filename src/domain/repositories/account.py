from src.infrastructure import EntityRepository
from ..entities import account


class AccountRepository(EntityRepository):
    entity = account
