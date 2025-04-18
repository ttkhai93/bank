from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.infrastructure import Engine
from src.settings import db_settings
from src.api.routers import v1_router, v2_router
from src.exceptions import exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    url = getattr(app.state, "DATABASE_URL", db_settings.DATABASE_URL)

    Engine.create(
        url=url,
        pool_size=db_settings.POOL_SIZE,
        max_overflow=db_settings.MAX_OVERFLOW,
    )
    yield
    await Engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan, exception_handlers=exception_handlers)
    app.include_router(v1_router)
    app.include_router(v2_router)
    return app
