from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_NAME = "FasApi Blog"
API_PREFIX = "/api/v1"

class Settings(BaseSettings):
    POSTGRES_PORT: str
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()


DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"


SWAGGER_PARAMETERS = {
    "syntaxHighlight.theme": "obsidian",
    "tryItOutEnabled": True,
    "displayOperationId": True,
    "filter": True,
    "requestSnippets": True,
    "defaultModelsExpandDepth": -1,
    "docExpansion": "none",
    "persistAuthorization": True,
    "displayRequestDuration": True,
}

