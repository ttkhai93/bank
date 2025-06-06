from typing import Annotated
from uuid import UUID

from fastapi import Query

from src.domain.services import account_service
from src.api.routers.standard_router import StandardAPIRouter
from src.api.schemas import CommonQueryParams
from src.api.schemas.account import CreateAccountRequest, TransferRequest


router = StandardAPIRouter(prefix="/accounts", tags=["Accounts"])


@router.get("")
async def get_accounts(query: Annotated[CommonQueryParams, Query()]):
    accounts = await account_service.get_accounts(**query.model_dump())
    return {"accounts": accounts}


@router.get("/{id}")
async def get_account_by_id(id: UUID):
    account = await account_service.get_account_by_id(id)
    return {"account": account}


@router.get("/{id}/transactions")
async def get_account_transactions(id: UUID):
    transactions = await account_service.get_account_transactions(id)
    return {"transactions": transactions}


@router.post("")
async def create_account(body: CreateAccountRequest):
    account = await account_service.create_account(body.model_dump())
    return {"account": account}


@router.post("/transfer")
async def transfer(body: TransferRequest):
    transaction = await account_service.transfer(body.model_dump())
    return {"transaction": transaction}


@router.delete("/{id}")
async def archive_account_by_id(id: UUID):
    account = await account_service.archive_account_by_id(id)
    return {"account": account}
