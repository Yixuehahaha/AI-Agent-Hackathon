# 🌐 CulturaSense — AI-Powered Cultural Sensitivity & Content Adaptation Agent

**CulturaSense** is a multi-agent AI system designed to detect cultural risks and rewrite marketing content for global audiences. Built with [Microsoft AutoGen](https://github.com/microsoft/autogen), FastAPI, and Streamlit, it enables marketing and localization teams to create culturally appropriate, emotionally resonant content — across regions, languages, and platforms.

> 🎯 Perfect for use in e-commerce, social media, customer support, and international product marketing.

---

## ✨ Key Features

- **CriticAgent** – Audits copy, image, and tone for cultural, religious, and political sensitivity risks  
- **RewriterAgent** – Rewrites content for cultural adaptation, emotional fit, and platform alignment  
- **Azure AI Vision Integration** – Automatically extracts image descriptions and feeds them into the critique pipeline  
- **image input support** – Enables multi-modal critique beyond plain text  
- Context-aware input based on country, platform, age, gender, religion, etc.  
- Powered by **GPT-4o**, designed for future RAG and multi-agent workflows  

---

## 🧪 How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Yixuehahaha/AI-Agent-Hackathon.git
cd AI-Agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file

```env
OPENAI_API_KEY=your_openai_key
AZURE_VISION_ENDPOINT=https://your_endpoint.cognitiveservices.azure.com
AZURE_VISION_KEY=your_azure_key
```

### 4. Run Agents Directly (for CLI testing)

```bash
python main.py
```

### 5. Launch Backend API (FastAPI)

```bash
python -m uvicorn main:app --reload
# Access docs at http://127.0.0.1:8000/docs
```

### 6. Launch Web Frontend (Streamlit)

```bash
cd frontend
streamlit run app.py
# Open http://localhost:8501
```

---

## 📷 Example Flow

1. Upload **text** and/or **image**
2. Set target **region, platform, language, gender, religion, etc.**
3. The system:
   - Uses Azure Vision to analyze the image
   - Sends content to CriticAgent → RewriterAgent
   - Returns cultural critique + improved content + CTR/risk estimate
4. See results in a structured, beautiful frontend UI

---

## 🙌 Acknowledgements

- Built with ❤️ for the [Microsoft AI Agent Hackathon](https://github.com/microsoft/autogen)
- Inspired by real-world challenges in **global marketing**, **cross-cultural communication**, and **AI adaptation**
