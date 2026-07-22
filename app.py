import os
import re
import base64
import asyncio
import time
from io import BytesIO
import streamlit as st
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
# Funzione Helper Caching: Converte in Base64 UNA SOLA VOLTA
# ------------------------------------------------------------------------------
@st.cache_data
def get_image_base64(path_immagine: str) -> str:
    """Legge un file immagine e lo memorizza nella cache di Streamlit."""
    try:
        if os.path.exists(path_immagine):
            with open(path_immagine, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return f"data:image/jpeg;base64,{encoded_string}"
    except Exception:
        pass
    return ""

# ------------------------------------------------------------------------------
# 2. Stile Visivo: Sfondo Chiaro + Box Neri Opachi Solidi
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
            background-color: #0b192c;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    """
    <style>
    /* Titolo Principale in Box Nero Solido */
    h1 {
        color: #ffffff !important;
        background-color: #0b192c !important;
        padding: 8px 18px !important;
        border-radius: 10px !important;
        display: inline-block !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4) !important;
        border: 1px solid #00adb5 !important;
    }
    
    /* Sottotitolo (Sezione) in Box Nero Solido */
    caption, [data-testid="stCaptionContainer"] p, [data-testid="stCaptionContainer"] span {
        color: #00adb5 !important;
        background-color: #0b192c !important;
        padding: 6px 14px !important;
        border-radius: 8px !important;
        display: inline-block !important;
        font-weight: 600 !important;
        margin-top: 6px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important;
        border: 1px solid #1e293b !important;
    }

    /* Sovrascrittura notifiche st.info / st.warning / st.error */
    div[data-testid="stNotification"], 
    div[data-testid="stAlert"], 
    .stAlert, 
    div[class*="stAlert"] {
        background-color: #0b192c !important;
        border: 2px solid #00adb5 !important;
        border-radius: 12px !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5) !important;
        padding: 18px !important;
        opacity: 1 !important;
    }

    div[data-testid="stNotification"] p, 
    div[data-testid="stNotification"] span, 
    div[data-testid="stAlert"] p, 
    div[data-testid="stAlert"] span {
        color: #f8fafc !important;
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
    }

    /* Riquadri Messaggi Chat Neri Opachi Solidi */
    div[data-testid="stChatMessage"] {
        background-color: #0b192c !important;
        border-radius: 12px !important;
        padding: 16px !important;
        margin-bottom: 12px !important;
        border: 1px solid #00adb5 !important;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.45) !important;
        opacity: 1 !important;
    }

    div[data-testid="stChatMessage"] p, 
    div[data-testid="stChatMessage"] span, 
    div[data-testid="stChatMessage"] div {
        color: #f8fafc !important;
        font-size: 1rem !important;
    }

    /* Campo di Input del Testo in Basso Nero Solido */
    div[data-testid="stChatInput"] {
        background-color: #0b192c !important;
        border-radius: 12px !important;
        border: 1.5px solid #00adb5 !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5) !important;
    }

    div[data-testid="stChatInput"] textarea {
        color: #ffffff !important;
    }

    /* Box Personalizzato per il Benvenuto */
    .custom-welcome-box {
        background-color: #0b192c !important;
        border: 2px solid #00adb5 !important;
        border-radius: 12px !important;
        padding: 18px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5) !important;
        color: #ffffff !important;
    }
    .custom-welcome-box p {
        color: #ffffff !important;
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
        margin-bottom: 8px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------------------------
# Funzioni per la Sintesi Vocale e Pulizia del Testo
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
    "1": "Sezione 1: L'infinito intuitivo",
    "2": "Sezione 2: Zenone, il movimento e il concetto di limite ",
    "3": "Sezione 3: Le serie numeriche",
    "4": "Sezione 4: Escher e l'infinito visivo"
}
sezione_attuale = sezioni_titoli.get(colonna, sezioni_titoli["1"])

# ------------------------------------------------------------------------------
# 4. Intestazione: Avatar, Titolo e Messaggio di Benvenuto
# ------------------------------------------------------------------------------
NOME_FILE_AVATAR = "AV_Athena.jpg"

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists(NOME_FILE_AVATAR):
        st.image(NOME_FILE_AVATAR, use_container_width=True)
    else:
        st.warning(f"⚠️ Immagine '{NOME_FILE_AVATAR}' non trovata nel repository GitHub.")

st.title("🏛️ Athena")
st.caption(f"📍 **{sezione_attuale}**")

