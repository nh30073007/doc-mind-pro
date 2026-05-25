# src/agents/memory_manager.py
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from config import get_settings

settings = get_settings()
DB_PATH = settings.DATA_DIR / "metadata.db"

class MemoryManager:
    def __init__(self, session_id="default"):
        self.session_id = session_id
        self._init_db()
    
    def _init_db(self):
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH))
        conn.execute('''
            CREATE TABLE IF NOT EXISTS conversation_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                user_message TEXT,
                assistant_response TEXT,
                interest_json TEXT,
                timestamp DATETIME
            )
        ''')
        conn.commit()
        conn.close()
    
    def add_exchange(self, user_message, assistant_response, interest):
        conn = sqlite3.connect(str(DB_PATH))
        conn.execute(
            "INSERT INTO conversation_memory (session_id, user_message, assistant_response, interest_json, timestamp) VALUES (?,?,?,?,?)",
            (self.session_id, user_message, assistant_response, json.dumps(interest, ensure_ascii=False), datetime.now())
        )
        conn.commit()
        conn.close()
    
    def get_history(self, limit=5):
        conn = sqlite3.connect(str(DB_PATH))
        cur = conn.execute(
            "SELECT user_message, assistant_response FROM conversation_memory WHERE session_id = ? ORDER BY timestamp DESC LIMIT ?",
            (self.session_id, limit)
        )
        rows = cur.fetchall()
        conn.close()
        return [{"user": r[0], "assistant": r[1]} for r in rows][::-1]