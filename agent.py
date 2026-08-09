import streamlit as st
from openai import OpenAI

# ---------------------------------------------------------
# KONFIGURASI UTAMA
# ---------------------------------------------------------
API_KEY = "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"
BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME = "meta-llama/llama-3.1-8b-instruct:free"

# ---------------------------------------------------------
# TAMPILAN & TEMA (HACKER RED & BLACK AESTHETIC)
# ---------------------------------------------------------
st.set_page_config(
    page_title="EXELYN AGENT",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #0d0000;
        color: #ff3333;
        font-family: 'Courier New', Courier, monospace;
    }
    h1 {
        color: #ff0000 !important;
        text-shadow: 0 0 10px #ff0000;
        font-family: 'Courier New', Courier, monospace;
        text-align: center;
        border-bottom: 2px solid #ff0000;
        padding-bottom: 10px;
    }
    .stChatInputContainer textarea {
        background-color: #1a0000 !important;
        color: #ff3333 !important;
        border: 1px solid #ff0000 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    [data-testid="stChatMessage"] {
        background-color: #150000;
        border: 1px solid #400000;
        border-radius: 5px;
        color: #ff6666;
    }
    code {
        color: #00ff66 !important;
        background-color: #050505 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ EXELYN AGENT ⚡")
st.caption("SYSTEM STATUS: ONLINE | PROTOCOL: CODING ASSISTANT")

SYSTEM_PROMPT = """
You are EXELYN AGENT, an elite hacker-style AI coding assistant.
Your responses must be precise, highly technical, clean, and optimized.
Always write clean, secure code and explain complex logic efficiently.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input dari pengguna
if prompt := st.chat_input("Enter code or command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            messages_payload = [{"role": "system", "content": SYSTEM_PROMPT}] + [
                {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
            ]

            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages_payload,
                stream=True
            )

            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"SYSTEM ACCESS DENIED / ERROR: {str(e)}")

            
 
