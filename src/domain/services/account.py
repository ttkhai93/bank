from uuid import UUID

from tenacity import retry, retry_if_exception_message, stop_after_attempt, wait_random_exponential

from src.exceptions import ClientError
from src.domain.repositories import begin_transaction, account_repo, transaction_repo


async def get_accounts(**kwargs):
    return await account_repo.get(**kwargs)


async def get_account_by_id(account_id: UUID):
    return await account_repo.get_by_id(account_id)


async def archive_account_by_id(account_id: UUID):
    accounts = await account_repo.archive(id=account_id)
    return accounts[0]


async def get_account_transactions(account_id: UUID):
    account = await account_repo.get_by_id(account_id)

    sql = "SELECT * FROM transaction WHERE to_account_id = :account_id or from_account_id = :account_id"
    return await account_repo.execute_sql_string(sql, account_id=account["id"])


async def create_account(account: dict):
    return await account_repo.create(account)


def account_has_enough_balance(account_balance, transfer_amount):
    return account_balance >= transfer_amount


@retry(
    retry=retry_if_exception_message(match=r".*DeadlockDetectedError.*deadlock detected.*"),
    stop=stop_after_attempt(4),
    wait=wait_random_exponential(multiplier=0.1, min=0.1),
)
async def transfer(tx_info: dict):
    async with begin_transaction():
        from_account_id = tx_info["from_account_id"]
        to_account_id = tx_info["to_account_id"]
        amount = tx_info["amount"]

        from_account = await account_repo.get_by_id(from_account_id, for_update=True)
        to_account = await account_repo.get_by_id(to_account_id, for_update=True)

        if not account_has_enough_balance(account_balance=from_account["amount"], transfer_amount=amount):
            raise ClientError(
                "Account doesn't have enough funds. Amount: {amount}, Transfer amount: {transfer_amount}".format(
                    amount=int(from_account["amount"]), transfer_amount=amount
                ),
            )

        if from_account["asset_id"] != to_account["asset_id"]:
            raise ClientError("Cannot transfer to a different asset account.")

        await account_repo.update({"amount": from_account["amount"] - amount}, id=from_account_id)
        await account_repo.update({"amount": to_account["amount"] + amount}, id=to_account_id)

        return await transaction_repo.create(tx_info)


@retry(
    retry=retry_if_exception_message(match=r".*DeadlockDetectedError.*deadlock detected.*"),
    stop=stop_after_attempt(4),
    wait=wait_random_exponential(multiplier=0.1, min=0.1),
)
@retry(
    retry=retry_if_exception_message(
        match=r".*SerializationError.*could not serialize access due to concurrent update.*"
    ),
    stop=stop_after_attempt(4),
    wait=wait_random_exponential(multiplier=0.1, min=0.1),
)
async def transfer_isolation_level(tx_info: dict):
    async with begin_transaction(isolation_level="REPEATABLE READ"):
        from_account_id = tx_info["from_account_id"]
        to_account_id = tx_info["to_account_id"]
        amount = tx_info["amount"]

        from_account = await account_repo.get_by_id(from_account_id)
        to_account = await account_repo.get_by_id(to_account_id)

        if not account_has_enough_balance(account_balance=from_account["amount"], transfer_amount=amount):
            raise ClientError(
                "Account doesn't have enough funds. Amount: {amount}, Transfer amount: {transfer_amount}".format(
                    amount=int(from_account["amount"]), transfer_amount=amount
                ),
            )

        if from_account["asset_id"] != to_account["asset_id"]:
            raise ClientError("Cannot transfer to a different asset account.")

        await account_repo.update({"amount": from_account["amount"] - amount}, id=from_account_id)
        await account_repo.update({"amount": to_account["amount"] + amount}, id=to_account_id)

        return await transaction_repo.create(tx_info)


@retry(
    retry=retry_if_exception_message(match=r".*DeadlockDetectedError.*deadlock detected.*"),
    stop=stop_after_attempt(4),
    wait=wait_random_exponential(multiplier=0.1, min=0.1),
)
@retry(
    retry=retry_if_exception_message(match=r".*Version conflict.*"),
    stop=stop_after_attempt(4),
    wait=wait_random_exponential(multiplier=0.1, min=0.1),
)
async def transfer_optimistic_locking(tx_info: dict):
    async with begin_transaction():
        from_account_id = tx_info["from_account_id"]
        to_account_id = tx_info["to_account_id"]
        amount = tx_info["amount"]

        from_account = await account_repo.get_by_id(from_account_id)
        to_account = await account_repo.get_by_id(to_account_id)

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

        res1 = await account_repo.update(
            {"amount": from_account["amount"] - amount, "version": from_account_target_version + 1},
            id=from_account_id,
            version=from_account_target_version,
        )
        res2 = await account_repo.update(
            {"amount": to_account["amount"] + amount, "version": to_account_target_version + 1},
            id=to_account_id,
            version=to_account_target_version,
        )

        if not res1 or not res2:
            raise ValueError("Version conflict")

        return await transaction_repo.create(tx_info)
