import streamlit as st
import g4f

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
st.markdown('<div class="status-bar">SYSTEM STATUS: ONLINE | PROTOCOL: STABLE FREE ENGINE</div>', unsafe_allow_html=True)

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
            # Gunakan Provider DDG (DuckDuckGo AI) / Blackbox yang tidak perlu cookie/auth
            formatted_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + [
                {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
            ]

            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4o,
                provider=g4f.Provider.DDG,
                messages=formatted_messages
            )
            
            message_placeholder.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            # Fallback otomatis jika provider utama sibuk
            try:
                response = g4f.ChatCompletion.create(
                    model="gpt-4o",
                    provider=g4f.Provider.Blackbox,
                    messages=formatted_messages
                )
                message_placeholder.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as ex:
                st.error(f"SYSTEM ACCESS DENIED / ERROR: {str(ex)}")
