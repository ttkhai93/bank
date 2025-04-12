from .users import router as users_router
from .accounts import router as accounts_router
from .assets import router as assets_router


routers = [users_router, accounts_router, assets_router]
