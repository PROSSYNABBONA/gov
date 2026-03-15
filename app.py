import streamlit as st
from dotenv import load_dotenv
import requests
import os

load_dotenv()


st.set_page_config(page_title="Govttalk Uganda", page_icon="🇺🇬", layout="wide")

# Custom CSS and animation for a modern look
st.markdown(
    """
    <style>
    .stChatMessage.user {
        background: #e3f2fd;
        border-radius: 1.2em 1.2em 0 1.2em;
        padding: 1em;
        margin-bottom: 0.5em;
    }
    .stChatMessage.assistant {
        background: #fffde7;
        border-radius: 1.2em 1.2em 1.2em 0;
        padding: 1em;
        margin-bottom: 0.5em;
    }
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-40px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(40px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .govttalk-loader {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 3em;
        margin-bottom: 2em;
    }
    .lds-ring {
      display: inline-block;
      position: relative;
      width: 64px;
      height: 64px;
    }
    .lds-ring div {
      box-sizing: border-box;
      display: block;
      position: absolute;
      width: 51px;
      height: 51px;
      margin: 6px;
      border: 6px solid #1a237e;
      border-radius: 50%;
      animation: lds-ring 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
      border-color: #1a237e transparent transparent transparent;
    }
    .lds-ring div:nth-child(1) { animation-delay: -0.45s; }
    .lds-ring div:nth-child(2) { animation-delay: -0.3s; }
    .lds-ring div:nth-child(3) { animation-delay: -0.15s; }
    @keyframes lds-ring {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Large centered Govttalk heading at the very top
st.markdown('<h1 style="text-align:center; font-size:3.5rem; font-family:Georgia,serif; color:#fff; margin-top:1.5rem; margin-bottom:0.5rem; letter-spacing:2px;">Govttalk</h1>', unsafe_allow_html=True)

# Info box under the header
st.info("""
Welcome to Govttalk Uganda! This chatbot helps you understand Ugandan laws, policies, and Hansards (2015–2024). Type your question below and get answers with practical interpretations for citizens.
""", icon="💡")



# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

# Replace OpenAI chat logic with Grok
def ask_grok(messages, model="grok-4-latest", temperature=0):
    GROK_API_KEY = os.getenv("GROK_API_KEY")
    if not GROK_API_KEY or not GROK_API_KEY.startswith("xai-"):
        st.error("Grok API key is missing or invalid. Please check your .env file and restart the app.")
        print("[DEBUG] GROK_API_KEY:", GROK_API_KEY)
        return "[Error: Missing or invalid Grok API key.]"
    GROK_API_URL = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROK_API_KEY}"
    }
    data = {
        "messages": messages,
        "model": model,
        "stream": False,
        "temperature": temperature
    }
    try:
        response = requests.post(GROK_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as e:
        st.error(f"Grok API request failed: {e}\nCheck your API key and permissions.")
        print("[DEBUG] HTTPError:", e)
        return f"[Error: Grok API request failed: {e}]"

if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": f"<b>You:</b> {prompt}"})
    with st.chat_message("user"):
        st.markdown(f"<b>You:</b> {prompt}", unsafe_allow_html=True)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            grok_messages = [
                {"role": "system", "content": "You are Uganda Govttalk, a helpful expert on Ugandan legislation. Answer using ONLY the provided context. Then give a balanced, practical interpretation of how this policy affects ordinary citizens (cost of living, jobs, rural/urban, rights, businesses). Always be honest and end with: 'This is AI analysis — please verify with official sources.'"},
                {"role": "user", "content": prompt}
            ]
            response = ask_grok(grok_messages)
        st.markdown(f"<b>Govttalk:</b> {response}", unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": f"<b>Govttalk:</b> {response}"})

# Sticky footer
st.markdown('''
<style>
.govttalk-footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100vw;
    background: #181a1f;
    z-index: 9999;
    padding-bottom: 0.5em;
}
.govttalk-footer .govttalk-copyright {
    text-align: center;
    color: #888;
    font-size: 0.95em;
    margin-top: 0.2em;
}
</style>
<div class="govttalk-footer">
    <div class="govttalk-copyright">&copy; 2026 Govttalk Uganda</div>
</div>
''', unsafe_allow_html=True)

# Sidebar with branding and description
with st.sidebar:
    # Logo image removed to prevent PIL.UnidentifiedImageError on Streamlit Cloud
    st.markdown('<h2 style="font-family:Georgia,serif; color:#fff;">Govttalk</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#bdbdbd; font-size:1.1rem;">Your Ugandan Law & Policy Chatbot</p>', unsafe_allow_html=True)
    st.markdown('---')
    st.markdown('''
    <ul style="color:#bdbdbd; font-size:1rem; list-style:none; padding-left:0;">
      <li>🇺🇬 <b>Uganda Legal Info</b></li>
      <li>📄 Bills, Constitution, Hansards</li>
      <li>🗓️ 2015–2024 Coverage</li>
      <li>💬 Ask anything legal</li>
    </ul>
    ''', unsafe_allow_html=True)

# Add a 'New Chat' button to the sidebar (no rerun)
with st.sidebar:
    if st.button('➕ New Chat', use_container_width=True):
        st.session_state.messages = []



