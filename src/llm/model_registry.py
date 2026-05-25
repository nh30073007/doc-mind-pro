# src/llm/model_registry.py
MODEL_REGISTRY = {
    "qwen2.5:7b": {"context_length": 32768, "recommended": True, "description": "Qwen 2.5, ভালো বাংলা সাপোর্ট"},
    "gemma2:9b": {"context_length": 8192, "recommended": False, "description": "Google Gemma 2"},
    "llama3.2:3b": {"context_length": 128000, "recommended": False, "description": "Meta LLaMA 3.2"}
}

def get_recommended_models():
    return {k:v for k,v in MODEL_REGISTRY.items() if v.get("recommended")}