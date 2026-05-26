# config/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from functools import lru_cache

load_dotenv()

class Settings(BaseModel):
    # ========== Project Paths ==========
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    DATA_DIR: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "data")
    UPLOAD_DIR: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "data/uploads")
    CHROMA_DB_DIR: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "chroma_db")
    LOG_DIR: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "logs")
    
    # ========== Embedding Model  ==========
    
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    
    # ========== Ollama Configuration ==========
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "phi3:mini")
    
    # ========== Groq API Configuration  ==========
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    
    
    
    # ========== Common API Parameters ==========
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "1024"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.2"))
    
    # ========== RAG Parameters  ==========
    CHUNK_SIZE: int = 300          # ৫০০ থেকে কমালাম (দ্রুত এম্বেডিং)
    CHUNK_OVERLAP: int = 30        # ৫০ থেকে কমালাম
    TOP_K_RESULTS: int = 2         # ৩ থেকে কমালাম 
    
    # ========== Logging ==========
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    def ensure_directories(self):
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        self.CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)
        self.LOG_DIR.mkdir(parents=True, exist_ok=True)

@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    settings.ensure_directories()
    return settings
