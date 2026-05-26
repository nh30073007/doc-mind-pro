# src/llm/ollama_client.py
import requests
import json
import logging
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class OllamaClient:
    def __init__(self, base_url=None, model=None):
        self.base_url = base_url or settings.OLLAMA_BASE_URL
        self.model = model or settings.OLLAMA_MODEL
        self.generate_url = f"{self.base_url}/api/generate"
    
    def generate(self, prompt: str, temperature=0.7) -> str:
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "temperature": temperature,
            "num_predict": 256          
        }
        try:
            response = requests.post(self.generate_url, json=payload)
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            logger.error(f"Ollama কল ব্যর্থ: {e}")
            return "দুঃখিত, ভাষা মডেলটি উত্তর দিতে পারেনি। Ollama চলছে কি না যাচাই করুন।"
    
    def generate_stream(self, prompt: str, temperature=0.7):
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,              
            "temperature": temperature,
            "num_predict": 256           
        }
        try:
            response = requests.post(self.generate_url, json=payload, stream=True)
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        if 'response' in data:
                            yield data['response']
                        if data.get('done', False):
                            break
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            logger.error(f"Ollama স্ট্রিম কল ব্যর্থ: {e}")
            yield "দুঃখিত, স্ট্রিমিং উত্তর দিতে ব্যর্থ হয়েছে।"
