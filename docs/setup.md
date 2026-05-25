# সেটআপ নির্দেশনা

## প্রয়োজনীয় সফটওয়্যার
- Python 3.10+
- Ollama (https://ollama.com)

## প্রথমবার সেটআপ
1. প্রোজেক্ট ক্লোন করুন।
2. `python -m venv venv`
3. `source venv/bin/activate` (Windows: `venv\Scripts\activate`)
4. `pip install -r requirements.txt`
5. `ollama pull qwen2.5:7b`
6. `ollama serve` (আলাদা টার্মিনালে)
7. `streamlit run src/main.py`