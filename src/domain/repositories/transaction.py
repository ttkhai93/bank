from src.infrastructure.database.repository import EntityRepository
from ..entities import transaction


class TransactionRepository(EntityRepository):
    entity = transaction
