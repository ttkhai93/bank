from src.infrastructure import EntityRepository
from ..entities import transaction


class TransactionRepository(EntityRepository):
    entity = transaction
