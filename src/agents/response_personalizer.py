# src/agents/response_personalizer.py
from src.llm.ollama_client import OllamaClient
from src.agents.interest_analyzer import InterestAnalyzer
from src.agents.memory_manager import MemoryManager

class ResponsePersonalizer:
    def __init__(self, session_id="default"):
        self.llm = OllamaClient()
        self.interest_analyzer = InterestAnalyzer()
        self.memory = MemoryManager(session_id)
    
    def generate_personalized_response(self, user_message: str, context_docs: str) -> str:
        interest = self.interest_analyzer.analyze(user_message)
        history = self.memory.get_history(3)
        history_text = "\n".join([f"প্রশ্ন: {h['user']}\nউত্তর: {h['assistant']}" for h in history])
        prompt = self._build_prompt(user_message, context_docs, interest, history_text)
        answer = self.llm.generate(prompt)
        self.memory.add_exchange(user_message, answer, interest)
        return answer
    
    def _build_prompt(self, query, context, interest, history):
        return f"""ইতিহাস:
{history}

ডকুমেন্ট:
{context}

পছন্দ: স্তর={interest['level']}, ভাষা={interest['language']}, শৈলী={interest['tone']}

প্রশ্ন: {query}

উত্তর:"""