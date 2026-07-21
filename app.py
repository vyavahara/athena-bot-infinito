import streamlit as st
import google.generativeai as genai

# 1. Lettura Parametro Colonna da Padlet (?colonna=1, ?colonna=2, etc.)
query_params = st.query_params
colonna = query_params.get("colonna", "1")

# 2. Inizializzazione Client con SDK Classica
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# 3. Prompt Maieutico di Athena adattato alla colonna
prompt_base = "Sei Athena, un'assistente didattica socratica per un laboratorio sull'infinito. Rispondi ponendo domande guidate, senza mai dare soluzioni dirette."

if colonna == "1":
    prompt_colonna = prompt_base + " Ti trovi nella Sezione 1: Filosofia e Paradossi (Zenone, Hilbert)."
elif colonna == "2":
    prompt_colonna = prompt_base + " Ti trovi nella Sezione 2: Il Rigore del Limite e del Continuo."
elif colonna == "3":
    prompt_colonna = prompt_base + " Ti trovi nella Sezione 3: Le Serie Matematiche e i Frattali."
else:
    prompt_colonna = prompt_base + " Ti trovi nella Sezione 4: Arte (Escher) e Creatività Digitale."

# Inizializzazione del Modello Stabile con System Instruction
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=prompt_colonna
)

# 4. Gestione Cronologia Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Fai la tua domanda ad Athena..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Ricostruzione cronologia nel formato per google-generativeai
    history_formatted = []
    for m in st.session_state.messages[:-1]: # Tutti tranne l'ultimo appena inserito
        role = "user" if m["role"] == "user" else "model"
        history_formatted.append({"role": role, "parts": [m["content"]]})

    try:
        # Avvio sessione di chat con lo storico
        chat = model.start_chat(history=history_formatted)
        response = chat.send_message(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"Errore nella risposta: {e}")
