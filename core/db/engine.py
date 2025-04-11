from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

_engine: AsyncEngine | None = None


def create(connection_url: str, **kwargs):
    global _engine

    if _engine:
        raise Exception("Engine already created")
    _engine = create_async_engine(connection_url, **kwargs)


def get() -> AsyncEngine:
    if _engine is None:
        raise ValueError("Cannot get the engine because it hasn't been created")
    return _engine


async def dispose() -> None:
    global _engine

    if _engine:
        await _engine.dispose()
        _engine = None
