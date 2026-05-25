# src/core/chunker.py
from config import get_settings

settings = get_settings()

class TextChunker:
    def __init__(self, chunk_size=None, chunk_overlap=None):
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP
        
    def split_text(self, text: str, metadata: dict = None) -> list:
        """Recursive character text splitter without any external dependency"""
        chunks = []
        start = 0
        text_length = len(text)
        
        if text_length <= self.chunk_size:
            # পুরো টেক্সট একটাই চাঙ্ক
            meta = (metadata or {}).copy()
            meta["chunk_index"] = 0
            meta["chunk_total"] = 1
            return [{"text": text, "metadata": meta}]
        
        # সেমিকোলন বা প্যারাগ্রাফের ভিত্তিতে ব্রেক পয়েন্ট খুঁজে বের করা
        separators = ["\n\n", "\n", ". ", "? ", "! ", ", ", " ", ""]
        
        while start < text_length:
            end = start + self.chunk_size
            
            if end >= text_length:
                # শেষ চাঙ্ক
                chunk = text[start:]
                chunks.append(chunk)
                break
            
            # চাঙ্কের শেষে ব্রেক পয়েন্ট খুঁজে বের করা (overlap এর জন্য)
            for sep in separators:
                # start+chunk_size এর আশেপাশে শেষ সেপারেটর খুঁজি
                last_sep = text.rfind(sep, start, end + 50)
                if last_sep != -1 and last_sep > start:
                    end = last_sep + len(sep)
                    break
            
            chunk = text[start:end]
            chunks.append(chunk)
            # overlap যোগ করে নতুন স্টার্ট
            start = end - self.chunk_overlap
        
        # মেটাডাটা যোগ করা
        result = []
        for i, chunk in enumerate(chunks):
            meta = (metadata or {}).copy()
            meta["chunk_index"] = i
            meta["chunk_total"] = len(chunks)
            result.append({"text": chunk, "metadata": meta})
        
        return result