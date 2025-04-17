import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.db import engine
from settings import app_settings, db_settings
from api.routers import v1_router, v2_router
from api.exception_handlers import exception_handlers


logging.basicConfig(level=app_settings.LOG_LEVEL)
logging.getLogger("sqlalchemy.engine").setLevel(app_settings.LOG_LEVEL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    url = getattr(app.state, "DATABASE_URL", db_settings.DATABASE_URL)

    engine.create(
        url=url,
        pool_size=db_settings.POOL_SIZE,
        max_overflow=db_settings.MAX_OVERFLOW,
    )
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(v1_router)
app.include_router(v2_router)

for exc_class, handler in exception_handlers:
    app.add_exception_handler(exc_class, handler)
