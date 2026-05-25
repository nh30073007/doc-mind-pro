# src/ui/pages/chat.py
import streamlit as st
import tempfile
import os
import uuid
from datetime import datetime
from pathlib import Path
from src.core.document_processor import DocumentProcessor
from src.core.chunker import TextChunker
from src.core.vector_store import VectorStore
from src.agents.interest_analyzer import InterestAnalyzer
from src.agents.memory_manager import MemoryManager
from src.core.rag_chain import RAGChain

# ---------- থিম ফাংশন ----------
def toggle_theme():
    current = st.session_state.get("theme", "dark")
    st.session_state.theme = "light" if current == "dark" else "dark"
    st.rerun()

def get_theme_css():
    if st.session_state.get("theme", "dark") == "dark":
        return """
        <style>
        .stApp { background-color: #0f0f0f; color: #e5e5e5; font-family: 'Inter', sans-serif; }
        [data-testid="stSidebar"] { background-color: #1a1a1a; border-right: 1px solid #2d2d2d; }
        .stChatMessage [data-testid="stChatMessageContent"] { background-color: #1e1e1e; border-radius: 16px; padding: 12px 16px; color: #e5e5e5; }
        .stChatInputContainer textarea { background-color: #2d2d2d; border: 1px solid #3d3d3d; border-radius: 24px; color: white; }
        .stButton button { background-color: #2d2d2d; color: white; border-radius: 20px; }
        .stFileUploader { background-color: #1a1a1a; border: 1px dashed #4c9aff; border-radius: 16px; }
        </style>
        """
    else:
        return """
        <style>
        .stApp { background-color: #ffffff; color: #1a1a1a; font-family: 'Inter', sans-serif; }
        [data-testid="stSidebar"] { background-color: #f5f5f5; border-right: 1px solid #e0e0e0; }
        .stChatMessage [data-testid="stChatMessageContent"] { background-color: #f0f0f0; border-radius: 16px; padding: 12px 16px; }
        .stChatInputContainer textarea { background-color: #ffffff; border: 1px solid #cccccc; border-radius: 24px; }
        .stButton button { background-color: #e0e0e0; color: #1a1a1a; border-radius: 20px; }
        .stFileUploader { background-color: #f9f9f9; border: 1px dashed #4c9aff; border-radius: 16px; }
        </style>
        """

# ---------- সেশন ইনিশিয়ালাইজেশন ----------
def init_session():
    if "sessions" not in st.session_state:
        st.session_state.sessions = {}
    if "current_session_id" not in st.session_state:
        new_id = str(uuid.uuid4())
        st.session_state.sessions[new_id] = {
            "name": "নতুন চ্যাট",
            "messages": [],
            "created_at": datetime.now(),
            "last_updated": datetime.now()
        }
        st.session_state.current_session_id = new_id
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = VectorStore()
    if "chunker" not in st.session_state:
        st.session_state.chunker = TextChunker()
    if "interest_analyzer" not in st.session_state:
        st.session_state.interest_analyzer = InterestAnalyzer()
    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = RAGChain()
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"
    # ট্র্যাক রাখার জন্য কোন ফাইল আগে প্রসেস হয়েছে
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = set()

def create_new_session():
    new_id = str(uuid.uuid4())
    st.session_state.sessions[new_id] = {
        "name": "নতুন চ্যাট",
        "messages": [],
        "created_at": datetime.now(),
        "last_updated": datetime.now()
    }
    st.session_state.current_session_id = new_id
    st.rerun()

def delete_session(session_id):
    if session_id in st.session_state.sessions:
        del st.session_state.sessions[session_id]
        if st.session_state.current_session_id == session_id:
            if st.session_state.sessions:
                st.session_state.current_session_id = list(st.session_state.sessions.keys())[0]
            else:
                create_new_session()
        st.rerun()

def rename_session(session_id, new_name):
    if session_id in st.session_state.sessions:
        st.session_state.sessions[session_id]["name"] = new_name[:50]
        st.rerun()

