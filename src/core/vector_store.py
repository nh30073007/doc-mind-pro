# src/core/vector_store.py
import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document
from config import get_settings
from src.core.embedding_model import EmbeddingModel

settings = get_settings()

class VectorStore:
    def __init__(self):
        self.persist_dir = str(settings.CHROMA_DB_DIR)
        self.embedding_model = EmbeddingModel()
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        self.collection_name = "doc_mind_collection"
    
    def get_langchain_chroma(self):
        return Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embedding_model.embeddings,
            persist_directory=self.persist_dir
        )
    
    def add_documents(self, chunks_with_metadata: list):
        langchain_chroma = self.get_langchain_chroma()
        docs = [Document(page_content=chunk["text"], metadata=chunk["metadata"]) for chunk in chunks_with_metadata]
        langchain_chroma.add_documents(docs)
        # নতুন ভার্সনে auto-persist হয়, তাই আলাদা persist() দরকার নেই
        # langchain_chroma.persist()   # <-- এই লাইনটি ডিলিট বা কমেন্ট করুন
    
    def search(self, query: str, k: int = None):
        k = k or settings.TOP_K_RESULTS
        langchain_chroma = self.get_langchain_chroma()
        return langchain_chroma.similarity_search_with_score(query, k=k)
    
    def delete_collection(self):
        try:
            self.client.delete_collection(self.collection_name)
        except:
            pass