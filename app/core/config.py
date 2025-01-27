from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/appdb",
        alias="DATABASE_URL",
    )
    secret_key: str = Field(alias="SECRET_KEY")
    token_expiry_time: int = Field(alias="TOKEN_EXPIRY_TIME")
    api_version: str = Field(alias="API_VERSION")
    email_sender: str = Field(alias="EMAIL_SENDER")
    resend_api_key: str = Field(alias="RESEND_API_KEY")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
