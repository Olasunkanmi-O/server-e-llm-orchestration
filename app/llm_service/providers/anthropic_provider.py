from anthropic import Anthropic
from app.config import settings

class AnthropicProvider:
    """Wrapper around Anthropic's Claude API."""

    def __init__(self):
        self.client = Anthropic(api_key=settings.API_KEY)  # single key
        self.model = settings.ANTHROPIC_MODEL or "claude-3-opus-20240229"

    def generate_response(self, prompt: str) -> dict:
        try:
            response = self.client.messages.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            text = response.content[0].text.strip()
            return {"text": text, "category": "General", "confidence": 0.9}
        except Exception as e:
            raise ValueError(f"Anthropic API call failed: {str(e)}")
