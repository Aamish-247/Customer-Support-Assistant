
#  Customer Support Chatbot  
 A FastAPI-based chatbot designed to act as a customer support agent. This application uses LangChain to provide conversational memory and retrieve information from a CSV file to answer user queries.  

---

## Features  

✅ Conversational AI using LangChain & LLMs (Gemini / Llama3)  
✅ Retrieval-Augmented Generation (RAG) with FAISS  
✅ Persistent chat history per user  
✅ RESTful API with FastAPI  
✅ Simple and responsive web UI  
✅ CORS support for cross-origin requests  

## Architecture  

The system consists of a backend API and a simple web frontend. The backend handles the core logic, including natural language processing, vector search, and chat history management.

┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│  Web Interface  │───┐   │   FastAPI App   │────>  │    Chatbot      │
│  (HTML, CSS, JS)│   │   │ (main.py)       │       │    (chatbot.py) │
└─────────────────┘   │   │ • REST Endpoints│       │ • LangChain     │
                      ├───┤ • Session Mgmt  │──────>│ • FAISS Vector  │
                      │   └─────────────────┘       │    Store        │
┌─────────────────┐   │                             │ • Chat History  │
│  User's Browser │───┘                             │ • CSV Data      │
└─────────────────┘                                 └─────────────────┘

## Prerequisites  

- Python **3.8+**  
- **Google Generative AI API key**  
- (Optional) **Groq API key** for Llama3  


## Installation  

Clone the repository (if applicable).
Create a virtual environment:
Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:
Install requirements.txt

## Environment Setup
Create a .env file in the root directory:

GOOGLE_GENAI_API_KEY=your_google_api_key_here
GROQ_API_KEY=your_groq_api_key_here

## Data Preparation
Ensure your product dataset is available as:
D:\ChatBot\Fragrance Wholesale Sheet .csv
The chatbot will automatically create a FAISS vector store from this file.

## Usage

uvicorn main:app --host 0.0.0.0 --port 8000
🌐 Web Interface → http://localhost:8000/

📖 API Docs → http://localhost:8000/docs

## API Endpoints

ET /: Serves the home page (home.html).
GET /chat_interface: Serves the chatbot's web interface (index.html).
POST /chat: The main endpoint for sending user messages and receiving bot responses.


## Project Structure

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
