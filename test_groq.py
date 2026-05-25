# test_groq.py
import os
from dotenv import load_dotenv
from groq import Groq

# .env ফাইল থেকে API কী লোড করুন
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ .env ফাইলে GROQ_API_KEY সেট করা হয়নি।")
    exit()

try:
    # ক্লায়েন্ট তৈরি করুন
    client = Groq(api_key=api_key)
    
    # একটি ছোট প্রম্পট পাঠান
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": "Say 'API connection successful' in one sentence."}
        ],
        model="llama-3.1-8b-instant",
        max_tokens=50,
        temperature=0.2,
    )
    
    print("✅ Groq API উত্তর:", response.choices[0].message.content)
    print("🎉 API সঠিকভাবে কাজ করছে!")

except Exception as e:
    print("❌ API কল ব্যর্থ:", e)