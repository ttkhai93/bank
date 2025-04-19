from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine


class Engine:
    _engine: AsyncEngine | None = None

    @classmethod
    def create(cls, url: str, **kwargs) -> None:
        if cls._engine:
            raise ValueError("Engine already created")
        cls._engine = create_async_engine(url, **kwargs)

    @classmethod
    def get(cls, **execution_options) -> AsyncEngine:
        if not cls._engine:
            raise ValueError("Engine not initialized. Call create() first")
        return cls._engine.execution_options(**execution_options)

    @classmethod
    async def dispose(cls) -> None:
        if not cls._engine:
            return
        await cls._engine.dispose()
        cls._engine = None
