from fastapi import APIRouter

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.get("")
async def get_accounts():
    return {"accounts": []}
