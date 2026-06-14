import os
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph
from langchain_core.messages import SystemMessage
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found.\n"
        "Local: .env file needed\n"
        "Streamlit Cloud: add in Secrets"
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

        response = llm.invoke([
            SystemMessage(content="You are Annova, a helpful AI assistant."),
            *messages
        ])

        return {"history": messages + [response]}

    graph = StateGraph(ChatState)

    graph.add_node("chatbot", chatbot_node)
    graph.set_entry_point("chatbot")
    graph.set_finish_point("chatbot")

    return graph.compile()