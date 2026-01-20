from typing import List, Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    app_name: str = "MKJD Moderation API"
    environment: str = "local"
    debug: bool = False
    log_level: str = "INFO"
    api_v1_prefix: str = "/v1"
    database_url: str = "sqlite:///./mkjd.db"
    allow_origins: List[str] | str = ["*"]

    model_enabled: bool = False
    model_path: str = "../model_judol_bert"
    model_device: str = "cpu"
    model_max_length: int = 128
    model_batch_size: int = 16

    threshold_low: float = 0.4
    threshold_high: float = 0.7
    borderline_enabled: bool = True

    youtube_api_key: Optional[str] = None
    youtube_client_id: Optional[str] = None
    youtube_client_secret: Optional[str] = None
    youtube_redirect_uri: Optional[str] = None
    frontend_url: str = "http://localhost:3000/setup"

    @field_validator("allow_origins", mode="before")
    @classmethod
    def split_origins(cls, value):
        if isinstance(value, str):
            if value.strip() == "*":
                return ["*"]
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


settings = Settings()
