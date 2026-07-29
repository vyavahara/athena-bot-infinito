import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ------------------------------------------------------------------------------
# CONFIGURAZIONE PAGINA
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Athena - Paradosso di Elea",
    page_icon="🏛️",
    layout="wide"
)

# ------------------------------------------------------------------------------
# CSS PERSONALIZZATO (Intestazione & Layout)
# ------------------------------------------------------------------------------
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
        letter-spacing: -0.01em;
        color: #ffffff;
    }
    .header-subtitle {
        font-size: 1.05rem;
        color: #cbd5e1;
        margin-top: 0.6rem;
        margin-bottom: 0;
        font-weight: 400;
        line-height: 1.5;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# INTESTAZIONE FORMATTATA
# ------------------------------------------------------------------------------
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🏛️ Athena: Guida Socratica al Paradosso di Elea</h1>
        <p class="header-subtitle">Laboratorio didattico di scomposizione logico-spaziale della corsa di Achille e la Tartaruga</p>
    </div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# INIZIALIZZAZIONE STATO
# ------------------------------------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 0

# ------------------------------------------------------------------------------
# PARAMETRI INIZIALI
# ------------------------------------------------------------------------------
x0_achille = 0.0
x0_tartaruga = 100.0  # Vantaggio iniziale della tartaruga (m)
rapporto = 0.1        # Achille è 10 volte più veloce

# Calcolo posizioni teoriche
passi_data = []
a_pos = float(x0_achille)
t_pos = float(x0_tartaruga)

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
    t_pos = t_pos + distanza * rapporto

# ------------------------------------------------------------------------------
# CONTROLLI SIMULAZIONE
# ------------------------------------------------------------------------------
col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([1, 1, 4])

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
# RENDERING GRAFICO
# ------------------------------------------------------------------------------
curr_a = float(passi_data[n]["Posizione Achille (m)"])
curr_t = float(passi_data[n]["Posizione Tartaruga (m)"])

fig = go.Figure()

# Asse di riferimento
fig.add_trace(go.Scatter(
    x=[0, 120], y=[0, 0],
    mode="lines",
    line=dict(color="#cbd5e1", width=4),
    showlegend=False,
    hoverinfo="none"
))

# Segnalini storici e sfalsamento etichette
for i in range(n + 1):
    pos_a = float(passi_data[i]["Posizione Achille (m)"])
    
    # Sfalsamento verticale alternato
    y_offset = -0.35 if (i % 2 == 0) else -0.65
    
    # Etichetta formattata
    label_text = "A₀" if i == 0 else f"A_{i} = T_{i-1}"
    
    # Punto sull'asse
    fig.add_trace(go.Scatter(
        x=[pos_a], y=[0],
        mode="markers",
        marker=dict(color="#1e3a8a", size=8),
        showlegend=False,
        hoverinfo="text",
        text=f"Passo {i}: {pos_a} m"
    ))
    
    # Etichetta del punto
    fig.add_annotation(
        x=pos_a, y=y_offset,
        text=f"| {label_text}",
        showarrow=False,
        font=dict(size=12, color="#334155")
    )

# Visualizzazione segmento d'avanzamento corrente
if n > 0:
    prev_a = float(passi_data[n-1]["Posizione Achille (m)"])
    fig.add_trace(go.Scatter(
        x=[prev_a, curr_a], y=[0.15, 0.15],
        mode="lines+markers",
        line=dict(color="#2563eb", width=3),
        marker=dict(size=8, color="#2563eb"),
        name=f"Tratto d_{n}",
        showlegend=False
    ))

# Marker Achille (corretto senza proprietà non valide)
fig.add_trace(go.Scatter(
    x=[curr_a], y=[0.4],
    mode="text",
    text=["🏃 Achille"],
    textposition="top center",
    font=dict(size=16),
    showlegend=False
))

# Marker Tartaruga (corretto senza proprietà non valide)
fig.add_trace(go.Scatter(
    x=[curr_t], y=[0.4],
    mode="text",
    text=["🐢 Tartaruga"],
    textposition="top center",
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

st.markdown("---")

# ------------------------------------------------------------------------------
# TABELLA DINAMICA
# ------------------------------------------------------------------------------
st.subheader("TABELLA")

df_totale = pd.DataFrame(passi_data)
df_visibile = df_totale.iloc[:n+1].copy()

st.dataframe(
    df_visibile,
    use_container_width=True,
    hide_index=True
)
