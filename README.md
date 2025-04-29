# 🌐 CulturaSense - AI-Powered Cultural Sensitivity & Adaptation Agent

CulturaSense is an AI Agent system built with [AutoGen](https://github.com/microsoft/autogen), designed for businesses and teams to detect cultural risks and rewrite content for global adaptation.  

It supports context-aware review and rewriting based on region, platform, audience profile, and sensitive contributors.

---

## 💡 Key Features

- 🔍 **CriticAgent** – detects cultural sensitivity risks (e.g. race, religion, tone)
- ✍️ **RewriterAgent** – rewrites content into regionally appropriate formats
- 📦 Powered by **GPT-4o** via AutoGen Agents
- 🧠 Ready for RAG and multi-modal input (text, images, PDFs)
- 💬 Designed for marketing, customer support, product localization teams

---

## 🧪 How to Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/Ethan215/AI-Agent.git
```
### 2. requrements
```bash
pip install -r requirements.txt
```
### 3. Install AutoGen and OPENAI
'''
pip install "pyautogen[openai]" --user
'''
### 4. Run the AI Agent(Optional)
```bash
python main.py
```

### 5. FastAPI
```bash
pip install uvicorn --user  

python -m uvicorn main:app --reload 

# test in http://127.0.0.1:8000/docs
```
### 6. Frontend
```bash
pip install streamlit --user 

cd frontend

python -m streamlit run app.py

# test in http://localhost:8501
```

### InStall：
```bash
pip install -r requirements.txt

pip install markdown --user

pip install requests

```