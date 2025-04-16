from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

_engine: AsyncEngine | None = None


def create(url: str, **kwargs) -> None:
    global _engine

    if _engine:
        raise ValueError("Engine already created")

    _engine = create_async_engine(url, **kwargs)


def get(**execution_options) -> AsyncEngine:
    if _engine is None:
        raise ValueError("Cannot get the engine because it hasn't been created")

    return _engine.execution_options(**execution_options)


async def dispose() -> None:
    global _engine

    if _engine is None:
        raise ValueError("Cannot dispose the engine because it hasn't been created")

    await _engine.dispose()
    _engine = None
