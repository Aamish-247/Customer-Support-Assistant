<<<<<<< HEAD
# 🛎️ Customer Support Chatbot  

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)  
[![LangChain](https://img.shields.io/badge/LangChain-00B140?style=for-the-badge&logo=chainlink&logoColor=white)](https://www.langchain.com/)  
[![FAISS](https://img.shields.io/badge/FAISS-FF6F00?style=for-the-badge&logo=vectorworks&logoColor=white)](https://github.com/facebookresearch/faiss)  
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)  

A **FastAPI-based AI-powered chatbot** designed to act as a **customer support agent**.  
It leverages **LangChain**, **FAISS vector search**, and **LLMs (Llama 3 / Gemini 1.5)** to answer queries from a **CSV product dataset**.  

---

## ✨ Features  

✅ Conversational AI using LangChain & LLMs (Gemini / Llama3)  
✅ Retrieval-Augmented Generation (RAG) with FAISS  
✅ Persistent chat history per user  
✅ RESTful API with FastAPI  
✅ Simple and responsive web UI  
✅ CORS support for cross-origin requests  

---

## 🏗️ Architecture  

The chatbot consists of a **FastAPI backend** and a **minimal web frontend**.  

┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Web Interface   │───┐ │ FastAPI App │────> │ Chatbot │
│ (HTML, CSS, JS) │ │ (main.py) │ │ (chatbot.py) │
└─────────────────┘ │ │ • REST Endpoints│ │ • LangChain │
├┤ • Session Mgmt ───>│ • FAISS Vector │
│ └─────────────────┘ │ Store │
┌─────────────────┐ │ │ • Chat History │
│ User's Browser  │───┘ • CSV Data     │
└─────────────────┘ └─────────────────┘

yaml
Copy
Edit

---

## 📋 Prerequisites  

- Python **3.8+**  
- **Google Generative AI API key**  
- (Optional) **Groq API key** for Llama3  

---

## ⚙️ Installation  

```bash
# Clone repository
git clone https://github.com/your-username/customer-support-chatbot.git
cd customer-support-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi "uvicorn[standard]" langchain langchain-google-genai langchain-groq python-dotenv faiss-cpu
⚡ Tip: Use faiss-gpu if you have a GPU.

🔑 Environment Setup
Create a .env file in the root directory:

ini
Copy
Edit
GOOGLE_GENAI_API_KEY=your_google_api_key_here
GROQ_API_KEY=your_groq_api_key_here
📂 Data Preparation
Ensure your product dataset is available as:

makefile
Copy
Edit
D:\ChatBot\Fragrance Wholesale Sheet .csv
The chatbot will automatically create a FAISS vector store from this file.

🚀 Usage
bash
Copy
Edit
uvicorn main:app --host 0.0.0.0 --port 8000
🌐 Web Interface → http://localhost:8000/chat_interface

📖 API Docs → http://localhost:8000/docs

📡 API Endpoints
POST /chat
Request Body:

json
Copy
Edit
{
  "user_input": "string",
  "user_id": "string or null"
}
Response Body:

json
Copy
Edit
{
  "response": "string",
  "user_id": "string"
}
If user_id is not provided, a new one will be generated.

📂 Project Structure
bash
Copy
Edit
├── .env                         # Environment variables
├── main.py                      # FastAPI application
├── chatbot.py                   # Core chatbot logic (LangChain, FAISS)
├── faiss_index/                 # FAISS vector store
│   ├── index.faiss
│   └── index.json
├── chat_history/                # User chat history
│   └── <user_id>.json
├── static/
│   ├── style.css                # Frontend CSS
│   ├── script.js                # Frontend JS
│   ├── index.html               # Chatbot UI
│   └── home.html                # Home page
└── Fragrance Wholesale Sheet .csv  # Product dataset└── Fragrance Wholesale Sheet .csv  # Product dataset
=======