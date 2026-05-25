# src/ui/components/sidebar.py
import streamlit as st
from config import get_settings

def render_sidebar():
    s = get_settings()
    st.sidebar.title("ডক মাইন্ড")
    st.sidebar.info(f"**মডেল:** {s.OLLAMA_MODEL}\n**এম্বেডিং:** {s.EMBEDDING_MODEL.split('/')[-1]}")
    st.sidebar.caption("সব ডাটা লোকালি সংরক্ষিত।")