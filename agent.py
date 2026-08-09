import streamlit as st
import requests

# Endpoint API Publik Gratis (Llama-3.1-8B)
API_URL = "https://router.huggingface.co/hf-inference/models/meta-llama/Llama-3.1-8B-Instruct/v1/chat/completions"

# ---------------------------------------------------------
# TAMPILAN & CSS ANIMATED CYBERPUNK
# ---------------------------------------------------------
st.set_page_config(
    page_title="EXELYN AGENT",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #080000;
        color: #ff3333;
        font-family: 'Courier New', Courier, monospace;
    }

    @keyframes redGlow {
        0% { text-shadow: 0 0 5px #ff0000, 0 0 10px #ff0000; transform: scale(1); }
        50% { text-shadow: 0 0 20px #ff0000, 0 0 35px #ff0000; transform: scale(1.02); }
        100% { text-shadow: 0 0 5px #ff0000, 0 0 10px #ff0000; transform: scale(1); }
    }

    .animated-title {
        color: #ff0000 !important;
        font-family: 'Courier New', Courier, monospace;
        text-align: center;
        font-size: 2.8rem;
        font-weight: bold;
        letter-spacing: 3px;
        animation: redGlow 2.5s infinite ease-in-out;
        margin-bottom: 5px;
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }

    [data-testid="stChatMessage"] {
        background-color: #120000;
        border: 1px solid #550000;
        border-radius: 8px;
        color: #ff6666;
        animation: fadeInUp 0.4s ease-out forwards;
        box-shadow: 0 0 10px rgba(255, 0, 0, 0.15);
    }

    .stChatInputContainer textarea {
        background-color: #1a0000 !important;
        color: #ff3333 !important;
        border: 1px solid #660000 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }

    code {
        color: #00ff66 !important;
        background-color: #030303 !important;
        border: 1px solid #004411;
    }

    .status-bar {
        text-align: center;
        color: #880000;
        font-size: 0.85rem;
        border-bottom: 1px solid #440000;
        padding-bottom: 12px;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="animated-title">⚡ EXELYN AGENT ⚡</div>', unsafe_allow_html=True)
st.markdown('<div class="status-bar">SYSTEM STATUS: ONLINE | PROTOCOL: PUBLIC INFERENCE ENGINE</div>', unsafe_allow_html=True)

SYSTEM_PROMPT = "You are EXELYN AGENT, an elite hacker-style AI coding assistant."

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Enter code or command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            formatted_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + [
                {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
            ]

            payload = {
                "model": "meta-llama/Llama-3.1-8B-Instruct",
                "messages": formatted_messages,
                "max_tokens": 500
            }

            res = requests.post(API_URL, json=payload, timeout=20)
            
            if res.status_code == 200:
                answer = res.json()["choices"][0]["message"]["content"]
                message_placeholder.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error(f"SYSTEM ACCESS DENIED / HTTP {res.status_code}: {res.text}")

        except Exception as e:
            st.error(f"SYSTEM ERROR: {str(e)}")
