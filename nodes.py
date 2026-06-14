import os
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph
from langchain_core.messages import SystemMessage
from typing import TypedDict
from dotenv import load_dotenv

# Works both locally (.env file) and on Streamlit Cloud (secrets injected automatically)
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found.\n"
        "Local: make sure a .env file exists with GROQ_API_KEY=your-key-here\n"
        "Streamlit Cloud: add it under App Settings → Secrets"
    )


class ChatState(TypedDict):
    history: list


llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0.7
)