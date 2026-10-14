from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Real Estate Platform"
    environment: str = "development"

    database_url: str

    openai_api_key: str
    openai_model: str = "gpt-5.6"

    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str = "eu-north-1"
    s3_bucket_name: str

    @property
    def checkpoint_database_url(self) -> str:
        return self.database_url.replace(
            "postgresql+asyncpg://",
            "postgresql://",
            1,
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()