# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_KEY: str  # single API key for all LLMs
    LLM_PROVIDER: str = "openai"  # default provider
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
