from uuid import UUID
from pydantic import BaseModel


class CreateAccountRequest(BaseModel):
    user_id: UUID
    asset_id: UUID


class TransferRequest(BaseModel):
    from_account_id: UUID
    to_account_id: UUID
    amount: int
