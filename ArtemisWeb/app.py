import streamlit as st
import google.generativeai as genai

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Artemis AI", page_icon="🤖", layout="centered")

# Estilo CSS customizado para deixar bonitão
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÃO DA API ---
# No Streamlit Cloud, o ideal é usar st.secrets["API_KEY"]
# Para testar rápido, você pode manter a string, mas recomendo os Secrets!
CHAVE_API = "AIzaSyAssF_oqDhTsV6g6GYiqv_YnBziStUyej8" 
genai.configure(api_key=CHAVE_API)

model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- INICIALIZAÇÃO DO HISTÓRICO ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# --- INTERFACE ---
st.title("🤖 Artemis Project")
st.subheader("O seu assistente inteligente")

# Barra Lateral (Sidebar)
with st.sidebar:
    st.title("Configurações")
    if st.button("Limpar Conversa"):
        st.session_state.messages = []
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()
    st.write("---")
    st.write("Versão: 2.0 (Web Edition)")

# Exibir o histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de entrada (Input)
if prompt := st.chat_input("Diga algo para o Artemis..."):
    # Mostra a mensagem do usuário
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Resposta do Artemis
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Envia para a API
            response = st.session_state.chat_session.send_message(prompt)
            full_response = response.text
            message_placeholder.markdown(full_response)
            
            # Salva no histórico
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Erro na conexão: {e}")
