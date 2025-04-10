from logging import getLogger
from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.db import engine
from settings import settings

from api.routers import routers


logger = getLogger("uvicorn")


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Setting up resources before startup complete.")
    engine.create(settings.DATABASE_URL)
    yield
    logger.info("Cleaning up resources before shutdown complete.")
    await engine.dispose()


def create_app() -> FastAPI:
    new_app = FastAPI(lifespan=lifespan)

    for router in routers:
        new_app.include_router(router)

    return new_app


app = create_app()
