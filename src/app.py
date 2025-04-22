from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter

from src.infrastructure.database import Engine
from src.infrastructure.redis_client import RedisClient
from src.settings import app_settings, db_settings
from src.api.routers import v1_router, v2_router
from src.api.exception_handlers import exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_url = getattr(app.state, "DATABASE_URL", db_settings.DATABASE_URL)
    redis_url = getattr(app.state, "REDIS_URL", app_settings.REDIS_URL)

    Engine.create(
        url=db_url,
        pool_size=db_settings.POOL_SIZE,
        max_overflow=db_settings.MAX_OVERFLOW,
    )
    RedisClient.create(url=redis_url)
    await FastAPILimiter.init(RedisClient.get())
    yield
    await Engine.dispose()
    await RedisClient.close()
    await FastAPILimiter.close()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan, exception_handlers=exception_handlers)
    app.include_router(v1_router)
    app.include_router(v2_router)
    return app
