from core.db import engine
from contextlib import asynccontextmanager


@asynccontextmanager
async def ctx_engine(postgres_url):
    try:
        engine.create(postgres_url)
        yield engine
    finally:
        await engine.dispose()
