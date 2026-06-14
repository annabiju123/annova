# 🤖 My Personal AI Chatbot

A conversational AI chatbot built with LangChain, LangGraph, and Streamlit —
powered by Meta's LLaMA 3 model via Groq (free & fast).

## 🚀 Features
- 🧠 Conversation memory — remembers full chat history
- ⚡ LangGraph state machine for robust conversation flow
- 🖥️ Clean Streamlit web UI
- 🆓 100% free — uses Groq API (no credit card needed)
- 🔄 Modular — easily swap LLM in one line

## 🛠️ Tech Stack
| Tool | Purpose |
|------|---------|
| Streamlit | Web UI |
| LangChain | LLM orchestration |
| LangGraph | Conversation state graph |
| Groq + LLaMA 3 | Free, fast language model |

## ⚙️ Run locally

### 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/my-personal-chatbot
cd my-personal-chatbot

### 2. Install dependencies
pip install -r requirements.txt

### 3. Add your Groq API key
Create a .env file:
GROQ_API_KEY=your-groq-api-key-here
Get a free key at: https://console.groq.com

### 4. Run the app
streamlit run app.py

## 🏗️ Architecture
User → Streamlit UI → LangGraph State Machine → LLaMA 3 (via Groq) → Response
Deployment refresh