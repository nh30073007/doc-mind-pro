import pytest
from src.core.vector_store import VectorStore
from src.core.chunker import TextChunker

def test_add_and_search(tmp_path, monkeypatch):
    monkeypatch.setattr("src.core.vector_store.settings.CHROMA_DB_DIR", tmp_path / "chroma")
    store = VectorStore()
    chunker = TextChunker(chunk_size=100)
    chunks = chunker.split_text("Artificial intelligence is great.")
    store.add_documents(chunks)
    results = store.search("AI", k=1)
    assert len(results) == 1
    store.delete_collection()