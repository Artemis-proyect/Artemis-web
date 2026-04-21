import streamlit as st
from google import genai
import time

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="ARTEMIS NEURAL WEB",
    page_icon="💜",
    layout="centered"
)

# --- ESTILO VISUAL (Look & Feel Artemis) ---
st.markdown("""
    <style>
    /* Fondo negro profundo */
    .stApp {
        background-color: #080808;
        color: #FFFFFF;
    }
    /* Sidebar oscuro */
    section[data-testid="stSidebar"] {
        background-color: #0D0D0D !important;
        border-right: 1px solid #1A1A1A;
    }
    /* Input de texto morado */
    .stTextInput > div > div > input {
        background-color: #121212 !important;
        color: #A855F7 !important;
        border: 1px solid #A855F7 !important;
    }
    /* Títulos en morado */
    h1, h2, h3 {
        color: #A855F7 !important;
    }
    /* Burbujas de chat */
    [data-testid="stChatMessage"] {
        background-color: #121212 !important;
        border-radius: 15px !important;
        border: 1px solid #1A1A1A;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE IA ---
# Tu llave maestra
API_KEY = "AIzaSyAssF_oqDhTsV6g6GYiqv_YnBziStUyej8"

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR ---
with st.sidebar:
    st.title("ARTEMIS v8.3")
    st.subheader("ESTADO DEL SISTEMA")
    st.success("● ONLINE")
    if st.button("Limpiar Memoria"):
        st.session_state.messages = []
        st.rerun()

# --- CHAT PRINCIPAL ---
st.title("✦ INTERFAZ NEURAL")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribí un comando..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Iniciamos el cliente con el nuevo SDK
        client = genai.Client(api_key=API_KEY)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Llamada al modelo Gemini
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )
            
            # Efecto de escritura pro
            for word in response.text.split(' '):
                full_response += word + " "
                time.sleep(0.02)
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
    except Exception as e:
        st.error(f"ERROR: No se pudo conectar con el motor. {e}")
