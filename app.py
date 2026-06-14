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

/* ── Brand title ── */
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

/* ── Kill ALL white backgrounds ── */
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

/* ── Make header transparent but keep all its controls intact ── */
[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stDecoration"],
#MainMenu, footer { display: none !important; }

/* ── STRICT Sidebar Toggle ONLY ── */
[data-testid="collapsedControl"] {
    z-index: 9999 !important;
}

[data-testid="collapsedControl"] button {
    background: rgba(255, 215, 0, 0.45) !important;
    border: 2px solid #ffd700 !important;

    width: 56px !important;
    height: 56px !important;

    border-radius: 0 14px 14px 0 !important;

    box-shadow: 0 0 25px rgba(255, 215, 0, 0.7) !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* ONLY icon inside sidebar toggle */
[data-testid="collapsedControl"] button svg {
    fill: #ffd700 !important;
}
/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: rgba(6, 6, 20, 0.95) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(255, 215, 0, 0.18) !important;
    display: flex !important;
    visibility: visible !important;
    min-width: 270px !important;
}

[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
    padding: 1.5rem 1.2rem !important;
    width: 100% !important;
}

/* Sidebar title */
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

/* Sidebar section labels */
.sidebar-section {
    font-family: 'Raleway', sans-serif;
    font-size: 10px;
    letter-spacing: 2.5px;
    color: rgba(180,160,220,0.50) !important;
    text-transform: uppercase;
    margin: 16px 0 8px 2px;
}

/* All text in sidebar */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div {
    color: #e0d8f8 !important;
    font-family: 'Raleway', sans-serif !important;
}

/* ── Sidebar BUTTONS ── */
[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    color: #D4AF37 !important;
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

/* Ensure button text/emoji content is visible */
[data-testid="stSidebar"] .stButton > button,
[data-testid="stSidebar"] .stButton > button p,
[data-testid="stSidebar"] .stButton > button span,
[data-testid="stSidebar"] .stButton > button div {
    color: #e0d8f8 !important;
    opacity: 1 !important;
    visibility: visible !important;
}

[data-testid="stSidebar"] .stButton > button:hover,
[data-testid="stSidebar"] .stButton > button:hover p,
[data-testid="stSidebar"] .stButton > button:hover span,
[data-testid="stSidebar"] .stButton > button:hover div {
    color: #ffd700 !important;
}

[data-testid="stSidebar"] .stButton > button svg {
    fill: currentColor !important;
    opacity: 1 !important;
    visibility: visible !important;
}

/* ── FILE UPLOADER in sidebar ── */
[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: transparent !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1.5px dashed rgba(255,215,0,0.28) !important;
    border-radius: 12px !important;
    transition: border-color 0.2s !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"]:hover {
    border-color: rgba(255,215,0,0.55) !important;
    background: rgba(255,215,0,0.03) !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] *,
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] p,
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] span,
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] small,
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] div {
    color: #c8c0e0 !important;
    font-size: 12px !important;
    opacity: 1 !important;
    visibility: visible !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button {
    background: rgba(255,215,0,0.10) !important;
    border: 1px solid rgba(255,215,0,0.30) !important;
    color: #ffd700 !important;
    border-radius: 8px !important;
    font-size: 12px !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button p,
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button span {
    color: #ffd700 !important;
}

/* Cloud / upload icon svg */
[data-testid="stFileUploaderDropzoneInstructions"] svg,
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] svg {
    fill: rgba(255,215,0,0.55) !important;
    stroke: rgba(255,215,0,0.55) !important;
    opacity: 1 !important;
    visibility: visible !important;
}

[data-testid="stFileUploaderFile"] {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 8px !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    margin-top: 6px !important;
}

[data-testid="stFileUploaderFile"] *,
[data-testid="stFileUploaderFile"] p,
[data-testid="stFileUploaderFile"] span {
    color: #e0d8f8 !important;
    opacity: 1 !important;
    visibility: visible !important;
}

[data-testid="stFileUploaderFile"] svg {
    fill: #e0d8f8 !important;
    opacity: 1 !important;
    visibility: visible !important;
}

/* Delete/cross icon on uploaded file chip */
[data-testid="stFileUploaderFile"] button svg,
[data-testid="baseButton-secondary"] svg {
    fill: #ffd700 !important;
    opacity: 1 !important;
    visibility: visible !important;
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
[data-testid="stChatInput"] button svg {
    fill: #ffd700 !important;
    opacity: 1 !important;
    visibility: visible !important;
}

/* ── Scrollbar ── */
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
(function () {
  let topDoc, topWin;
  try {
    topWin = window.parent.parent;
    topDoc = topWin.document;
    topDoc.body;
  } catch (e) {
    try {
      topWin = window.parent;
      topDoc = topWin.document;
      topDoc.body;
    } catch (e2) {
      topWin = window;
      topDoc = document;
    }
  }

  const old = topDoc.getElementById('annova-space-bg');
  if (old) old.remove();
  const oldStyle = topDoc.getElementById('annova-space-style');
  if (oldStyle) oldStyle.remove();

  const style = topDoc.createElement('style');
  style.id = 'annova-space-style';
  style.textContent = `
    html, body { background: #03040f !important; }
    .stApp, .main,
    [data-testid="stAppViewContainer"],
    [data-testid="stBottom"],
    [data-testid="stBottomBlockContainer"],
    [data-testid="stChatInputContainer"],
    div.stChatFloatingInputContainer {
      background: transparent !important;
    }
    [data-testid="stBottom"] > div,
    [data-testid="stBottom"] > div > div,
    [data-testid="stBottomBlockContainer"] > div,
    [data-testid="stChatInputContainer"] > div {
      background: transparent !important;
      background-color: transparent !important;
      box-shadow: none !important;
    }
    .stApp { position: relative !important; z-index: 2 !important; }
    [data-testid="stAppViewContainer"],
    [data-testid="stSidebar"] { position: relative !important; z-index: 2 !important; }

    /* SIDEBAR always visible */
    [data-testid="stSidebar"] {
      display: flex !important;
      visibility: visible !important;
      background: rgba(6,6,20,0.95) !important;
      border-right: 1px solid rgba(255,215,0,0.18) !important;
      min-width: 270px !important;
    }

    /* SIDEBAR TOGGLE always visible */
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] {
      display: flex !important;
      visibility: visible !important;
      opacity: 1 !important;
      z-index: 999 !important;
    }

    #annova-space-bg {
      position: fixed !important;
      top: 0 !important; left: 0 !important;
      z-index: 0 !important;
      pointer-events: none !important;
    }
    [data-testid="stHeader"] {
      background: transparent !important;
    }

    div[data-testid="stChatMessage"] {
      background: rgba(10,10,25,.58) !important;
      backdrop-filter: blur(16px);
      border-radius: 18px !important;
      border: 1px solid rgba(255,255,255,.08) !important;
    }
    div[data-testid="stChatMessage"] p,
    div[data-testid="stChatMessage"] span,
    div[data-testid="stChatMessage"] div { color: #e8e8f0 !important; }
    [data-testid="stChatInput"] {
      border: 1.5px solid rgba(255,215,0,0.35) !important;
      border-radius: 28px !important;
      background: rgba(8,8,24,0.75) !important;
    }
    [data-testid="stChatInput"] textarea { color: #f0f0f5 !important; }
    [data-testid="stChatInput"] textarea::placeholder { color: rgba(255,215,0,0.38) !important; }
    [data-testid="stChatInput"] button svg {
      fill: #ffd700 !important;
      opacity: 1 !important;
      visibility: visible !important;
    }

    /* Sidebar button + uploader icons always visible */
    [data-testid="stSidebar"] .stButton > button svg {
      fill: currentColor !important;
      opacity: 1 !important;
      visibility: visible !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] svg,
    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] svg,
    [data-testid="stFileUploaderFile"] svg {
      opacity: 1 !important;
      visibility: visible !important;
    }
  `;
  topDoc.head.appendChild(style);

  const canvas = topDoc.createElement('canvas');
  canvas.id = 'annova-space-bg';
  topDoc.body.prepend(canvas);
  const ctx = canvas.getContext('2d');

  function resize() {
    const w = topWin.innerWidth, h = topWin.innerHeight;
    canvas.width = w; canvas.height = h;
    canvas.style.width = w + 'px'; canvas.style.height = h + 'px';
  }
  resize();
  topWin.addEventListener('resize', resize);

  const W = () => canvas.width;
  const H = () => canvas.height;
  const rand = (a, b) => a + Math.random() * (b - a);
  let t = 0;

  const blobs = [240, 220, 260].map(hue => ({
    rx: rand(0.05, 0.95), ry: rand(0.05, 0.95),
    r: rand(180, 420), hue, phase: rand(0, Math.PI * 2),
  }));

  function drawSky() {
    const g = ctx.createLinearGradient(0, 0, 0, H());
    g.addColorStop(0, '#03040f'); g.addColorStop(0.5, '#070b1f'); g.addColorStop(1, '#0a0e2a');
    ctx.fillStyle = g; ctx.fillRect(0, 0, W(), H());
  }

  function drawBlobs() {
    ctx.save();
    ctx.globalCompositeOperation = 'lighter';
    blobs.forEach(b => {
      const cx = (b.rx + Math.sin(t * 0.3 + b.phase) * 0.05) * W();
      const cy = (b.ry + Math.cos(t * 0.25 + b.phase) * 0.05) * H();
      const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, b.r);
      g.addColorStop(0, `hsla(${b.hue},60%,35%,0.08)`);
      g.addColorStop(0.5, `hsla(${b.hue},60%,30%,0.04)`);
      g.addColorStop(1, `hsla(${b.hue},60%,30%,0)`);
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(cx, cy, b.r, 0, Math.PI * 2); ctx.fill();
    });
    ctx.restore();
  }

  function makeStar() {
    return {
      baseX: rand(0, W()), baseY: rand(0, H()), x: 0, y: 0,
      size: rand(0.6, 2.6), opacity: rand(0.1, 0.9),
      twinkleSpeed: rand(0.005, 0.025), twinkleDir: Math.random() > 0.5 ? 1 : -1,
      angle: rand(0, Math.PI * 2), angleSpeed: rand(0.002, 0.006),
      gold: Math.random() > 0.65, cross: Math.random() > 0.75,
    };
  }

  const stars = Array.from({ length: 220 }, makeStar);

  function drawCircleStar(s) {
    const color = s.gold ? '#ffd700' : '#ffffff';
    const rgb = s.gold ? '255,215,0' : '255,255,255';
    ctx.save();
    ctx.globalAlpha = s.opacity * 0.3;
    const g = ctx.createRadialGradient(s.x, s.y, 0, s.x, s.y, s.size * 5);
    g.addColorStop(0, `rgba(${rgb},1)`); g.addColorStop(1, `rgba(${rgb},0)`);
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(s.x, s.y, s.size * 5, 0, Math.PI * 2); ctx.fill();
    ctx.globalAlpha = s.opacity; ctx.fillStyle = color;
    ctx.shadowColor = color; ctx.shadowBlur = s.size * 4;
    ctx.beginPath(); ctx.arc(s.x, s.y, s.size, 0, Math.PI * 2); ctx.fill();
    ctx.restore();
  }

  function drawCrossStar(s) {
    const color = s.gold ? '#ffd700' : '#ffffff'; const r = s.size;
    ctx.save();
    ctx.globalAlpha = s.opacity; ctx.fillStyle = color;
    ctx.shadowColor = color; ctx.shadowBlur = r * 5;
    ctx.beginPath(); ctx.arc(s.x, s.y, r * 0.65, 0, Math.PI * 2); ctx.fill();
    ctx.fillRect(s.x - r*3.2, s.y - r*0.28, r*6.4, r*0.56);
    ctx.fillRect(s.x - r*0.28, s.y - r*3.2, r*0.56, r*6.4);
    ctx.restore();
  }

  function animate() {
    if (!topDoc.body.contains(canvas)) return;
    t += 0.01; drawSky(); drawBlobs();
    stars.forEach(s => {
      s.angle += s.angleSpeed;
      s.x = s.baseX + Math.sin(s.angle) * 10;
      s.y = s.baseY + Math.cos(s.angle) * 10;
      s.opacity += s.twinkleSpeed * s.twinkleDir;
      if (s.opacity >= 0.95) { s.opacity = 0.95; s.twinkleDir = -1; }
      if (s.opacity <= 0.08) { s.opacity = 0.08; s.twinkleDir = 1; }
      if (s.cross) drawCrossStar(s); else drawCircleStar(s);
    });
    topWin.requestAnimationFrame(animate);
  }
  animate();
})();
</script>
""", height=0, width=0)


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
        "Upload a file",          # ← merged text
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
        "text-align:center;letter-spacing:2px;'>born from stars ",
        unsafe_allow_html=True
    )

# ==============================================================================
# MAIN CONTENT
# ==============================================================================

st.markdown("""
<div class='brand'>✦ ANNOVA</div>
<div class='brand-sub'>born from stars </div>
""", unsafe_allow_html=True)

# Chat history
for msg in st.session_state.history:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# Chat input
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

        


        