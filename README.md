# Customer Support Chatbot

A FastAPI-based chatbot designed to act as a customer support agent. This application uses LangChain to provide conversational memory and retrieve information from a CSV file to answer user queries.

## Features

- **Conversational AI**: Powered by **LangChain** and a language model (Groq's **Llama 3** or Google's **Gemini 1.5**).
- **RAG (Retrieval-Augmented Generation)**: Uses a **FAISS** vector store to retrieve relevant product data from a CSV file.
- **Persistent Chat History**: Stores and loads chat history for each user in a dedicated directory (`chat_history/`) using JSON files, allowing for continuous conversations.
- **RESTful API**: Built with **FastAPI** to handle chat requests and serve a web interface.
- **User-Friendly Interface**: A simple web interface (`index.html`) for interacting with the chatbot.
- **CORS Support**: Configured to allow cross-origin requests.

<br>

***

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

<br>

***

## Prerequisites

- Python 3.8+
- A Google Generative AI API key
- A Groq API key (optional, if you switch to the `llama3-8b-8192` model)

## Installation

1.  **Clone the repository** (if applicable).
2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install fastapi "uvicorn[standard]" langchain langchain-google-genai langchain-groq python-dotenv faiss-cpu
    ```
    *Note: `faiss-cpu` is used for the vector store. If you have a GPU, you can use `faiss-gpu` for better performance.*

***

## Environment Setup

Create a `.env` file in your project's root directory and add your API keys:

```ini
GOOGLE_GENAI_API_KEY=your_google_api_key_here
GROQ_API_KEY=your_groq_api_key_here

## Usage
Prepare your data: Ensure you have a CSV file named Fragrance Wholesale Sheet .csv in the specified directory D:\ChatBot. The chatbot.py script will automatically create a FAISS vector store from this file.

Start the server:

Bash

uvicorn main:app --host 0.0.0.0 --port 8000
The application will load the CSV data, create the vector store if it doesn't exist, and start the server.

Access the application:

Web Interface: Open your browser and navigate to http://localhost:8000/chat_interface to use the chatbot.

API Documentation: You can view the interactive API documentation at http://localhost:8000/docs.
