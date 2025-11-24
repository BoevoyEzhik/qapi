from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB: str
    POSTGRES_DB: str
    SYNC_DRIVER: str
    ASYNC_DRIVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: int

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent / ".env", env_file_encoding="utf-8"
    )

    def get_db_url_async(self):
        return (
            f"{self.DB}+{self.ASYNC_DRIVER}://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        )

    def get_db_url_sync(self) -> str:
        return (
            f"{self.DB}+{self.SYNC_DRIVER}:"
            f"//{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
