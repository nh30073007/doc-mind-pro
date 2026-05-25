#!/usr/bin/env python
from sentence_transformers import SentenceTransformer
from config import get_settings

settings = get_settings()
print(f"📥 ডাউনলোড হচ্ছে: {settings.EMBEDDING_MODEL}")
model = SentenceTransformer(settings.EMBEDDING_MODEL)
model.save(str(settings.PROJECT_ROOT / "models" / settings.EMBEDDING_MODEL.replace("/", "_")))
print("✅ মডেল সেভ হয়েছে।")

# Ollama মডেল ডাউনলোডের জন্য নির্দেশনা
print(f"🦙 Ollama মডেল '{settings.OLLAMA_MODEL}' পেতে চালান: ollama pull {settings.OLLAMA_MODEL}")