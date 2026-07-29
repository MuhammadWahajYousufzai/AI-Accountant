from urllib.parse import urlencode, urlparse, urlunparse, parse_qs

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/accounting"
    secret_key: str = "dev-secret-key-change-in-production"
    cors_origins: str = "*"
    google_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai"

    class Config:
        env_file = ".env"

    @property
    def async_database_url(self) -> str:
        url = self.database_url
        if url.startswith("postgresql://") and "+asyncpg" not in url:
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        parsed = urlparse(url)
        parsed = parsed._replace(query="")
        return urlunparse(parsed)


settings = Settings()
