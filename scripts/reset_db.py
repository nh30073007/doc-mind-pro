#!/usr/bin/env python
import shutil
from pathlib import Path
from config import get_settings

settings = get_settings()
chroma = settings.CHROMA_DB_DIR
meta_db = settings.DATA_DIR / "metadata.db"

print("⏹️ ডাটাবেজ রিসেট করা হচ্ছে...")
if chroma.exists():
    shutil.rmtree(chroma)
    chroma.mkdir()
if meta_db.exists():
    meta_db.unlink()
print("✅ সম্পন্ন। সব ভেক্টর ও মেটাডাটা মুছে গেছে।")