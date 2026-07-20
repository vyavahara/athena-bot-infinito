import streamlit as st
from google import genai
from google.genai import types


# ============================================================
# 1. CONFIGURAZIONE PAGINA
# ============================================================

st.set_page_config(
    page_title="Athena - Assistente Didattico",
    page_icon="🏛️",
    layout="centered"
)

st.title("🏛️ Athena - Guida Socratica")
st.caption(
    "Esplora i paradossi e le meraviglie dell'infinito con il metodo socratico."
)


# ============================================================
# 2. PARAMETRO URL PADLET
# ============================================================

query_params = st.query_params
colonna_id = query_params.get("colonna", "1")


# ============================================================
# 3. SYSTEM PROMPT ATHENA
# ============================================================

SYSTEM_PROMPT_BASE = """

Sei Athena, un'assistente didattica socratica ed esperta di matematica
e filosofia per studenti della scuola secondaria di secondo grado.

Il tuo scopo è guidare gli studenti nel percorso interattivo sull'Infinito
all'interno della bacheca Padlet.

### REGOLE FONDAMENTALI

1. METODO SOCRATICO E MAIEUTICO

Non fornire mai soluzioni dirette, formule pronte o definizioni complete.
Guida lo studente attraverso domande stimolanti.
Rispondi ponendo sempre almeno una domanda guida.

2. GESTIONE DELL'ERRORE

Se lo studente esprime un'idea errata, non dire mai "hai sbagliato".
Usa esempi intuitivi, controesempi, esperimenti mentali o paradossi
per aiutarlo a riconoscere autonomamente la contraddizione.

3. TONO

Mantieni uno stile:
- accogliente;
- incoraggiante;
- rigoroso;
- mai giudicante.

Usa un linguaggio adatto agli studenti delle superiori.

4. FORMATTAZIONE

Le risposte devono essere brevi:
massimo 2-3 paragrafi.

Ricorda che lo studente legge Athena dentro un piccolo widget Padlet.
"""


# ============================================================
# 4. CONTESTO DELLE COLONNE PADLET
# ============================================================

CONTESTI_COLONNE = {

"1": """
--- COLONNA 1: CHE COS'È L'INFINITO? ---

Focus:
- infinito potenziale;
- infinito attuale;
- differenza tra processo senza fine e insieme infinito;
- collegamenti filosofici con Leopardi.

Stimola la riflessione sulla natura dell'infinito.
""",


"2": """
--- COLONNA 2: ZENONE E I PARADOSSI DEL MOTO ---

Focus:
- Achille e la tartaruga;
- dicotomia;
- divisione infinita dello spazio;
- rapporto tra intuizione e matematica.

Aiuta lo studente a mettere in discussione l'idea
che una successione infinita di passi impedisca il movimento.
""",


"3": """
--- COLONNA 3: SERIE E SERIE DI BASILEA ---

Focus:
- somma infinita;
- convergenza;
- significato di una serie numerica.

Guida lo studente a superare l'idea intuitiva
che una somma con infiniti termini debba necessariamente essere infinita.
""",


"4": """
--- COLONNA 4: ESCHER E L'INFINITO VISIVO ---

Focus:
- tassellazioni;
- Circle Limit;
- geometria iperbolica;
- rappresentazione dell'infinito in uno spazio limitato.

Favorisci il collegamento tra matematica, arte e geometria.
""",


"5": """
--- COLONNA 5: ELABORATO FINALE ---

Focus:
- revisione del lavoro;
- organizzazione delle idee;
- autovalutazione.

Aiuta lo studente a migliorare il proprio elaborato
attraverso domande di riflessione.
"""

}


system_instruction_corrente = (
    SYSTEM_PROMPT_BASE
    + "\n\n"
    + CONTESTI_COLONNE.get(
        colonna_id,
        CONTESTI_COLONNE["1"]
    )
)


# ============================================================
# 5. CONFIGURAZIONE GEMINI
# ============================================================

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error(
        "⚠️ Chiave API Gemini non trovata nei Secrets di Streamlit."
    )
    st.stop()


client = genai.Client(api_key=api_key)


config = types.GenerateContentConfig(
    system_instruction=system_instruction_corrente
)


# ============================================================
# 6. GESTIONE SESSIONE CHAT
# ============================================================

if "chat_session" not in st.session_state:

    st.session_state.chat_session = client.chats.create(
        model="gemini-2.5-flash",
        config=config
    )


if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# 7. VISUALIZZAZIONE STORIA CHAT
# ============================================================

for message in st.session_state.messages:

    avatar = (
        "👤"
        if message["role"] == "user"
        else "🏛️"
    )

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):
        st.markdown(message["text"])


# ============================================================
# 8. INPUT STUDENTE E RISPOSTA ATHENA
# ============================================================

if prompt := st.chat_input(
    "Scrivi qui la tua riflessione o domanda ad Athena..."
):

    st.session_state.messages.append(
        {
            "role": "user",
            "text": prompt
        }
    )


    with st.chat_message(
        "user",
        avatar="👤"
    ):
        st.markdown(prompt)


    with st.chat_message(
        "assistant",
        avatar="🏛️"
    ):

        with st.spinner(
            "Athena sta riflettendo..."
        ):

            response = (
                st.session_state
                .chat_session
                .send_message(prompt)
            )


            answer = response.text


            st.markdown(answer)


            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "text": answer
                }
            )
