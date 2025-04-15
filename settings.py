from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/bank"
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
