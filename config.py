"""config.py - Summarization settings, chunk thresholds & API settings."""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", extra="ignore")

    PROJECT_NAME: str = "Multi-Document AI Summarization & Synthesis Engine"
    API_V1_STR: str = "/api/v1/summary"
    VERSION: str = "1.0.0"
    DOCS_URL: str = "/docs"

    APP_ENV: str = "development"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-3.5-turbo"

    # Map-Reduce Chunking parameters
    MAX_CHUNK_SIZE: int = 3000
    CHUNK_OVERLAP: int = 200

    # Storage Paths
    BASE_DIR: str = os.path.abspath(os.path.dirname(__file__))
    DOCS_INPUT_DIR: str = os.path.join(BASE_DIR, "docs_input")

    @property
    def is_mock_mode(self) -> bool:
        return not self.OPENAI_API_KEY or "your_openai_key" in self.OPENAI_API_KEY


settings = Settings()
os.makedirs(settings.DOCS_INPUT_DIR, exist_ok=True)