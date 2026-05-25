import pytest
from pathlib import Path
from src.core.document_processor import DocumentProcessor

def test_process_txt(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hello world", encoding="utf-8")
    result = DocumentProcessor.process_file(file)
    assert "text" in result
    assert result["text"] == "hello world"
    assert result["metadata"]["extension"] == ".txt"