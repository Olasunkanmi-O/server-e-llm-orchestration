# app/llm_service/providers/openai_provider.py
import openai
from app.config import settings

class OpenAIProvider:
    def __init__(self):
        openai.api_key = settings.API_KEY
        self.model = "gpt-4o-mini"

    def generate_response(self, prompt: str) -> dict:
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.choices[0].message.content.strip()
        return {"text": text, "category": "General", "confidence": 0.9}
