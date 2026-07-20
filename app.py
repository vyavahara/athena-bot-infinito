import streamlit as st
from google import genai
from google.genai import types

# 1. Recupera la chiave dai Secrets
api_key = st.secrets["GEMINI_API_KEY"]

# 2. Crea il client in modo pulito
client = genai.Client(api_key=api_key)

# 3. Definizione Istruzioni di Sistema (Athena Maieutica)
system_instruction_corrente = """
Sei Athena, un'assistente didattica socratica per il laboratorio sull'infinito.
Non dare mai risposte dirette. Rispondi ponendo domande guidate che facciano riflettere lo studente.
"""

# 4. Inizializza lo storico dei messaggi in session_state se non esiste
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Visualizza i messaggi precedenti nella chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. Input dell'utente
if prompt := st.chat_input("Fai una domanda ad Athena..."):
    # Mostra il messaggio utente
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepara la cronologia per il nuovo client
    contents_history = []
    for m in st.session_state.messages:
        role = "user" if m["role"] == "user" else "model"
        contents_history.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=m["content"])]
            )
        )

    # Invia la richiesta con il modello gemini-2.5-flash o gemini-1.5-flash
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # Oppure "gemini-1.5-flash"
            contents=contents_history,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction_corrente,
                temperature=0.7,
            )
        )
        
        # Mostra e salva la risposta
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"Errore nella generazione della risposta: {e}")
