from api import StandardAPIRouter


router = StandardAPIRouter(prefix="/accounts", tags=["Accounts"])


@router.get("")
async def get_accounts():
    return {"accounts": []}
