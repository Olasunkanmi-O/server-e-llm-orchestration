import google.generativeai as genai
from app.config import settings

class GoogleProvider:
    """Wrapper for Google Gemini API."""

    def __init__(self):
        genai.configure(api_key=settings.API_KEY)  # single key
        self.model = settings.GOOGLE_MODEL or "gemini-1.5-pro-latest"
        self.client = genai.GenerativeModel(self.model)

    def generate_response(self, prompt: str) -> dict:
        try:
            response = self.client.generate_content(prompt)
            text = response.text.strip()
            return {"text": text, "category": "General", "confidence": 0.9}
        except Exception as e:
            raise ValueError(f"Google Gemini API call failed: {str(e)}")
