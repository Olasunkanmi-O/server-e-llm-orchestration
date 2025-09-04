import requests
from app.config import settings

class DeepSeekProvider:
    """Wrapper for DeepSeek API."""

    def __init__(self):
        self.api_key = settings.API_KEY  # single key
        self.model = settings.DEEPSEEK_MODEL or "deepseek-chat"

    def generate_response(self, prompt: str) -> dict:
        try:
            url = "https://api.deepseek.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
            }
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            text = data["choices"][0]["message"]["content"].strip()
            return {"text": text, "category": "General", "confidence": 0.9}
        except Exception as e:
            raise ValueError(f"DeepSeek API call failed: {str(e)}")
