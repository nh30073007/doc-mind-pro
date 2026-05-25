# src/ui/pages/upload.py
import streamlit as st
import shutil
from config import get_settings
from src.core.document_processor import DocumentProcessor
from src.core.chunker import TextChunker
from src.core.vector_store import VectorStore

settings = get_settings()

def show():
    st.title("📄 ফাইল আপলোড")
    files = st.file_uploader("PDF, DOCX, TXT, MD ফাইল আপলোড করুন", type=['pdf','docx','txt','md'], accept_multiple_files=True)
    if files and st.button("প্রসেস করো"):
        vector_store = VectorStore()
        chunker = TextChunker()
        for f in files:
            path = settings.UPLOAD_DIR / f.name
            with open(path, "wb") as buffer:
                buffer.write(f.getbuffer())
            doc = DocumentProcessor.process_file(path)
            chunks = chunker.split_text(doc["text"], doc["metadata"])
            vector_store.add_documents(chunks)
            st.success(f"{f.name} প্রসেস হয়েছে")
        st.success("সব ফাইল সফলভাবে সংরক্ষিত!")