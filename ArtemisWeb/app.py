import streamlit as st
from google import genai
import time

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="ARTEMIS NEURAL WEB",
    page_icon="💜",
    layout="centered"
)

# --- ESTILO CSS PERSONALIZADO (Look & Feel Artemis) ---
st.markdown("""
    <style>
    /* Fondo general */
    .stApp {
        background-color: #080808;
        color: #FFFFFF;
    }
    /* Estilo del Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0D0D0D !important;
        border-right: 1px solid #1A1A1A;
    }
    /* Input de texto */
    .stTextInput > div > div > input {
        background-color: #121212 !important;
        color: #A855F7 !important;
        border: 1px solid #A855F7 !important;
    }
    /* Botones */
    .stButton > button {
        background-color: #A855F7 !important;
        color: white !important;
        border-radius: 10px !important;
    }
    /* Títulos */
    h1, h2, h3 {
        color: #A855F7 !important;
        font-family: 'Arial', sans-serif;
    }
    /* Burbujas de chat */
    [data-testid="stChatMessage"] {
        background-color: #121212 !important;
        border-radius: 15px !important;
        border: 1px solid #1A1A1A;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURACIÓN DEL MOTOR ---
# Usamos tu última API Key que funciona con el SDK genai
API_KEY = "AIzaSyAssF_oqDhTsV6g6GYiqv_YnBziStUyej8"

# Inicializar historial de chat si no existe
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR ---
with st.sidebar:
    st.title("ARTEMIS v8.3")
    st.subheader("SYSTEM STATUS")
    st.success("● ENGINE ONLINE")
    st.info("Hospedado en Streamlit Cloud")
    
    if st.button("Resetear Memoria"):
        st.session_state.messages = []
        st.rerun()

# --- INTERFAZ PRINCIPAL ---
st.title("✦ NEURAL INTERFACE")
st.markdown("---")

# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de comandos
if prompt := st.chat_input("Escribe un comando para Artemis..."):
    # Guardar y mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta de la IA
    try:
        client = genai.Client(api_key=API_KEY)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Llamada al modelo
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )
            
            # Efecto de escritura "Typing"
            for word in response.text.split(' '):
                full_response += word + " "
                time.sleep(0.03)
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        
        # Guardar respuesta en el historial
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
    except Exception as e:
        st.error(f"SYSTEM ERROR: No se pudo enlazar con el motor. Detalle: {e}")