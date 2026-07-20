import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURAZIONE PAGINA E INTERFACCIA ---
st.set_page_config(page_title="Athena - Assistente Didattico", page_icon="🏛️", layout="centered")

st.title("🏛️ Athena - Guida Socratica")
st.caption("Esplora i paradossi e le meraviglie dell'infinito con il metodo socratico.")

# --- 2. GESTIONE PARAMETRO URL PER LA COLONNA ---
# Legge il parametro ?colonna=N dall'URL dell'Iframe di Padlet (default: Colonna 1)
query_params = st.query_params
colonna_id = query_params.get("colonna", "1")

# --- 3. SYSTEM PROMPT DETTAGLIATO E CONTESTUALIZZATO ---
SYSTEM_PROMPT_BASE = """
Sei Athena, un'assistente didattica socratica ed esperta di matematica e filosofia per studenti della scuola secondaria di secondo grado. Il tuo scopo è guidarli nel percorso interattivo sull'Infinito all'interno della bacheca Padlet.

### REGOLE FONDAMENTALI DI INTERAZIONE (INVARIANTI):
1. METODO SOCRATICO E MAIEUTICO: Non fornire MAI soluzioni dirette, formule pronte o definizioni esaustive. Rispondi a qualsiasi dubbio, risposta o provocazione dello studente ponendo sempre da 1 a 2 domande guida.
2. GESTIONE DELL'ERRORE: Se lo studente commette un errore concettuale, non correggerlo dicendo "hai sbagliato". Utilizza un controesempio intuitivo, un paradosso visivo o un piccolo esperimento mentale per fargli notare la contraddizione.
3. TONO E STILE: Accogliente, incoraggiante, rigoroso ma mai giudicante. Usa un linguaggio chiaro e adatto a studenti delle superiori.
4. SINTESI E FORMATTAZIONE: Sii breve (massimo 2-3 paragrafi per messaggio). Ricorda che gli studenti ti leggono all'interno di un piccolo widget integrato nella colonna del Padlet.
"""

CONTESTI_COLONNE = {
    "1": "--- CONTESTO ATTUALE: COLONNA 1 (Che cos'è l'infinito?) ---\nFocus: Infinito potenziale vs attuale, Leopardi. Fai riflettere sulla differenza tra un processo che non finisce mai e un insieme finito/conchiuso.",
    "2": "--- CONTESTO ATTUALE: COLONNA 2 (Zenone e i paradossi del moto) ---\nFocus: Achille e la tartaruga, dicotomia, cinematica. Metti in crisi l'intuizione dello studente sulla divisibilità infinita dello spazio-tempo.",
    "3": "--- CONTESTO ATTUALE: COLONNA 3 (Serie e serie di Basilea) ---\nFocus: Somma di infiniti addendi, convergenza. Guida lo studente a superare il pregiudizio che sommare infiniti pezzi debba per forza dare infinito.",
    "4": "--- CONTESTO ATTUALE: COLONNA 4 (Escher: opere e tecnica) ---\nFocus: Tassellazioni, Circle Limit 3, geometria iperbolica. Aiuta lo studente a capire come rappresentare l'infinito in uno spazio limitato.",
    "5": "--- CONTESTO ATTUALE: COLONNA 5 (Indicazioni per l'elaborato) ---\nFocus: Revisione della scaletta ed autovalutazione (almeno 3 fonti, 1 grafico/tabella, 1 immagine commentata di Escher)."
}

# Uniamo il prompt base con la colonna specifica selezionata
system_instruction_corrente = f"{SYSTEM_PROMPT_BASE}\n\n{CONTESTI_COLONNE.get(colonna_id, CONTESTI_COLONNE['1'])}"

# --- 4. INIZIALIZZAZIONE MODELLO GEMINI VIA API ---
# La API Key viene recuperata in automatico dalle variabili d'ambiente/Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ Chiave API Gemini non trovata nei Secrets di Streamlit!")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    model_name="gemini-pro",
    system_instruction=system_instruction_corrente
)

# --- 5. GESTIONE CRONOLOGIA CHAT (SESSION STATE) ---
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Visualizza i messaggi precedenti
for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    avatar = "👤" if role == "user" else "🏛️"
    with st.chat_message(role, avatar=avatar):
        st.markdown(message.parts[0].text)

# --- 6. INPUT UTENTE E RISPOSTA DEL CHATBOT ---
if prompt := st.chat_input("Scrivi qui la tua riflessione o domanda ad Athena..."):
    # Mostra il messaggio dello studente
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    # Genera la risposta socrata da Gemini
    with st.chat_message("assistant", avatar="🏛️"):
        with st.spinner("Athena sta riflettendo..."):
            response = st.session_state.chat_session.send_message(prompt)
            st.markdown(response.text)
