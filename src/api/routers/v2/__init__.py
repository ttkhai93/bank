from fastapi import APIRouter
from .accounts import router as accounts_router


router = APIRouter(prefix="/v2")
router.include_router(accounts_router)
