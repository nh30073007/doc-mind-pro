import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from src.ui.pages import chat

def main():
    st.set_page_config(page_title="ডক মাইন্ড - DeepSeek ক্লোন", page_icon="🧠", layout="wide")
    chat.show()

if __name__ == "__main__":
    main()