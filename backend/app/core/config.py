from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    database_url: str
    
    # Torne a chave do Gemini opcional (default None) para não bloquear o servidor
    gemini_api_key: Optional[str] = None
    
    # Adicione a chave da Groq
    groq_api_key: Optional[str] = None

    class Config:
        env_file = ".env"
        extra = "ignore" # Ignora variáveis extras no .env sem dar erro

settings = Settings()