import streamlit as st
from google import genai
import time

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="ARTEMIS NEURAL WEB",
    page_icon="💜",
    layout="centered"
)

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    .stApp {
        background-color: #080808;
        color: #FFFFFF;
    }
    section[data-testid="stSidebar"] {
        background-color: #0D0D0D !important;
        border-right: 1px solid #1A1A1A;
    }
    .stTextInput > div > div > input {
        background-color: #121212 !important;
        color: #A855F7 !important;
        border: 1px solid #A855F7 !important;
    }
    h1, h2, h3 {
        color: #A855F7 !important;
    }
    [data-testid="stChatMessage"] {
        background-color: #121212 !important;
        border-radius: 15px !important;
        border: 1px solid #1A1A1A;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURACIÓN DEL MOTOR ---
# Tu clave de API
API_KEY = "AIzaSyAssF_oqDhTsV6g6GYiqv_YnBziStUyej8"

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR ---
with st.sidebar:
    st.title("ARTEMIS v8.3")
    st.subheader("SYSTEM STATUS")
    st.success("● ONLINE")
    if st.button("Resetear Memoria"):
        st.session_state.messages = []
        st.rerun()

# --- INTERFAZ DE CHAT ---
st.title("✦ NEURAL INTERFACE")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe un comando para Artemis..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Usamos el cliente actualizado
        client = genai.Client(api_key=API_KEY)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Usamos gemini-2.0-flash que es la versión más actual y estable
            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=prompt
            )
            
            # Efecto de tipeo
            if response.text:
                for word in response.text.split(' '):
                    full_response += word + " "
                    time.sleep(0.02)
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            else:
                st.error("El modelo no devolvió texto.")
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
    except Exception as e:
        st.error(f"SYSTEM ERROR: {e}")
