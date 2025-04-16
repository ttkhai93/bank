from core.services import account_service
from api import StandardAPIRouter
from api.schemas.account import TransferRequest


router = StandardAPIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("/transfer_isolation_level")
async def transfer_isolation_level(body: TransferRequest):
    transaction = await account_service.transfer_isolation_level(body.model_dump())
    return {"transaction": transaction}


@router.post("/transfer_optimistic_locking")
async def transfer_optimistic_locking(body: TransferRequest):
    transaction = (await account_service.transfer_optimistic_locking(body.model_dump()),)
    return {"transaction": transaction}
