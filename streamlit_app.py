import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable or use a default for development
API_KEY = os.getenv("API_KEY", "development-key")

st.set_page_config(page_title="Agentic AI Chat", layout="centered")
st.title("🤖 Agentic AI Prototype")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input field
user_input = st.chat_input("Digite sua pergunta...")

# If user sent something
if user_input:
    # Add question to history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    try:
        # Call FastAPI with API key
        headers = {"X-API-Key": API_KEY}
        response = requests.get(
            "http://localhost:8000/ask",
            params={"question": user_input},
            headers=headers
        )
        
        if response.status_code == 200:
            answer = response.json()["response"]
        else:
            answer = f"Erro na requisição: {response.status_code} - {response.text}"

    except Exception as e:
        answer = f"[Erro ao conectar ao backend]: {e}"

    # Add response to history
    st.session_state.chat_history.append({"role": "agent", "content": answer})

# Render chat
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
