from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/bank"
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str
    ACCESS_TOKEN_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
