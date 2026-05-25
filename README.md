# 🧠 Doc Mind – AI Document Assistant

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35.0-red.svg)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.0-green.svg)](https://python.langchain.com/)
[![Groq](https://img.shields.io/badge/Groq-API-purple.svg)](https://console.groq.com)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

> Production‑grade RAG (Retrieval-Augmented Generation) system with DeepSeek‑style UI.  
> Upload PDF, DOCX, TXT – ask questions – get instant answers using Groq’s ultra‑fast LLM.

## ✨ Key Features

- 📄 **Auto‑process files** – just upload, no extra button.
- 💬 **Chat with your documents** – context‑aware answers.
- 🎨 **DeepSeek‑style UI** – dark/light theme, chat history.
- ⚡ **Streaming responses** – type‑as‑you‑see.
- 🧠 **Local embeddings** (all‑MiniLM‑L6‑v2) with GPU support.
- 🔐 **100% private** – your data never leaves your machine (except API calls to Groq/Gemini).

## 🏗️ Architecture
User → Streamlit UI → RAGChain → Vector Store (ChromaDB)
↓ ↓
Groq API ← Embedding Model (local)


## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Groq API key (free) from [console.groq.com](https://console.groq.com)

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/doc-mind.git
cd doc-mind



2. Setup virtual environment
bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
# or
venv\Scripts\activate      # Windows
3. Install dependencies
bash
pip install -r requirements.txt
4. Configure environment
bash
cp .env.example .env
# Edit .env – add your GROQ_API_KEY
5. Run the app
bash
streamlit run src/main.py



📁 Project Structure 
text
doc-mind/
├── config/                 # Pydantic settings, logging config
├── src/
│   ├── core/               # RAG core (chunker, embedding, vector store, chain)
│   ├── llm/                # Groq/Gemini clients
│   ├── agents/             # Interest analyzer, memory manager
│   ├── ui/                 # Streamlit pages & components
│   └── utils/              # Text cleaning, file helpers
├── tests/                  # Unit tests
├── scripts/                # Reset DB, backup, download models
├── docs/                   # Setup, architecture, privacy
├── .env.example
├── .gitignore
├── requirements.txt
├── Makefile
├── Dockerfile
├── docker-compose.yml
└── README.md
🧪 Testing
bash
pytest tests/ -v

🤝 Contributing
Contributions are welcome. Please open an issue first.

📄 License
MIT © [a.h.m nazmul hasan]

🙏 Acknowledgements
Groq – Lightning‑fast inference

LangChain – RAG framework

Streamlit – UI magic