from ..repositories import AccountRepository


class AccountService:
    async def get_accounts(self, **kwargs):
        return await AccountRepository.get(**kwargs)

    async def create_account(self, account: dict):
        return await AccountRepository.create(account)
