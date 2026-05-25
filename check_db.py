# check_db.py
from src.core.vector_store import VectorStore

vs = VectorStore()
try:
    collection = vs.client.get_collection("doc_mind_collection")
    total_chunks = len(collection.get()['ids'])
    print(f"✅ ডাটাবেজে মোট চাঙ্কের সংখ্যা: {total_chunks}")
    
    if total_chunks > 0:
        # একটি নমুনা সার্চ
        results = vs.search("test", k=1)
        if results:
            print("✅ সার্চ কাজ করছে। নমুনা ফলাফল:")
            print(results[0][0].page_content[:200])
        else:
            print("⚠️ সার্চ কোনো ফলাফল দেয়নি।")
    else:
        print("❌ ডাটাবেজ খালি। দয়া করে একটি PDF আপলোড ও প্রসেস করুন।")
except Exception as e:
    print(f"❌ এরর: {e}")