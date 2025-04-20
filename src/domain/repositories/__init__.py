from src.infrastructure.database import EntityRepository, begin as begin_transaction
from ..entities import users, account, asset, transaction


asset_repo = EntityRepository(asset)
users_repo = EntityRepository(users)
account_repo = EntityRepository(account)
transaction_repo = EntityRepository(transaction)
