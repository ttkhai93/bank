from typing import Annotated

from fastapi import Query

from core.services import AccountService
from api import StandardAPIRouter
from api.schemas import CommonQueryParams
from api.schemas.account import CreateAccountRequest


router = StandardAPIRouter(prefix="/accounts", tags=["Accounts"])
account_service = AccountService()


@router.get("/")
async def get_accounts(query: Annotated[CommonQueryParams, Query()]):
    accounts = await account_service.get_accounts(**query.model_dump())
    return {"accounts": accounts}


@router.post("/")
async def create_account(body: CreateAccountRequest):
    account = await account_service.create_account(body.model_dump())
    return {"account": account}
