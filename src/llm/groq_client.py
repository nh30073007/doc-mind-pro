# src/llm/groq_client.py
import logging
from groq import Groq
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class GroqClient:
    def __init__(self, api_key=None, model=None):
        self.api_key = api_key or settings.GROQ_API_KEY
        self.model = model or settings.GROQ_MODEL
        if not self.api_key:
            raise ValueError("GROQ_API_KEY missing in .env")
        self.client = Groq(api_key=self.api_key)

    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=temperature,
                max_tokens=settings.MAX_TOKENS,
                stream=False,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            return "দুঃখিত, ভাষা মডেলটি উত্তর দিতে পারেনি।"

    def generate_stream(self, prompt: str, temperature: float = 0.7):
        try:
            stream = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=temperature,
                max_tokens=settings.MAX_TOKENS,
                stream=True,
            )
            for chunk in stream:
                # কখনো কখনো chunk.choices খালি হতে পারে
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                else:
                    # কোনো content না থাকলে skip
                    continue
        except Exception as e:
            logger.error(f"Groq streaming error: {e}")
            # স্ট্রিমিং ব্যর্থ হলে ফলব্যাক হিসেবে পুরো উত্তর জেনারেট করে দিই
            fallback = self.generate(prompt, temperature)
            yield fallback