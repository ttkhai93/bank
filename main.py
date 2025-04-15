import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.db import engine
from settings import settings
from api.routers import v1_router, v2_router
from api.exception_handlers import exception_handlers


logging.basicConfig(level=settings.LOG_LEVEL)
logging.getLogger("sqlalchemy.engine").setLevel(settings.LOG_LEVEL)


@asynccontextmanager
async def lifespan(_: FastAPI):
    engine.create(settings.DATABASE_URL)
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    new_app = FastAPI(lifespan=lifespan)
    new_app.include_router(v1_router)
    new_app.include_router(v2_router)

    for exc_class, handler in exception_handlers:
        new_app.exception_handler(exc_class)(handler)

    return new_app


app = create_app()
