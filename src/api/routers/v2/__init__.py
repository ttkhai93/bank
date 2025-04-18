from src.api import StandardAPIRouter
from .accounts import router as accounts_router


router = StandardAPIRouter(prefix="/v2")


router.include_router(accounts_router)
