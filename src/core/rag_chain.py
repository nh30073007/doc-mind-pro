# src/core/rag_chain.py
from src.core.vector_store import VectorStore
from src.llm.groq_client import GroqClient   # ← GroqClient ইম্পোর্ট
from config import get_settings

settings = get_settings()

class RAGChain:
    def __init__(self):
        self.vector_store = VectorStore()
        self.llm = GroqClient()               # ← GroqClient ব্যবহার
    
    def ask(self, query: str, interest: dict = None) -> str:
        results = self.vector_store.search(query, k=settings.TOP_K_RESULTS)
        if not results:
            return "দুঃখিত, আপনার প্রশ্নের সাথে প্রাসঙ্গিক কোনো ডকুমেন্ট খুঁজে পাওয়া যায়নি।"
        
        contexts = [f"[{score:.2f}] {doc.page_content}" for doc, score in results]
        context_text = "\n\n---\n\n".join(contexts)
        prompt = self._build_prompt(query, context_text, interest)
        return self.llm.generate(prompt)        # ← GroqClient-এর generate() কল
    
    def ask_stream(self, query: str, interest: dict = None):
        """স্ট্রিমিং উত্তরের জন্য জেনারেটর (Groq API স্ট্রিমিং সমর্থন করে)"""
        results = self.vector_store.search(query, k=settings.TOP_K_RESULTS)
        if not results:
            yield "দুঃখিত, আপনার প্রশ্নের সাথে প্রাসঙ্গিক কোনো ডকুমেন্ট খুঁজে পাওয়া যায়নি।"
            return
        
        contexts = [f"[{score:.2f}] {doc.page_content}" for doc, score in results]
        context_text = "\n\n---\n\n".join(contexts)
        prompt = self._build_prompt(query, context_text, interest)
        
        for chunk in self.llm.generate_stream(prompt):   # ← GroqClient-এর স্ট্রিমিং
            yield chunk
    
    def _build_prompt(self, query: str, context: str, interest: dict) -> str:
        level = interest.get("level", "মাঝারি") if interest else "মাঝারি"
        lang = interest.get("language", "বাংলা") if interest else "বাংলা"
        tone = interest.get("tone", "বন্ধুত্বপূর্ণ") if interest else "বন্ধুত্বপূর্ণ"
        
        # Groq মডেল ইংরেজিতে সবচেয়ে ভালো কাজ করে
        return f"""You are a helpful assistant. Answer based on the following document.

Level: {level}
Language: {lang} (if you can answer in Bengali, do so; otherwise answer in English)
Tone: {tone}

Document:
{context}

Question: {query}

Answer:"""