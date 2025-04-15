from .auth import router as auth_router
from .users import router as users_router
from .accounts import router as accounts_router
from .assets import router as assets_router


routers = [auth_router, users_router, accounts_router, assets_router]
