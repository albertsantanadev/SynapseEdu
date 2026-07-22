from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Tipagem explícita: se DATABASE_URL não existir no .env,
    # a aplicação falha ao subir, com um erro claro apontando o campo faltante.
    database_url: str
    gemini_api_key: str
    environment: str = "development"  # tem um default, então é opcional

    # Isso instrui o Pydantic a procurar essas variáveis também num arquivo .env
    # (e não só nas variáveis de ambiente reais do sistema operacional).
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Instância única, importada por qualquer outro módulo que precise de config.
settings = Settings()