"""
Модуль конфигурации приложения.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Настройки приложения.
    """
    DATABASE_URL: str = "postgresql://directory_user:directory_pass@db:5432/directory_db"
    API_KEY: str = "test-api-key-123"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
