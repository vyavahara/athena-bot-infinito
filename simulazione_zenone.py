import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ------------------------------------------------------------------------------
# CONFIGURAZIONE PAGINA & CSS DIDATTICO
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Athena - Paradosso di Elea",
    page_icon="🏛️",
    layout="wide"
)

st.markdown("""
    <style>
    .header-container {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        padding: 2.2rem 1.5rem;
        border-radius: 12px;
        text-align: center;
        color: #ffffff;
        margin-bottom: 1.8rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    .header-title {
        font-size: 2.1rem;
        font-weight: 700;
        margin: 0;
        color: #ffffff;
    }
    .header-subtitle {
        font-size: 1.05rem;
        color: #cbd5e1;
        margin-top: 0.5rem;
        margin-bottom: 0;
        font-weight: 400;
    }
    .socratic-card {
        background-color: #f8fafc;
        border-left: 5px solid #2563eb;
        border-radius: 8px;
        padding: 1.25rem 1.5rem;
        margin: 1.2rem 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    }
    .socratic-title {
        color: #1e293b;
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }
    .socratic-text {
        color: #334155;
        font-size: 0.98rem;
        line-height: 1.5;
        margin-bottom: 0.5rem;
    }
    .socratic-question {
        margin-top: 0.8rem;
        padding-top: 0.6rem;
        border-top: 1px dashed #cbd5e1;
        color: #1e3a8a;
        font-weight: 600;
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
# GUIDA SOCRATICA DIDATTICA
# ------------------------------------------------------------------------------
guida_socratica = {
    0: {
        "titolo": "Passo 0: Il Contesto Iniziale",
        "punti": [
            "La Tartaruga parte con un vantaggio iniziale di 100 metri (T₀ = 100 m).",
            "Achille parte dall'origine (A₀ = 0 m) ed è 10 volte più veloce della tartaruga.",
            "Per raggiungere la tartaruga, Achille deve prima percorrere la distanza che li separa."
        ],
        "domanda": "Se Achille corre più veloce, perché non raggiunge subito la tartaruga?"
    },
    1: {
        "titolo": "Passo 1: Il Primo Raggiungimento (A₁ = T₀)",
        "punti": [
            "Achille corre fino al punto A₁ = 100 m, occupando la posizione iniziale della tartaruga.",
            "Nello stesso tempo, la tartaruga è avanzata del 10% della distanza, arrivando a T₁ = 110 m.",
            "Il distacco Δs si è ridotto da 100 m a 10 m."
        ],
        "domanda": "Achille ha annullato il distacco o lo ha solo ridotto?"
    },
    2: {
        "titolo": "Passo 2: La Riduzione Scalare (A₂ = T₁)",
        "punti": [
            "Achille copre i 10 metri arrivando a A₂ = 110 m.",
            "La tartaruga avanza ulteriormente di 1 metro, raggiungendo T₂ = 111 m.",
            "Il distacco residuale è ora di solo 1 metro (Δs = 1 m)."
        ],
        "domanda": "Il numero di passaggi necessari per annullare il distacco è finito o infinito?"
    },
    3: {
        "titolo": "Passo 3: La Scomposizione dell'Infinitesimo",
        "punti": [
            "Achille raggiunge A₃ = 111 m.",
            "La tartaruga si trova a T₃ = 111.1 m. Il distacco è di 0.1 metri (10 cm).",
            "I punti di arresto si concentrano sempre più nello spazio."
        ],
        "domanda": "Se dividiamo lo spazio in infiniti intervalli, il tempo impiegato diventa anch'esso infinito?"
    },
    4: {
        "titolo": "Passo 4: Il Limite della Percezione",
        "punti": [
            "Achille giunge a A₄ = 111.1 m. La tartaruga è a T₄ = 111.11 m (distacco: 1 cm).",
            "I punti sull'asse sono visivamente vicinissimi, ma la relazione matematica resta invariata."
        ],
        "domanda": "La ragione ci dice che la tartaruga è avanti, i sensi ci dicono che sono insieme: a chi credere?"
    }
}

# ------------------------------------------------------------------------------
# INIZIALIZZAZIONE E CALCOLO DATI
# ------------------------------------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 0

x0_a, x0_t, rapporto = 0.0, 100.0, 0.1
passi_data = []
a_pos, t_pos = float(x0_a), float(x0_t)

for i in range(15):
    distanza = t_pos - a_pos
    passi_data.append({
        "Passo (n)": int(i),
        "Posizione Achille (m)": float(round(a_pos, 4)),
        "Posizione Tartaruga (m)": float(round(t_pos, 4)),
        "Distacco Δs (m)": float(round(distanza, 4))
    })
    a_pos = t_pos
    t_pos = t_pos + (distanza * rapporto)

# ------------------------------------------------------------------------------
# CONTROLLI SIMULAZIONE
# ------------------------------------------------------------------------------
col_c1, col_c2, _ = st.columns([1, 1, 4])

with col_c1:
    if st.button("⬅️ Passo Precedente", use_container_width=True):
        if st.session_state.step > 0:
            st.session_state.step -= 1

with col_c2:
    if st.button("Passo Successivo ➡️", use_container_width=True):
        if st.session_state.step < 10:
            st.session_state.step += 1

n = st.session_state.step

# ------------------------------------------------------------------------------
# GRAFICO PLOTLY ANTI-SOVRAPPOSIZIONE
# ------------------------------------------------------------------------------
curr_a = passi_data[n]["Posizione Achille (m)"]
curr_t = passi_data[n]["Posizione Tartaruga (m)"]
dist_attuale = passi_data[n]["Distacco Δs (m)"]

fig = go.Figure()

# Asse principale
fig.add_trace(go.Scatter(
    x=[-5, 120], y=[0, 0],
    mode="lines",
    line=dict(color="#cbd5e1", width=4),
    showlegend=False,
    hoverinfo="none"
))

# Punti storici A_i con staggering dinamico delle etichette
for i in range(n + 1):
    pos_a = passi_data[i]["Posizione Achille (m)"]
    
    # Sfalsamento verticale alternato a 3 livelli per evitare sovrapposizioni nei punti vicini
    offsets = [-0.35, -0.65, -0.95]
    y_off = offsets[i % 3]
    
    label_text = "A₀" if i == 0 else f"A_{i}=T_{i-1}"

    # Punto
    fig.add_trace(go.Scatter(
        x=[pos_a], y=[0],
        mode="markers",
        marker=dict(color="#1e3a8a", size=7),
        showlegend=False,
        hoverinfo="text",
        text=f"Passo {i}: {pos_a} m"
    ))

    # Etichetta
    fig.add_annotation(
        x=pos_a, y=y_off,
        text=f"| {label_text}",
        showarrow=False,
        font=dict(size=11, color="#334155")
    )

# Tratto d'avanzamento corrente
if n > 0:
    prev_a = passi_data[n - 1]["Posizione Achille (m)"]
    fig.add_trace(go.Scatter(
        x=[prev_a, curr_a], y=[0.15, 0.15],
        mode="lines+markers",
        line=dict(color="#2563eb", width=3),
        marker=dict(size=6, color="#2563eb"),
        showlegend=False,
        hoverinfo="none"
    ))

# Posizionamento verticale disaccoppiato per evitare sovrapposizione tra Achille e Tartaruga
y_achille = 0.45
y_tartaruga = 0.75 if dist_attuale < 15.0 else 0.45

# Icona Achille
fig.add_annotation(
    x=curr_a, y=y_achille,
    text="🏃 Achille",
    showarrow=False,
    font=dict(size=15, color="#0f172a"),
    xanchor="center"
)

# Icona Tartaruga
fig.add_annotation(
    x=curr_t, y=y_tartaruga,
    text="🐢 Tartaruga",
    showarrow=False,
    font=dict(size=15, color="#0f172a"),
    xanchor="center"
)

fig.update_layout(
    xaxis=dict(range=[-5, 120], zeroline=False, showgrid=False, title="Spazio (metri)"),
    yaxis=dict(range=[-1.3, 1.1], zeroline=False, showgrid=False, showticklabels=False),
    height=340,
    margin=dict(l=20, r=20, t=20, b=20),
    plot_bgcolor="white"
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------------------------
# RENDER BOX SOCRATICO
# ------------------------------------------------------------------------------
info = guida_socratica.get(n, {
    "titolo": f"Passo {n}: Iterazione Avanzata",
    "punti": [f"Posizione Achille: {curr_a} m", f"Posizione Tartaruga: {curr_t} m", f"Distacco attuale: {dist_attuale} m"],
    "domanda": "Come si comporta la somma infinita di questi segmenti di spazio?"
})

st.markdown(f"""
    <div class="socratic-card">
        <div class="socratic-title">{info['titolo']}</div>
        {"".join([f'<div class="socratic-text">• {p}</div>' for p in info['punti']])}
        <div class="socratic-question">🤔 Riflessione Socratica: {info['domanda']}</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# ------------------------------------------------------------------------------
# TABELLA DATI DINAMICA
# ------------------------------------------------------------------------------
st.subheader("TABELLA")

df_totale = pd.DataFrame(passi_data)
st.dataframe(
    df_totale.iloc[:n + 1],
    use_container_width=True,
    hide_index=True
)
