import streamlit as st
from google import genai
from google.genai import types

# ------------------------------------------------------------------------------
# 1. Configurazione della Pagina
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Athena - Assistente Socratica",
    page_icon="🏛️",
    layout="centered"
)

# ------------------------------------------------------------------------------
# 2. Stile Visivo: Sfondo Blu Elegante e Testo Chiaro Ad Alto Contrasto
# ------------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Sfondo principale dell'applicazione */
    .stApp {
        background-color: #0b192c;
        color: #ffffff;
    }

    /* Box di Benvenuto Info */
    div[data-testid="stNotification"] {
        background-color: #1e3e62;
        color: #ffffff;
        border: 1px solid #00adb5;
        border-radius: 10px;
    }

    /* Formattazione Testi e Titoli */
    h1, h2, h3, p, span, div, caption {
        color: #f0f6fc !important;
    }

    /* Stile Riquadri Messaggi Chat */
    div[data-testid="stChatMessage"] {
        background-color: #1a2e40;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 10px;
        border: 1px solid #2a4560;
    }

    /* Centratura e stile dell'Avatar */
    .avatar-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 15px;
    }
    .avatar-img {
        width: 180px;
        height: auto;
        border-radius: 50%;
        box-shadow: 0px 4px 15px rgba(0, 173, 181, 0.4);
        border: 2px solid #00adb5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------------------------
# 3. Lettura Parametro Colonna da Padlet (?colonna=1, ?colonna=2, etc.)
# ------------------------------------------------------------------------------
query_params = st.query_params
colonna = query_params.get("colonna", "1")

sezioni_titoli = {
    "1": "Sezione 1: Filosofia e Paradossi (Zenone, Hilbert)",
    "2": "Sezione 2: Il Rigore del Limite e del Continuo",
    "3": "Sezione 3: Le Serie Matematiche e i Frattali",
    "4": "Sezione 4: Arte (Escher) e Creatività Digitale"
}
sezione_attuale = sezioni_titoli.get(colonna, sezioni_titoli["1"])

# ------------------------------------------------------------------------------
# 4. Intestazione: Avatar Incorporato, Titolo e Messaggio di Benvenuto
# ------------------------------------------------------------------------------
# Render dell'avatar tramite GitHub Raw permalink garantito
URL_AVATAR = "https://raw.githubusercontent.com/athena-bot-infinito/main/AV_Athena.png"

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Mostriamo l'immagine dell'Avatar Athena
    st.image("AV_Athena.png", use_container_width=True)

st.title("🏛️ Athena")
st.caption(f"📍 **{sezione_attuale}**")

st.info(
    "👋 **Benvenuto/a nel Laboratorio sull'Infinito!**\n\n"
    "Sono **Athena**, la tua guida didattica. Il mio compito non è fornirti risposte pronte o soluzioni dirette, "
    "ma aiutarti a ragionare ponendoti le giuste domande socratiche. "
    "Esploriamo insieme i concetti matematici e filosofici: dimmi, da cosa vuoi partire?"
)

st.divider()

# ------------------------------------------------------------------------------
# 5. Inizializzazione Client Google GenAI
# ------------------------------------------------------------------------------
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

# ------------------------------------------------------------------------------
# 6. System Instruction Maieutica (Metodo Socratico)
# ------------------------------------------------------------------------------
prompt_base = (
    "Sei Athena, un'assistente didattica socratica per un laboratorio sull'infinito. "
    "Rispondi ponendo domande guidate, senza mai dare soluzioni dirette."
)

if colonna == "1":
    prompt_colonna = prompt_base + " Ti trovi nella Sezione 1: Filosofia e Paradossi (Zenone, Hilbert)."
elif colonna == "2":
    prompt_colonna = prompt_base + " Ti trovi nella Sezione 2: Il Rigore del Limite e del Continuo."
elif colonna == "3":
    prompt_colonna = prompt_base + " Ti trovi nella Sezione 3: Le Serie Matematiche e i Frattali."
else:
    prompt_colonna = prompt_base + " Ti trovi nella Sezione 4: Arte (Escher) e Creatività Digitale."

# ------------------------------------------------------------------------------
# 7. Gestione Cronologia Chat e Interazione
# ------------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Ripristino messaggi della sessione corrente
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Prompt Input Utente
if prompt := st.chat_input("Fai la tua domanda ad Athena..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Ricostruzione cronologia per l'API
    contents_history = []
    for m in st.session_state.messages:
        role = "user" if m["role"] == "user" else "model"
        contents_history.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=m["content"])]
            )
        )

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=contents_history,
            config=types.GenerateContentConfig(
                system_instruction=prompt_colonna,
                temperature=0.7,
            )
        )
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"Errore nella risposta: {e}")
