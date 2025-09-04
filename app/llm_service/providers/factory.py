# app/llm_service/providers/factory.py

from app.llm_service.providers.openai_provider import OpenAIProvider
from app.llm_service.providers.anthropic_provider import AnthropicProvider
from app.llm_service.providers.deepseek_provider import DeepSeekProvider
from app.llm_service.providers.google_provider import GoogleProvider

def get_provider(provider_name: str):
    provider_name = provider_name.lower()
    if provider_name == "openai":
        return OpenAIProvider()
    elif provider_name == "anthropic":
        return AnthropicProvider()
    elif provider_name == "deepseek":
        return DeepSeekProvider()
    elif provider_name == "google":
        return GoogleProvider()
    else:
        raise ValueError(f"Unknown LLM provider: {provider_name}")

def get_api_key(provider: str) -> str:
    match provider:
        case "openai": return settings.OPENAI_API_KEY
        case "google": return settings.GEMINI_API_KEY
        case _: raise ValueError(f"No API key configured for provider: {provider}")
