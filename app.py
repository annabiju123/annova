import streamlit as st
import streamlit.components.v1 as components
import json
import os
from langchain_core.messages import HumanMessage, AIMessage
from nodes import get_graph

import pypdf
import docx


# ==============================================================================
# PAGE CONFIG
# ==============================================================================

st.set_page_config(
    page_title="Annova",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==============================================================================
# BASE CSS
# ==============================================================================

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700;900&family=Raleway:wght@300;400;600&display=swap" rel="stylesheet">

<style>

/* ── BACKGROUND ── */
html, body { background: #03040f !important; }

.stApp, .main, section.main, section.main > div,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"],
[data-testid="stChatInputContainer"],
[data-testid="stMainBlockContainer"],
.block-container,
div.stChatFloatingInputContainer,
footer {
    background: transparent !important;
    background-color: transparent !important;
}

[data-testid="stBottom"] > div,
[data-testid="stBottom"] > div > div,
[data-testid="stBottomBlockContainer"] > div {
    background: transparent !important;
    background-color: transparent !important;
    box-shadow: none !important;
    border: none !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stDecoration"], #MainMenu, footer { display: none !important; }

/* ── SIDEBAR ALWAYS OPEN — NO TOGGLE ── */
[data-testid="stSidebar"] {
    display: block !important;
    visibility: visible !important;
    width: 270px !important;
    min-width: 270px !important;
    background: rgba(6, 6, 20, 0.95) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(255, 215, 0, 0.18) !important;
}

[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

/* ── SIDEBAR CONTENT ── */
[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
    padding: 1.5rem 1.2rem !important;
    width: 100% !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div {
    color: #e0d8f8 !important;
    font-family: 'Raleway', sans-serif !important;
}

.sidebar-title {
    font-family: 'Cinzel Decorative', serif;
    font-size: 17px;
    font-weight: 700;
    color: #ffd700 !important;
    text-align: center;
    letter-spacing: 3px;
    text-shadow: 0 0 14px rgba(255,215,0,0.45);
    margin-bottom: 18px;
    padding-bottom: 14px;
    border-bottom: 1px solid rgba(255,215,0,0.18);
}

.sidebar-section {
    font-family: 'Raleway', sans-serif;
    font-size: 10px;
    letter-spacing: 2.5px;
    color: rgba(180,160,220,0.50) !important;
    text-transform: uppercase;
    margin: 16px 0 8px 2px;
}

/* ── SIDEBAR BUTTONS ── */
[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    color: #e0d8f8 !important;
    border-radius: 12px !important;
    font-family: 'Raleway', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    padding: 0.55rem 1rem !important;
    margin-bottom: 8px !important;
    text-align: left !important;
    transition: all 0.2s ease !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,215,0,0.12) !important;
    border-color: rgba(255,215,0,0.42) !important;
    color: #ffd700 !important;
    transform: translateX(4px) !important;
}

/* ── FILE UPLOADER ── */
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1.5px dashed rgba(255,215,0,0.28) !important;
    border-radius: 12px !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] * {
    color: #c8c0e0 !important;
    font-size: 12px !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button {
    background: rgba(255,215,0,0.10) !important;
    border: 1px solid rgba(255,215,0,0.30) !important;
    color: #ffd700 !important;
    border-radius: 8px !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] svg {
    fill: rgba(255,215,0,0.55) !important;
}

[data-testid="stFileUploaderFile"] {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 8px !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    margin-top: 6px !important;
}

[data-testid="stFileUploaderFile"] * { color: #e0d8f8 !important; }

/* ── BRAND ── */
.brand {
    text-align: center;
    font-family: 'Cinzel Decorative', serif;
    font-size: 54px;
    font-weight: 900;
    letter-spacing: 10px;
    background: linear-gradient(90deg, #ffe066, #ffd700, #fff8dc, #ffd700, #ffe066);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 3s linear infinite;
    filter: drop-shadow(0 0 18px rgba(255,215,0,0.5));
    margin-bottom: 4px;
}

@keyframes shimmer {
    0%   { background-position: 0% center; }
    100% { background-position: 200% center; }
}

.brand-sub {
    text-align: center;
    font-family: 'Raleway', sans-serif;
    font-size: 12px;
    letter-spacing: 4px;
    color: rgba(180,160,220,0.55);
    margin-bottom: 24px;
}

/* ── CHAT BUBBLES ── */
div[data-testid="stChatMessage"] {
    background: rgba(10,10,25,.58) !important;
    backdrop-filter: blur(16px);
    border-radius: 18px !important;
    border: 1px solid rgba(255,255,255,.08) !important;
    margin-bottom: 10px !important;
}

div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: rgba(80,30,150,0.28) !important;
    border-color: rgba(180,130,255,0.22) !important;
}

div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] span,
div[data-testid="stChatMessage"] li,
div[data-testid="stChatMessage"] div {
    color: #e8e8f0 !important;
    font-family: 'Raleway', sans-serif !important;
    font-size: 15px !important;
    line-height: 1.7 !important;
}

/* ── CHAT INPUT ── */
[data-testid="stChatInput"],
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] * { background: transparent !important; }

[data-testid="stChatInput"] {
    border: 1.5px solid rgba(255,215,0,0.35) !important;
    border-radius: 28px !important;
    background: rgba(8,8,24,0.75) !important;
    backdrop-filter: blur(16px) !important;
}

[data-testid="stChatInput"] textarea {
    color: #f0f0f5 !important;
    font-family: 'Raleway', sans-serif !important;
    font-size: 15px !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: rgba(255,215,0,0.38) !important;
}

[data-testid="stChatInput"] button { background: transparent !important; }
[data-testid="stChatInput"] button svg { fill: #ffd700 !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(255,215,0,0.18);
    border-radius: 4px;
}

</style>
""", unsafe_allow_html=True)


# ==============================================================================
# NIGHT SKY CANVAS BACKGROUND
# ==============================================================================

components.html("""
<script>
const canvas = document.createElement("canvas");
document.body.appendChild(canvas);

canvas.style.position = "fixed";
canvas.style.top = "0";
canvas.style.left = "0";
canvas.style.width = "100vw";
canvas.style.height = "100vh";
canvas.style.zIndex = "0";
canvas.style.pointerEvents = "none";

const ctx = canvas.getContext("2d");

function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener("resize", resize);
resize();

let stars = Array.from({length: 150}, () => ({
    x: Math.random() * window.innerWidth,
    y: Math.random() * window.innerHeight,
    r: Math.random() * 1.5,
    dx: (Math.random() - 0.5) * 0.2,
    dy: (Math.random() - 0.5) * 0.2,
    alpha: Math.random()
}));

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#03040f";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    for (let s of stars) {
        s.x += s.dx;
        s.y += s.dy;

        if (s.x < 0 || s.x > canvas.width) s.dx *= -1;
        if (s.y < 0 || s.y > canvas.height) s.dy *= -1;

        s.alpha += (Math.random() - 0.5) * 0.05;
        if (s.alpha < 0.2) s.alpha = 0.2;
        if (s.alpha > 1) s.alpha = 1;

        ctx.beginPath();
        ctx.globalAlpha = s.alpha;
        ctx.fillStyle = "white";
        ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
        ctx.fill();
    }

    ctx.globalAlpha = 1;
    requestAnimationFrame(animate);
}

animate();
</script>
""", height=0)


# ==============================================================================
# MEMORY
# ==============================================================================

MEMORY_FILE = "chat_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
        return [
            HumanMessage(content=m["content"]) if m["type"] == "human"
            else AIMessage(content=m["content"])
            for m in data
        ]
    return []

def save_memory(history):
    with open(MEMORY_FILE, "w") as f:
        json.dump([{
            "type": "human" if isinstance(m, HumanMessage) else "ai",
            "content": m.content
        } for m in history], f)

def delete_memory():
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)


# ==============================================================================
# FILE TEXT EXTRACTION
# ==============================================================================

def extract_text_from_file(uploaded_file):
    name = uploaded_file.name
    ext  = name.split(".")[-1].lower()
    try:
        if ext == "pdf":
            reader = pypdf.PdfReader(uploaded_file)
            return "\n".join(p.extract_text() or "" for p in reader.pages).strip()
        elif ext == "docx":
            document = docx.Document(uploaded_file)
            return "\n".join(p.text for p in document.paragraphs).strip()
        elif ext in ("txt", "md", "csv"):
            return uploaded_file.getvalue().decode("utf-8", errors="ignore").strip()
        elif ext in ("png", "jpg", "jpeg", "gif", "webp"):
            return f"[Image attached: {name}]"
        else:
            return f"[Unsupported file type: {name}]"
    except Exception as e:
        return f"[Could not read {name}: {e}]"


# ==============================================================================
# FOUNDER DETECTION
# ==============================================================================

FOUNDER_TRIGGERS = [
    "who made you", "who built you", "who created you", "who is your creator",
    "who made annova", "who built annova", "who created annova",
    "who is the founder", "who is your founder", "who is your developer",
    "who is your maker", "who developed you", "who designed you",
    "who is behind you", "who is behind annova", "your creator",
    "your founder", "your maker", "your developer", "who are you made by",
]

def is_founder_question(text: str) -> bool:
    t = text.lower().strip()
    return any(trigger in t for trigger in FOUNDER_TRIGGERS)


# ==============================================================================
# SESSION STATE
# ==============================================================================

if "history" not in st.session_state:
    st.session_state.history = load_memory()

if "graph" not in st.session_state:
    st.session_state.graph = get_graph()


# ==============================================================================
# SIDEBAR
# ==============================================================================

with st.sidebar:

    st.markdown("<div class='sidebar-title'>✦ ANNOVA</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-section'>Actions</div>", unsafe_allow_html=True)

    if st.button("✦  New Chat", use_container_width=True):
        st.session_state.history = []
        save_memory(st.session_state.history)
        st.rerun()

    if st.button("🗑  Delete Memory", use_container_width=True):
        st.session_state.history = []
        delete_memory()
        st.rerun()

    st.markdown("<div class='sidebar-section'>Attach Files</div>", unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Upload a file",
        type=["pdf", "docx", "txt", "md", "csv", "png", "jpg", "jpeg", "gif", "webp"],
        accept_multiple_files=True
    )

    if uploaded_files:
        st.markdown(
            f"<p style='color:rgba(255,215,0,0.7);font-size:12px;margin-top:6px'>"
            f"📎 {len(uploaded_files)} file(s) attached</p>",
            unsafe_allow_html=True
        )

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:rgba(180,160,220,0.28);font-size:10px;"
        "text-align:center;letter-spacing:2px;'>born from stars · built by Anna</p>",
        unsafe_allow_html=True
    )


# ==============================================================================
# MAIN CONTENT
# ==============================================================================

st.markdown("""
<div class='brand'>✦ ANNOVA</div>
<div class='brand-sub'>born from stars · built by Anna</div>
""", unsafe_allow_html=True)

for msg in st.session_state.history:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

prompt = st.chat_input("Ask Annova anything… ✨")

if prompt:

    if is_founder_question(prompt):
        reply = "✨ I am **Annova**, created by **Anna Biju** — born from stars, built with love 🌟"
        st.session_state.history.append(HumanMessage(content=prompt))
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.history.append(AIMessage(content=reply))
        with st.chat_message("assistant"):
            st.markdown(reply)
        save_memory(st.session_state.history)
        st.rerun()

    else:
        full_prompt = prompt
        if uploaded_files:
            attachments = []
            for uf in uploaded_files:
                extracted = extract_text_from_file(uf)
                attachments.append(f"\n\n--- Attached file: {uf.name} ---\n{extracted}")
            full_prompt = prompt + "".join(attachments)

        st.session_state.history.append(HumanMessage(content=full_prompt))
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("✨ Thinking…"):
                result = st.session_state.graph.invoke({
                    "history": st.session_state.history
                })
                reply = result["history"][-1].content
            st.markdown(reply)

        st.session_state.history.append(AIMessage(content=reply))
        save_memory(st.session_state.history)
        st.rerun()
