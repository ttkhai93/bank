from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncConnection

_engine: AsyncEngine | None = None


def create(url: str, **kwargs) -> None:
    global _engine

    if _engine:
        raise ValueError("Engine already created")
    _engine = create_async_engine(url, **kwargs)


def get() -> AsyncEngine:
    if _engine is None:
        raise ValueError("Cannot get the engine because it hasn't been created")
    return _engine


async def get_connection(**execution_options) -> AsyncConnection:
    engine = get()
    connection = await engine.connect()
    connection = await connection.execution_options(**execution_options)
    return connection


async def dispose() -> None:
    global _engine

    if _engine is None:
        raise ValueError("Cannot dispose the engine because it hasn't been created")

    await _engine.dispose()
    _engine = None


@asynccontextmanager
async def context(url):
    try:
        create(url)
        yield
    finally:
        await dispose()
