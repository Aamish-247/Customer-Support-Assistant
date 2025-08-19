from langchain_google_genai import ChatGoogleGenerativeAI , GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os
import json
load_dotenv()

api_key = os.getenv("GOOGLE_GENAI_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_GENAI_API_KEY is not set in the environment variables.")

api = os.getenv("GROQ_API_KEY")

model = ChatGroq(
    model="llama3-8b-8192",
    api_key=api,
    temperature=0.2,
)

# model = ChatGoogleGenerativeAI(
#     model="gemini-1.5-flash",
#     api_key=api_key,
#     temperature=0.2,
# )

embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=api_key
)



def create_vector_store(file_path: str, vector_store_path: str = "faiss_index") -> FAISS:
    if os.path.exists(vector_store_path):
        vector_store = FAISS.load_local(
            vector_store_path,
            embedding_model,
            allow_dangerous_deserialization=True,
        )
        print(f"Vector store loaded from {vector_store_path}.")
        return vector_store

    loader = CSVLoader(file_path=file_path)
    documents = loader.load()
    print(f"Loaded {len(documents)} documents from CSV.")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 100)
    chunks = text_splitter.split_documents(documents)

    vector_store = FAISS.from_documents(chunks, embedding_model)
    vector_store.save_local(vector_store_path)
    print(f"Vector store saved to {vector_store_path}.")
    return vector_store

vector_store_instance = create_vector_store(file_path=r"D:\ChatBot\Fragrance Wholesale Sheet .csv", vector_store_path="faiss_index")

def search_relevant_documents(query: str, vector_store: FAISS, k: int = 5) -> list:
    results = vector_store.similarity_search(query, k=k)
    print(f"Found {len(results)} relevant documents.")
    return results

History_directory = "chat_history"
def get_history_file_path(user_id: str) -> str:
    if not os.path.exists(History_directory):
        os.makedirs(History_directory)
    return os.path.join(History_directory, f"{user_id}.json")

def load_chat_history(user_id: str) -> list:
    file_path = get_history_file_path(user_id)
    if os.path.exists(file_path):
        with open(file_path, 'r' , encoding="utf-8") as f:
            return json.load(f)
    return []

def save_chat_history(user_id: str, messages: list):
    file_path = get_history_file_path(user_id)
    with open(file_path, 'w', encoding="utf-8") as f:
        json.dump(messages, f)





parser = StrOutputParser()

def get_response(user_input: str, user_id: str) -> str:
    chat_history = load_chat_history(user_id)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Instead of manually adding messages, load chat history into memory
    memory.chat_memory.messages = [
        HumanMessage(content=msg["content"]) if msg["role"] == "user" else AIMessage(content=msg["content"])
        for msg in chat_history
    ]


    prompt = ChatPromptTemplate.from_messages(
       [
        (
            "system",
            """You are a helpful and polite customer support assistant for our store.
            Your name is Aamish and you behaviour will be like a human and if someone ask you about you then you will tell them you are customer support assistant and if you are not sure about the answer then tell customer you are not sure and you will connect them to human support.
            Speak as the company using 'we' and 'our'. Do not mention being an AI.
            Use ONLY the FAQs and the Product Data below with the chat history to answer.
            If the information is missing, say so briefly and offer to connect the user to human support.

            Guidelines:
            - Be clear, concise, and friendly.
            - If you don't know something, politely say so.
            - Suggest helpful alternatives where possible.
            - If the user requests escalation, provide them with human support contact details.

            Important: If the answer to the user's question is explicitly covered in the FAQs below, 
            always use that exact FAQ answer instead of general knowledge.

            If the user's question is not explicitly covered in the FAQs, use your general knowledge to assist the user.


            Frequently Asked Questions (FAQs):
            1. What is your return policy?
               - Our standard return policy allows returns within 30 days of purchase, provided the item is unused and in original condition.

            2. How long does shipping take?
               - Standard shipping usually takes 3 to 7 business days. Express options are also available.

            3. Do you offer international shipping?
               - Yes, we ship internationally. Delivery times may vary by region.

            4. How can I track my order?
               - Once your order is shipped, you'll receive a tracking link via email or SMS.

            5. How do I contact support directly?
               - You can reach our support team by email at support@example.com or call us at +123-456-7890.

            6. What payment methods do you accept?
               - We accept credit/debit cards, PayPal, and select digital wallets.

            Product Data:
            {context}
            """
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{user_input}")
    ]
    )

    chain_input = RunnablePassthrough.assign(
    chat_history=lambda _: memory.load_memory_variables({})["chat_history"],
    context=lambda x: "\n".join(
        [doc.page_content for doc in search_relevant_documents(x["user_input"], vector_store_instance, k=4)]
    ) or "No relevant product data found."
    )

    chain = chain_input | prompt | model | parser

    response = chain.invoke({
        "user_input": user_input,
    })

    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "AI", "content": response})

    save_chat_history(user_id, chat_history)

    return response



