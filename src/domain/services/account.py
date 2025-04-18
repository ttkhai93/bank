from uuid import UUID

from src.infrastructure.database import transaction
from src.decorators import retry_on_deadlock_error, retry_on_serialization_error, retry_on_version_conflict_error
from src.errors import ClientError
from src.domain.repositories import AccountRepository, TransactionRepository


async def get_accounts(**kwargs):
    return await AccountRepository.get(**kwargs)


async def get_account_by_id(account_id: UUID):
    return await AccountRepository.get_by_id(account_id)


async def get_account_transactions(account_id: UUID):
    account = await AccountRepository.get_by_id(account_id)

    sql = "SELECT * FROM transaction WHERE to_account_id = :account_id or from_account_id = :account_id"
    return await transaction.execute_text_clause(sql, account_id=account["id"])


async def create_account(account: dict):
    return await AccountRepository.create(account)


def account_has_enough_balance(account_balance, transfer_amount):
    return account_balance >= transfer_amount


@retry_on_deadlock_error()
async def transfer(tx_info: dict):
    async with transaction.context():
        from_account_id = tx_info["from_account_id"]
        to_account_id = tx_info["to_account_id"]
        amount = tx_info["amount"]

        from_account = await AccountRepository.get_by_id(from_account_id, for_update=True)
        to_account = await AccountRepository.get_by_id(to_account_id, for_update=True)

        if not account_has_enough_balance(account_balance=from_account["amount"], transfer_amount=amount):
            raise ClientError(
                "Account doesn't have enough funds. Amount: {amount}, Transfer amount: {transfer_amount}".format(
                    amount=int(from_account["amount"]), transfer_amount=amount
                ),
            )

        if from_account["asset_id"] != to_account["asset_id"]:
            raise ClientError("Cannot transfer to a different asset account.")

        await AccountRepository.update({"amount": from_account["amount"] - amount}, id=from_account_id)
        await AccountRepository.update({"amount": to_account["amount"] + amount}, id=to_account_id)

        return await TransactionRepository.create(tx_info)


@retry_on_deadlock_error()
@retry_on_serialization_error()
async def transfer_isolation_level(tx_info: dict):
    async with transaction.context(isolation_level="REPEATABLE READ"):
        from_account_id = tx_info["from_account_id"]
        to_account_id = tx_info["to_account_id"]
        amount = tx_info["amount"]

        from_account = await AccountRepository.get_by_id(from_account_id)
        to_account = await AccountRepository.get_by_id(to_account_id)

        if not account_has_enough_balance(account_balance=from_account["amount"], transfer_amount=amount):
            raise ClientError(
                "Account doesn't have enough funds. Amount: {amount}, Transfer amount: {transfer_amount}".format(
                    amount=int(from_account["amount"]), transfer_amount=amount
                ),
            )

        if from_account["asset_id"] != to_account["asset_id"]:
            raise ClientError("Cannot transfer to a different asset account.")

        await AccountRepository.update({"amount": from_account["amount"] - amount}, id=from_account_id)
        await AccountRepository.update({"amount": to_account["amount"] + amount}, id=to_account_id)

        return await TransactionRepository.create(tx_info)


@retry_on_deadlock_error()
@retry_on_version_conflict_error()
async def transfer_optimistic_locking(tx_info: dict):
    async with transaction.context():
        from_account_id = tx_info["from_account_id"]
        to_account_id = tx_info["to_account_id"]
        amount = tx_info["amount"]

        from_account = await AccountRepository.get_by_id(from_account_id)
        to_account = await AccountRepository.get_by_id(to_account_id)

        if not account_has_enough_balance(account_balance=from_account["amount"], transfer_amount=amount):
            raise ClientError(
                "Account doesn't have enough funds. Amount: {amount}, Transfer amount: {transfer_amount}".format(
                    amount=int(from_account["amount"]), transfer_amount=amount
                ),
            )

        if from_account["asset_id"] != to_account["asset_id"]:
            raise ClientError("Cannot transfer to a different asset account.")

        from_account_target_version = from_account["version"]
        to_account_target_version = to_account["version"]

        res1 = await AccountRepository.update(
            {"amount": from_account["amount"] - amount, "version": from_account_target_version + 1},
            id=from_account_id,
            version=from_account_target_version,
        )
        res2 = await AccountRepository.update(
            {"amount": to_account["amount"] + amount, "version": to_account_target_version + 1},
            id=to_account_id,
            version=to_account_target_version,
        )

        if not res1 or not res2:
            raise ValueError("Version conflict")

        return await TransactionRepository.create(tx_info)
