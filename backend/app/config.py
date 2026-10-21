from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env-prod",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # PostgreSQL
    POSTGRES_USER: Optional[str | None]
    POSTGRES_PASSWORD: Optional[str | None] 
    POSTGRES_DB: Optional[str | None] 
    POSTGRES_HOST: Optional[str | None] 
    POSTGRES_PORT: Optional[int | None] 

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
# print(settings.DATABASE_URL)