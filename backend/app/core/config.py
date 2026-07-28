from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    database_url: str
    gemini_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None
    environment: str = "development"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
