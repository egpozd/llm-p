from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(validation_alias="APP_NAME")
    env: str = Field(validation_alias="ENV")

    jwt_secret: str = Field(validation_alias="JWT_SECRET")
    jwt_alg: str = Field(validation_alias="JWT_ALG")
    access_token_expire_minutes: int = Field(
        validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    sqlite_path: str = Field(validation_alias="SQLITE_PATH")

    openrouter_api_key: str = Field(default="", validation_alias="OPENROUTER_API_KEY")
    openrouter_base_url: str = Field(validation_alias="OPENROUTER_BASE_URL")
    openrouter_model: str = Field(validation_alias="OPENROUTER_MODEL")
    openrouter_site_url: str = Field(validation_alias="OPENROUTER_SITE_URL")
    openrouter_app_name: str = Field(validation_alias="OPENROUTER_APP_NAME")

    cors_origins: list[str] = []


settings = Settings()