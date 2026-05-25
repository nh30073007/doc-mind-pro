# src/core/embedding_model.py
import torch
from langchain_huggingface import HuggingFaceEmbeddings
from config import get_settings

settings = get_settings()

class EmbeddingModel:
    def __init__(self, model_name=None):
        self.model_name = model_name or settings.EMBEDDING_MODEL
        # GPU চেক করা
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🖥️ এম্বেডিং ডিভাইস: {self.device.upper()}")
        self._embeddings = None

    @property
    def embeddings(self):
        if self._embeddings is None:
            model_kwargs = {'device': self.device}
            encode_kwargs = {'normalize_embeddings': True}
            self._embeddings = HuggingFaceEmbeddings(
                model_name=self.model_name,
                model_kwargs=model_kwargs,
                encode_kwargs=encode_kwargs
            )
        return self._embeddings