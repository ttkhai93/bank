from core.db.transaction import Transaction
from core.db.decorators import retry_on_deadlock_error
from core.errors import ClientError
from ..repositories import AccountRepository, TransactionRepository


class AccountService:
    async def get_accounts(self, **kwargs):
        return await AccountRepository.get(**kwargs)

    async def create_account(self, account: dict):
        return await AccountRepository.create(account)

    @retry_on_deadlock_error()
    async def transfer(self, tx_info: dict):
        async with Transaction():
            from_account_id = tx_info["from_account_id"]
            to_account_id = tx_info["to_account_id"]
            amount = tx_info["amount"]

            from_account = await AccountRepository.get_by_id(from_account_id, with_for_update=True)
            to_account = await AccountRepository.get_by_id(to_account_id, with_for_update=True)

            if from_account["amount"] < amount:
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
