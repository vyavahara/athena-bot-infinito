import streamlit as st
from google import genai

st.title("🧪 Test Modelli AI Studio")

# 1. Recupero API Key dai Secrets di Streamlit
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
    st.success("API Key trovata nei Secrets!")
except Exception as e:
    st.error(f"Errore nella lettura della chiave API dai Secrets: {e}")
    st.stop()

# 2. Chiamata ListModels per elencare i modelli attivi
st.subheader("📋 Elenco dei modelli disponibili per la tua chiave:")

try:
    models_found = []
    for model in client.models.list():
        # Filtra solo i modelli che supportano la generazione di testo (generateContent)
        if hasattr(model, "supported_actions") and "generateContent" in model.supported_actions:
            models_found.append(model.name)
        elif not hasattr(model, "supported_actions"):
            models_found.append(model.name)

    if models_found:
        for m in models_found:
            st.code(m)
    else:
        st.warning("Nessun modello restituito dall'API.")

except Exception as e:
    st.error(f"Errore durante la chiamata ListModels: {e}")
