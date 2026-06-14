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

def get_graph():
    def chatbot_node(state: ChatState):
        messages = state["history"]

        system_prompt = SystemMessage(
            content="You are Annova, a helpful AI assistant."
        )

        response = llm.invoke([system_prompt] + messages)

        return {"history": messages + [response]}

    graph = StateGraph(ChatState)

    graph.add_node("chatbot", chatbot_node)
    graph.set_entry_point("chatbot")
    graph.set_finish_point("chatbot")

    return graph.compile()


