from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/bank"
    DATABASE_ECHO: bool = False

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
