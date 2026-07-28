from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/accounting"
    secret_key: str = "dev-secret-key-change-in-production"
    google_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash-exp"
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai"

    class Config:
        env_file = ".env"


settings = Settings()
