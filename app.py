import os
import re
import base64
import asyncio
from io import BytesIO
import streamlit as st
from PIL import Image
import edge_tts
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
# Funzione Helper: Converte Immagine Locale in Base64 per CSS
# ------------------------------------------------------------------------------
def get_image_base64(path_immagine: str) -> str:
    """Legge un file immagine e lo converte in una stringa base64."""
    if os.path.exists(path_immagine):
        with open(path_immagine, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded_string}"
    return ""

# ------------------------------------------------------------------------------
# 2. Stile Visivo: Sfondo Chiaro + Box Opachi ad Alto Contrasto
# ------------------------------------------------------------------------------
NOME_FILE_SFONDO = "Athena_sfondo.jpg"
bg_base64 = get_image_base64(NOME_FILE_SFONDO)

if bg_base64:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{bg_base64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f4f6f8;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    """
    <style>
    /* Titoli con sfondo protettivo chiaro per staccare dallo sfondo */
    h1 {
        color: #0f172a !important;
        background: rgba(255, 255, 255, 0.88);
        padding: 6px 16px;
        border-radius: 8px;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    caption, [data-testid="stCaptionContainer"] {
        color: #1e293b !important;
        background: rgba(255, 255, 255, 0.88);
        padding: 4px 10px;
        border-radius: 6px;
        display: inline-block;
        font-weight: 600;
        margin-top: 4px;
    }

    /* Box di Benvenuto opaco ad altissima leggibilità */
    div[data-testid="stNotification"] {
        background-color: #ffffff !important;
        border: 2px solid #00adb5 !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15) !important;
        padding: 16px !important;
    }
    
    div[data-testid="stNotification"] p, div[data-testid="stNotification"] span {
        color: #0f172a !important;
        font-size: 1.05rem !important;
        line-height: 1.5 !important;
    }

    /* Riquadri Messaggi Chat bianchi e nitidi */
    div[data-testid="stChatMessage"] {
        background-color: #ffffff !important;
        border-radius: 12px !important;
        padding: 16px !important;
        margin-bottom: 12px !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12) !important;
    }

    div[data-testid="stChatMessage"] p, div[data-testid="stChatMessage"] span {
        color: #0f172a !important;
        font-weight: 450 !important;
    }

    /* Campo di Input in basso */
    div[data-testid="stChatInput"] {
        background-color: #ffffff !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------------------------
# Funzioni per la Sintesi Vocale e Pulizia del Testo Markdown
# ------------------------------------------------------------------------------
def pulisci_testo_per_audio(testo: str) -> str:
    """Rimuove asterischi, cancelletti e formattazioni Markdown per l'ascolto."""
    testo_pulito = re.sub(r'\*+', '', testo)
    testo_pulito = re.sub(r'#+', '', testo_pulito)
    testo_pulito = re.sub(r'^\s*-\s+', '', testo_pulito, flags=re.MULTILINE)
    return testo_pulito.strip()

async def genera_audio_femminile(testo: str) -> bytes:
    """Genera file audio MP3 con voce neurale femminile italiana (Elsa)."""
    VOICE = "it-IT-ElsaNeural"
    testo_vocale = pulisci_testo_per_audio(testo)
    communicate = edge_tts.Communicate(testo_vocale, VOICE)
    fp = BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            fp.write(chunk["data"])
    fp.seek(0)
    return fp.read()

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
# 4. Intestazione: Avatar, Titolo e Messaggio di Benvenuto
# ------------------------------------------------------------------------------
NOME_FILE_AVATAR = "AV_Athena.jpg"

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists(NOME_FILE_AVATAR):
        image = Image.open(NOME_FILE_AVATAR)
        st.image(image, use_container_width=True)
    else:
        st.warning(f"⚠️ Immagine '{NOME_FILE_AVATAR}' non trovata nel repository GitHub.")

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
# 7. Gestione Cronologia Chat con Generazione Vocale On-Demand
# ------------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Ripristino messaggi
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            if "audio" in msg:
                st.audio(msg["audio"], format="audio/mp3")
            else:
                if st.button("🔊 Ascolta la risposta", key=f"btn_{idx}"):
                    with st.spinner("🔊 Generazione voce in corso..."):
                        audio_b = asyncio.run(genera_audio_femminile(msg["content"]))
                        msg["audio"] = audio_b
                        st.rerun()

# Prompt Input Utente
if prompt := st.chat_input("Fai la tua domanda ad Athena..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    contents_history = []
    for m in st.session_state.messages:
        role = "user" if m["role"] == "user" else "model"
        contents_history.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=m["content"])]
            )
        )

    with st.spinner("⏳ Athena sta riflettendo..."):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=contents_history,
                config=types.GenerateContentConfig(
                    system_instruction=prompt_colonna,
                    temperature=0.7,
                )
            )
            
            testo_risposta = response.text

            with st.chat_message("assistant"):
                st.markdown(testo_risposta)

            st.session_state.messages.append({
                "role": "assistant",
                "content": testo_risposta
            })
            st.rerun()

        except Exception as e:
            st.error(f"Errore nella risposta: {e}")
