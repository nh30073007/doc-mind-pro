import pytest
from src.core.rag_chain import RAGChain

# মকিং সহজ করার জন্য
def test_build_prompt():
    rag = RAGChain()
    prompt = rag._build_prompt("কি?", "ডকুমেন্ট", {"level": "বিগিনার", "language": "বাংলা"})
    assert "বিগিনার" in prompt
    assert "ডকুমেন্ট" in prompt