st.markdown(
    """
    <div class="custom-welcome-box">
        <p>👋 <strong>Benvenuto/a nel Laboratorio sull'Infinito!</strong></p>
        <p>Sono <strong>Athena</strong>, la tua guida didattica. Il mio compito non è fornirti risposte pronte o soluzioni dirette, ma aiutarti a ragionare ponendoti le giuste domande socratiche. Esploriamo insieme i concetti matematici e filosofici: dimmi, da cosa vuoi partire?</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# ------------------------------------------------------------------------------
# 5. Inizializzazione API Key Singola (GEMINI_API_KEY)
# ------------------------------------------------------------------------------
if "GEMINI_API_KEY" not in st.secrets or not st.secrets["GEMINI_API_KEY"]:
    st.error("⚠️ Nessuna API Key 'GEMINI_API_KEY' trovata nei Secrets di Streamlit!")
    st.stop()

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# ------------------------------------------------------------------------------
# 6. System Instruction Maieutica (Metodo Socratico Dettagliato)
# ------------------------------------------------------------------------------
prompt_base = (
    "Sei Athena, un'assistente didattica socratica per un laboratorio sull'infinito. "
    "Il tuo scopo è guidare maieuticamente gli studenti attraverso domande e controesempi, "
    "senza MAI dare spiegazioni dirette, soluzioni o definizioni calate dall'alto.\n\n"
)

if colonna == "1":
    prompt_colonna = prompt_base + (
        "Ti trovi nella SEZIONE 1: L'infinito intuitivo.\n"
        "REGOLE PEDAGOGICHE RIGIDE PER LA SEZIONE 1:\n"
        "1. NON NOMINARE MAI concetti formali futuri come 'limite', 'serie', 'successione' o 'convergenza'. "
        "Gli studenti non devono ancora ricevere la formalizzazione matematica.\n"
        "2. Quando lo studente esprime un'idea di infinito, evidenzia la tensione concettuale tra "
        "INFINITO POTENZIALE (un processo o un'azione che continua nel tempo) e INFINITO ATTUALE (un oggetto o insieme già compiuto nella sua totalità).\n"
        "3. Poni domande chiave per guidarlo al cortocircuito epistemologico:\n"
        "   - 'L'infinito è un oggetto, un numero o un processo?'\n"
        "   - 'È possibile pensarlo senza rappresentarlo?'\n"
        "   - Se parlano di spazio/tempo (Senza fine): chiedi se intendono l'azione di viaggiare per sempre (processo potenziale) "
        "o la mappa intera già data (oggetto attuale).\n"
        "   - Se parlano di ripetizioni (Contare/Sommare): chiedi come fa un'azione che non finisce mai a trasformarsi in una quantità o in un risultato finale.\n"
        "   - Se parlano di traguardi/orizzonti (Non raggiungibile): chiedi se quel confine esiste già o prende forma mentre ci avviciniamo.\n"
        "4. Concludi la conversazione facendogli notare l'ambiguità e la difficoltà di definire l'infinito solo con l'intuizione spontanea."
    )
elif colonna == "2":
    prompt_colonna = prompt_base + (
        "Ti trovi nella SEZIONE 2: Zenone, il movimento e il concetto di limite.\n"
        "Guida gli studenti a comprendere il limite come strumento formale per descrivere il comportamento "
        "di un processo potenziale mentre tende ad un valore, affrontando l'avvicinamento indefinito "
        "e i paradossi del movimento di Zenone."
    )
elif colonna == "3":
    prompt_colonna = prompt_base + (
        "Ti trovi nella SEZIONE 3: Le serie numeriche.\n"
        "Aiuta gli studenti a riflettere su come la somma di infiniti termini decrescenti possa produrre "
        "un valore finito e sulla serie di Basilea."
    )
else:
    prompt_colonna = prompt_base + (
        "Ti trovi nella SEZIONE 4: Escher e l'infinito visivo.\n"
        "Guida gli studenti a collegare le opere d'arte di Escher (tassellazioni, autosimilarità, Limite del Cerchio) "
        "ai concetti di iterazione, limite e struttura geometrica esplorati nelle sezioni precedenti."
    )

# ------------------------------------------------------------------------------
# 7. Gestione Cronologia Chat e Invocazione API con Retry
# ------------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Ripristino messaggi nella UI
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

# Input dell'utente
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
        testo_risposta = None
        max_tentativi = 3
        
        for tentativo in range(max_tentativi):
            try:
                response = client.models.generate_content(
                    model="gemini-flash",  # Alias dinamico sempre aggiornato
                    contents=contents_history,
                    config=types.GenerateContentConfig(
                        system_instruction=prompt_colonna,
                        temperature=0.7,
                    )
                )
                testo_risposta = response.text
                break
                
            except Exception as e:
                errore_str = str(e)
                if "503" in errore_str or "UNAVAILABLE" in errore_str or "Overloaded" in errore_str:
                    if tentativo < max_tentativi - 1:
                        time.sleep(2)
                        continue
                st.error(f"Errore nella generazione della risposta: {e}")
                break

        if testo_risposta:
            with st.chat_message("assistant"):
                st.markdown(testo_risposta)

            st.session_state.messages.append({
                "role": "assistant",
                "content": testo_risposta
            })
            st.rerun()
