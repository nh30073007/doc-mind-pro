# src/agents/interest_analyzer.py
class InterestAnalyzer:
    @staticmethod
    def analyze(user_message: str) -> dict:
        interest = {"level": "মাঝারি", "language": "বাংলা", "tone": "বন্ধুত্বপূর্ণ"}
        msg = user_message.lower()
        
        if any(w in msg for w in ["সহজ", "বেসিক", "শুরু", "beginner"]):
            interest["level"] = "বিগিনার"
        elif any(w in msg for w in ["এডভান্সড", "গভীর", "ডিটেইল", "প্রো", "advanced"]):
            interest["level"] = "এডভান্সড"
        
        if any(w in msg for w in ["ইংরেজি", "english"]):
            interest["language"] = "ইংরেজি"
        elif any(w in msg for w in ["বাংলা", "bangla"]):
            interest["language"] = "বাংলা"
        
        if any(w in msg for w in ["ফরমাল", "সিরিয়াস"]):
            interest["tone"] = "আনুষ্ঠানিক"
        elif any(w in msg for w in ["মজার", "হালকা", "ইনফরমাল"]):
            interest["tone"] = "হালকা"
        
        return interest