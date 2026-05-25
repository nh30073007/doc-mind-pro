# আর্কিটেকচার

- **অ্যাপ** : Streamlit
- **ভেক্টর ডাটাবেজ** : ChromaDB (লোকাল)
- **এম্বেডিং** : BAAI/bge-small-en-v1.5 (লোকাল)
- **LLM** : Ollama + qwen2.5:7b
- **মেমোরি** : SQLite (metadata.db)
- **পার্সিং** : PyPDF2, python-docx

সব কম্পোনেন্ট লোকালি চলে। কোনো ডাটা বাইরে যায় না।