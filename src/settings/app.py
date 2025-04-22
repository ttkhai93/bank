from .base import BaseSettings


class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    REDIS_URL: str = "redis://localhost:6379/0"


settings = Settings()
