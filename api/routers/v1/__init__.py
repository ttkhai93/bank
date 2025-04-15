from api import StandardAPIRouter
from .auth import router as auth_router
from .users import router as users_router
from .accounts import router as accounts_router
from .assets import router as assets_router


router = StandardAPIRouter(prefix="/v1")


router.include_router(auth_router)
router.include_router(users_router)
router.include_router(accounts_router)
router.include_router(assets_router)