# ---------- অটো ফাইল প্রসেসিং (কোনো বাটন ছাড়া) ----------
def auto_process_file(uploaded_file):
    """ফাইল আপলোড হলেই স্বয়ংক্রিয়ভাবে প্রসেস করবে"""
    if uploaded_file is None:
        return
    # চেক করা ইতিমধ্যে এই ফাইল প্রসেস হয়েছে কিনা (নাম + সাইজ দিয়ে)
    file_key = f"{uploaded_file.name}_{uploaded_file.size}"
    if file_key in st.session_state.processed_files:
        return  # ইতিমধ্যে প্রসেস করা
    
    try:
        file_name = uploaded_file.name
        extension = Path(file_name).suffix
        if not extension:
            extension = ".pdf"
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name
        
        # প্রসেসিং শুরু
        with st.spinner(f"🔄 প্রসেসিং: {file_name}"):
            doc_data = DocumentProcessor.process_file(tmp_path)
            chunks = st.session_state.chunker.split_text(doc_data["text"], doc_data["metadata"])
            st.session_state.vector_store.add_documents(chunks)
            st.session_state.processed_files.add(file_key)
            
            # সফল মেসেজ চ্যাটে যোগ
            current_session = st.session_state.sessions[st.session_state.current_session_id]
            current_session["messages"].append({
                "role": "assistant",
                "content": f"📘 `{file_name}` আপলোড ও সফলভাবে প্রসেস করা হয়েছে। এখন প্রশ্ন করতে পারেন।"
            })
            # সেশন আপডেট সময়
            current_session["last_updated"] = datetime.now()
            # UI রিফ্রেশ
            st.rerun()
    except Exception as e:
        st.error(f"❌ প্রসেস ব্যর্থ: {str(e)}")
    finally:
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)

# ---------- মূল UI ----------
def show():
    init_session()
    st.markdown(get_theme_css(), unsafe_allow_html=True)
    
    # সাইডবার
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="color: #4c9aff;">🧠 ডক মাইন্ড</h2>
            <p style="font-size: 0.8rem; color: #888;">AI Document Assistant</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("➕ নতুন চ্যাট", use_container_width=True):
            create_new_session()
        
        st.divider()
        st.markdown("### 📋 চ্যাট ইতিহাস")
        sessions_to_show = sorted(st.session_state.sessions.items(), key=lambda x: x[1]["last_updated"], reverse=True)
        for sid, data in sessions_to_show:
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(f"💬 {data['name'][:30]}", key=f"btn_{sid}", use_container_width=True):
                    st.session_state.current_session_id = sid
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"del_{sid}"):
                    delete_session(sid)
        
        st.divider()
        st.markdown("### 📎 ফাইল আপলোড")
        # auto_process_file চালানোর জন্য on_change ইভেন্ট ব্যবহার
        uploaded_file = st.file_uploader(
            "ফাইল নির্বাচন করুন (PDF, DOCX, TXT)",
            type=['pdf', 'docx', 'txt'],
            key="auto_uploader",
            label_visibility="collapsed",
            on_change=lambda: auto_process_file(st.session_state.auto_uploader)
        )
        # initial call if file already present
        if uploaded_file is not None:
            auto_process_file(uploaded_file)
        
        st.divider()
        st.markdown("### 🤖 মডেল")
        model_option = st.selectbox(
            "মডেল নির্বাচন করুন",
            ["Groq (llama-3.1-8b-instant)", "Gemini (gemini-2.0-flash)"],
            index=0,
            key="model_selector",
            label_visibility="collapsed"
        )
        
        st.divider()
        st.markdown("### ⚙️ সেটিংস")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("🎨 থিম:")
        with col2:
            if st.button("🌙 ডার্ক" if st.session_state.theme == "light" else "☀️ লাইট"):
                toggle_theme()
    
    # মূল চ্যাট এলাকা
    current_session = st.session_state.sessions[st.session_state.current_session_id]
    messages = current_session["messages"]
    
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 1rem;">
        <h1 style="font-weight: 600;">{current_session['name']}</h1>
        <p style="color: #888;">AI ডকুমেন্ট অ্যাসিস্ট্যান্ট</p>
    </div>
    """, unsafe_allow_html=True)
    
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    prompt = st.chat_input("প্রশ্ন লিখুন (ইংরেজি বা বাংলা)...")
    if prompt:
        st.chat_message("user").markdown(prompt)
        messages.append({"role": "user", "content": prompt})
        current_session["last_updated"] = datetime.now()
        
        interest = st.session_state.interest_analyzer.analyze(prompt)
        
        with st.chat_message("assistant"):
            msg_placeholder = st.empty()
            full_response = ""
            try:
                for chunk in st.session_state.rag_chain.ask_stream(prompt, interest):
                    if chunk:
                        full_response += chunk
                        msg_placeholder.markdown(full_response + "▌")
                msg_placeholder.markdown(full_response)
            except Exception as e:
                full_response = f"❌ ত্রুটি: {str(e)}"
                msg_placeholder.markdown(full_response)
        messages.append({"role": "assistant", "content": full_response})
        current_session["last_updated"] = datetime.now()
        
        if len(messages) == 2:
            new_name = prompt[:30] + ("..." if len(prompt) > 30 else "")
            rename_session(st.session_state.current_session_id, new_name)
        
        st.rerun()