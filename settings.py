from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    PASSWORD_MIN_LENGTH: int = 6
    SECRET_KEY: str

    DATABASE_URL: str = "sqlite+aiosqlite:///db.sqlite3"


config = Config()

__all__ = ("config",)
