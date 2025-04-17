from .base import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/dbname"
    POOL_SIZE: int = 5  # The number of connections is always maintained in the pool, available for immediate reuse
    MAX_OVERFLOW: int = 10  # The number of temporary connections can be open when POOL_SIZE is exhausted


settings = Settings()
