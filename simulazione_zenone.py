import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ------------------------------------------------------------------------------
# CONFIGURAZIONE PAGINA E CSS PERSONALIZZATO (Didattico)
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Athena - Paradosso di Elea (Didattico)",
    page_icon="🏛️",
    layout="wide"
)

# CSS per il box socratico e l'intestazione
st.markdown("""
    <style>
    .header-container {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        padding: 2.5rem 1.5rem;
        border-radius: 12px;
        text-align: center;
        color: #ffffff;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    .header-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.3;
        color: #ffffff;
    }
    .header-subtitle {
        font-size: 1.05rem;
        color: #cbd5e1;
        margin-top: 0.6rem;
        margin-bottom: 0;
        font-weight: 400;
    }
    /* Stile per il box socratico didattico */
    .socratic-box {
        background-color: #f8fafc;
        border-left: 6px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .socratic-title {
        color: #475569;
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 1rem;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 0.5rem;
    }
    .socratic-point {
        margin-bottom: 0.75rem;
        line-height: 1.6;
        color: #334155;
    }
    .socratic-point strong {
        color: #0f172a;
    }
    .socratic-question {
        margin-top: 1rem;
        padding-top: 0.75rem;
        border-top: 1px dashed #cbd5e1;
        color: #1e3a8a;
        font-weight: 500;
        font-style: italic;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# INTESTAZIONE
# ------------------------------------------------------------------------------
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🏛️ Athena: Guida Socratica al Paradosso di Elea</h1>
        <p class="header-subtitle">Laboratorio didattico di scomposizione logico-spaziale della corsa di Achille e la Tartaruga</p>
    </div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# DEFINIZIONE DEL CONTENUTO SOCRATICO DIDATTICO
# ------------------------------------------------------------------------------
# Questo dizionario contiene l'intero materiale educativo, indispensabile.
socratic_guidance = {
    0: {
        "titolo": "Passo 0: L'Impostazione del Paradosso",
        "punti": [
            "Osserva la situazione iniziale: la Tartaruga parte con un vantaggio (t0 = 100m).",
            "Achille parte da zero (a0 = 0m) ed è 10 volte più veloce.",
            "L'obiettivo di Achille è coprire la distanza d0 = 100m che lo separa dalla Tartaruga."
        ],
        "domanda": "Perché, pur essendo 10 volte più veloce, Achille non può vincere in questo singolo istante?"
    },
    1: {
        "titolo": "Passo 1: Il Primo Inseguimento",
        "punti": [
            "Achille ha corso e ha coperto la distanza d0 (100m). Arriva dove era la Tartaruga (t0).",
            "Ma mentre Achille correva, la Tartaruga si è mossa, coprendo d1 (10m).",
            "Il nuovo distacco tra i due è ora di 10 metri (Δs = 10m)."
        ],
        "domanda": "Come ha fatto un distacco di 100m a ridursi a soli 10m? Achille si è avvicinato, ma ha cancellato il vantaggio?"
    },
    2: {
        "titolo": "Passo 2: Il Divario si Assottiglia",
        "punti": [
            "Achille riprende l'inseguimento, coprendo i 10m della distanza d1. Arriva a a2=110m (dove era la t1).",
            "Nel frattempo, la Tartaruga ha coperto la sua d2 (1m).",
            "Il distacco ora è minuscolo, solo 1 metro (Δs = 1m).",
            "Possiamo vedere chiaramente i marcatori delle posizioni storiche A0, A1, A2 sull'asse spaziale."
        ],
        "domanda": "Il distacco si riduce sempre del 90%. È una 'perdita di tempo' o un 'avvicinamento reale'?"
    },
    3: {
        "titolo": "Passo 3: La Micro-Scomposizione",
        "punti": [
            "La distanza d2 (1m) è stata coperta da Achille. Ma la Tartaruga si è mossa di d3 (0.1m).",
            "Il distacco è ora di soli 10 centimetri (Δs = 0.1m).",
            "A questo punto, lo spazio tra Achille e la Tartaruga è visibile nel grafico come un piccolo intervallo blu.",
            "I marcatori delle posizioni storiche (A0, A1, A2, A3) si stanno affollando sull'asse."
        ],
        "domanda": "Questi marcatori sono infiniti? Possiamo davvero contare un numero infinito di tappe in un tempo finito?"
    },
    4: {
        "titolo": "Passo 4: Il Confine dei Sensi e della Logica",
        "punti": [
            "Il distacco si riduce ulteriormente a 1 centimetro (Δs = 0.01m).",
            "L'intervallo spaziale è quasi invisibile. Gli occhi faticano a distinguerli.",
            "Matematicamente, il distacco è ancora presente e non è zero."
        ],
        "domanda": "Se non riusciamo a vederlo con gli occhi, esiste davvero un distacco? Di chi ci fidiamo, dei sensi o della logica?"
    },
    # ... Aggiungere altri passi qui per l'intervallo completo n < 10 ...
}

# ------------------------------------------------------------------------------
# GESTIONE STATO SIMULAZIONE (Semplificata, solo n)
# ------------------------------------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 0

# ------------------------------------------------------------------------------
# PARAMETRI DEL MODELLO E DATI
# ------------------------------------------------------------------------------
# Calcolo deterministico, non serve memorizzare tutto nello stato
x0_achille = 0.0
x0_tartaruga = 100.0  # Vantaggio iniziale (m)
rapporto = 0.1        # Achille 10 volte più veloce

passi_data = []
a_pos = x0_achille
t_pos = x0_tartaruga

for i in range(15):
    distanza = t_pos - a_pos
    passi_data.append({
        "Passo (n)": i,
        "Posizione Achille (m)": round(a_pos, 4),
        "Posizione Tartaruga (m)": round(t_pos, 4),
        "Distacco Δs (m)": round(distanza, 4)
    })
    # Avanzamento
    a_pos = t_pos
    t_pos = t_pos + (distanza * rapporto)

# ------------------------------------------------------------------------------
# CONTROLLI SIMULAZIONE
# ------------------------------------------------------------------------------
col_ctrl1, col_ctrl2, _ = st.columns([1, 1, 4])

with col_ctrl1:
    if st.button("⬅️ Passo Precedente", use_container_width=True):
        if st.session_state.step > 0:
            st.session_state.step -= 1

with col_ctrl2:
    if st.button("Passo Successivo ➡️", use_container_width=True):
        if st.session_state.step < 10:
            st.session_state.step += 1

n = st.session_state.step

# ------------------------------------------------------------------------------
# COSTRUZIONE GRAFICO PLOTLY CON SOLUZIONE ANTI-SOVRAPPOSIZIONE
# ------------------------------------------------------------------------------
# Estrai dati specifici per il passo n
curr_a = passi_data[n]["Posizione Achille (m)"]
curr_t = passi_data[n]["Posizione Tartaruga (m)"]
curr_dist = passi_data[n]["Distacco Δs (m)"]

fig = go.Figure()

# 1. Asse spaziale di riferimento
fig.add_trace(go.Scatter(
    x=[-5, 120], y=[0, 0],
    mode="lines",
    line=dict(color="#cbd5e1", width=4),
    showlegend=False,
    hoverinfo="none"
))

# 2. Marcatori storici e SOLUZIONE ANTI-SOVRAPPOSIZIONE
# Lo "staggering" verticale è dinamico e adattivo
for i in range(n + 1):
    pos_a = passi_data[i]["Posizione Achille (m)"]

    # Calcolo dello staggering verticale dinamico (y_offset)
    # L'idea è che più la distanza attuale (curr_dist) è piccola,
    # più le etichette storiche "scendono", liberando spazio.
    # Usiamo una formula esponenziale o lineare adattiva.
    
    # y_offset di base (-0.3)
    y_base_offset = -0.3
    # Fattore adattivo che fa scendere le etichette quando la distanza si riduce
    y_adaptive_offset = max(-1.0, -0.1 * (4 - i) + (curr_dist / 20))

    # Alternanza di base per ordine visivo
    y_stagger = -0.05 if (i % 2 == 0) else -0.1
    y_final_offset = y_base_offset + y_adaptive_offset + y_stagger

    # Etichetta formattata (unificata A_i = T_i-1)
    label_text = f"A₀" if i == 0 else f"A_{i} = T_{i-1}"
    
    # Punto sull'asse
    fig.add_trace(go.Scatter(
        x=[pos_a], y=[0],
        mode="markers",
        marker=dict(color="#1e3a8a", size=8),
        showlegend=False,
        hoverinfo="text",
        text=f"Passo {i}: {pos_a} m"
    ))
    
    # Etichetta sotto l'asse (posizionata con y_final_offset)
    fig.add_annotation(
        x=pos_a, y=y_final_offset,
        text=f"| {label_text}",
        showarrow=False,
        font=dict(size=12, color="#334155")
    )

# 3. Visualizzazione dello spazio d'avanzamento corrente
if n > 0:
    prev_a = passi_data[n-1]["Posizione Achille (m)"]
    fig.add_trace(go.Scatter(
        x=[prev_a, curr_a], y=[0.15, 0.15],
        mode="lines+markers",
        line=dict(color="#2563eb", width=3),
        marker=dict(size=6, color="#2563eb"),
        name=f"Tratto d_{n}",
        showlegend=False
    ))

# 4. Icone ( Achille e Tartaruga)
fig.add_trace(go.Scatter(
    x=[curr_a], y=[0.4],
    mode="text",
    text=["🏃 Achille"],
    textposition="top right",
    font=dict(size=16),
    showlegend=False
))

fig.add_trace(go.Scatter(
    x=[curr_t], y=[0.4],
    mode="text",
    text=["🐢 Tartaruga"],
    textposition="top right",
    font=dict(size=16),
    showlegend=False
))

fig.update_layout(
    xaxis=dict(range=[-5, 120], zeroline=False, showgrid=False, title="Spazio (metri)"),
    yaxis=dict(range=[-1.2, 1.2], zeroline=False, showgrid=False, showticklabels=False),
    height=320,
    margin=dict(l=20, r=20, t=30, b=20),
    plot_bgcolor="white"
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------------------------
# VISUALIZZAZIONE DEL CONTENUTO SOCRATICO DIDATTICO (REINSERITO)
# ------------------------------------------------------------------------------
# Questo è il box indispensabile per la didattica
if n in socratic_guidance:
    guidance = socratic_guidance[n]
    
    st.markdown(f"""
        <div class="socratic-box">
            <div class="socratic-title">{guidance['titolo']}</div>
            {"".join(f'<p class="socratic-point">• {point}</p>' for point in guidance['punti'])}
            <p class="socratic-question">🤔 Domanda Socratica: {guidance['domanda']}</p>
        </div>
    """, unsafe_allow_html=True)
else:
    # Caso di riserva se il passo non è definito
    st.info(f"Visualizzazione didattica per il passo {n} non ancora definita.")

st.markdown("---")

# ------------------------------------------------------------------------------
# TABELLA DATI DINAMICA
# ------------------------------------------------------------------------------
st.subheader("TABELLA")

df_totale = pd.DataFrame(passi_data)
df_visibile = df_totale.iloc[:n+1].copy()

st.dataframe(
    df_visibile,
    use_container_width=True,
    hide_index=True
)
