from .base import BaseSettings


class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str
    ACCESS_TOKEN_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10


settings = Settings()
