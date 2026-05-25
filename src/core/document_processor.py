# src/core/document_processor.py
from pathlib import Path
import hashlib
import PyPDF2
from docx import Document
from src.utils.text_cleaner import clean_text

class DocumentProcessor:
    @staticmethod
    def process_file(file_path) -> dict:
        # 🔧 ফিক্স: যদি file_path স্ট্রিং হয়, তাহলে Path এ কনভার্ট করো
        if not isinstance(file_path, Path):
            file_path = Path(file_path)
        
        ext = file_path.suffix.lower()
        if ext == ".pdf":
            text = DocumentProcessor._read_pdf(file_path)
        elif ext == ".docx":
            text = DocumentProcessor._read_docx(file_path)
        elif ext in [".txt", ".md"]:
            text = file_path.read_text(encoding="utf-8")
        else:
            raise ValueError(f"অসমর্থিত ফাইল টাইপ: {ext}")
        
        text = clean_text(text)
        file_hash = hashlib.md5(file_path.read_bytes()).hexdigest()
        return {
            "text": text,
            "metadata": {
                "source": str(file_path),
                "filename": file_path.name,
                "hash": file_hash,
                "size_kb": file_path.stat().st_size / 1024,
                "extension": ext
            }
        }
    
    @staticmethod
    def _read_pdf(path: Path) -> str:
        text = ""
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    
    @staticmethod
    def _read_docx(path: Path) -> str:
        doc = Document(path)
        return "\n".join([para.text for para in doc.paragraphs])