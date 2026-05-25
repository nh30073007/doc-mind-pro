# src/ui/pages/admin.py
import streamlit as st
from config import get_settings
from src.core.vector_store import VectorStore

settings = get_settings()

def show():
    st.title("⚙️ অ্যাডমিন")
    st.write(f"**ডাটা ফোল্ডার:** {settings.DATA_DIR}")
    st.write(f"**ক্রোমা ডিবি:** {settings.CHROMA_DB_DIR}")
    if st.button("ডাটাবেজ রিসেট করো"):
        VectorStore().delete_collection()
        st.success("ডাটাবেজ রিসেট হয়েছে। সব ভেক্টর মুছে গেছে।")