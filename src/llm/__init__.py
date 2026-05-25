# src/llm/__init__.py
from .ollama_client import OllamaClient
from .model_registry import MODEL_REGISTRY

__all__ = ["OllamaClient", "MODEL_REGISTRY"]