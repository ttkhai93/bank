from uuid import UUID
from pydantic import BaseModel


class CreateAccountRequest(BaseModel):
    user_id: UUID
    asset_id: UUID
