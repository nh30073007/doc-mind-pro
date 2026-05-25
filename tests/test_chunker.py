from src.core.chunker import TextChunker

def test_chunking():
    chunker = TextChunker(chunk_size=50, chunk_overlap=10)
    text = "a " * 100
    chunks = chunker.split_text(text)
    assert len(chunks) > 1
    assert "chunk_index" in chunks[0]["metadata"]