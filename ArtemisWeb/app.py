import google.generativeai as genai
import os

# --- CONFIGURAÇÃO DO ARTEMIS ---
# Substitua 'SUA_API_KEY_AQUI' pela sua chave real do Google AI Studio
CHAVE_API = "SUA_API_KEY_AQUI"
genai.configure(api_key=CHAVE_API)

# Configurações de geração (opcional, para deixar as respostas melhores)
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 1000,
}

# Inicializando o modelo corretamente
# Usamos o 'gemini-1.5-flash' que é o mais atual para projetos como o seu
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config
)

def iniciar_artemis():
    # Inicia o histórico do chat vazio
    chat = model.start_chat(history=[])
    
    print("--- ARTEMIS ONLINE ---")
    print("Pode falar comigo! (Digite 'sair' para encerrar)")
    print("-----------------------")

    while True:
        pergunta = input("Você: ")

        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("Artemis: Falou, meu parceiro! Até a próxima.")
            break

        try:
            # Envia a mensagem para o Gemini
            response = chat.send_message(pergunta)
            
            # Exibe a resposta do Modo Chat
            print(f"Artemis: {response.text}")
            print("-" * 20)

        except Exception as e:
            print(f"Ops, deu um erro aqui: {e}")

if __name__ == "__main__":
    iniciar_artemis()
