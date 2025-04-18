from .base import BaseSettings


class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"


settings = Settings()
