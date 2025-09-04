from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    LLM_PROVIDER: str = "openai"
    DATABASE_URL: str

    OPENAI_API_KEY: str
    GEMINI_API_KEY: str
    GOOGLE_MODEL: str = "gemini-1.5-pro-latest"





settings = Settings()

