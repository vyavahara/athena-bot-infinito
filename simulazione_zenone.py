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
        color: #ffffff;
    }
    .header-subtitle {
        font-size: 1.05rem;
        color: #cbd5e1;
        margin-top: 0.6rem;
        margin-bottom: 0;
        font-weight: 400;
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
# GESTIONE STATO E GENERAZIONE DATI
# ------------------------------------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 0

# Parametri modello
x0_achille = 0.0
x0_tartaruga = 100.0
rapporto = 0.1

passi_data = []
a_pos = float(x0_achille)
t_pos = float(x0_tartaruga)

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
# COSTRUZIONE GRAFICO PLOTLY
# ------------------------------------------------------------------------------
curr_a = float(passi_data[n]["Posizione Achille (m)"])
curr_t = float(passi_data[n]["Posizione Tartaruga (m)"])

fig = go.Figure()

# 1. Asse di riferimento principale
fig.add_trace(go.Scatter(
    x=[-5, 120],
    y=[0.0, 0.0],
    mode="lines",
    line=dict(color="#cbd5e1", width=4),
    showlegend=False,
    hoverinfo="none"
))

# 2. Marcatori e annotazioni dei passi storici (A_i)
for i in range(n + 1):
    pos_a = float(passi_data[i]["Posizione Achille (m)"])
    y_offset = -0.35 if (i % 2 == 0) else -0.65
    label_text = "A₀" if i == 0 else f"A_{i} = T_{i-1}"

    # Punto sull'asse
    fig.add_trace(go.Scatter(
        x=[pos_a],
        y=[0.0],
        mode="markers",
        marker=dict(color="#1e3a8a", size=8),
        showlegend=False,
        hoverinfo="text",
        text=f"Passo {i}: {pos_a} m"
    ))

    # Etichetta sotto l'asse
    fig.add_annotation(
        x=pos_a,
        y=y_offset,
        text=f"| {label_text}",
        showarrow=False,
        font=dict(size=12, color="#334155")
    )

# 3. Tratto di avanzamento per il passo corrente
if n > 0:
    prev_a = float(passi_data[n - 1]["Posizione Achille (m)"])
    fig.add_trace(go.Scatter(
        x=[prev_a, curr_a],
        y=[0.15, 0.15],
        mode="lines+markers",
        line=dict(color="#2563eb", width=3),
        marker=dict(size=6, color="#2563eb"),
        showlegend=False,
        hoverinfo="none"
    ))

# 4. Marker di Achille e Tartaruga (tramite add_annotation per stabilità assoluta)
fig.add_annotation(
    x=curr_a,
    y=0.4,
    text="🏃 Achille",
    showarrow=False,
    font=dict(size=16, color="#0f172a"),
    yshift=10
)

fig.add_annotation(
    x=curr_t,
    y=0.4,
    text="🐢 Tartaruga",
    showarrow=False,
    font=dict(size=16, color="#0f172a"),
    yshift=10
)

fig.update_layout(
    xaxis=dict(range=[-5, 120], zeroline=False, showgrid=False, title="Spazio (metri)"),
    yaxis=dict(range=[-1.0, 1.0], zeroline=False, showgrid=False, showticklabels=False),
    height=320,
    margin=dict(l=20, r=20, t=30, b=20),
    plot_bgcolor="white"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ------------------------------------------------------------------------------
# TABELLA DATI
# ------------------------------------------------------------------------------
st.subheader("TABELLA")

df_visibile = pd.DataFrame(passi_data[:n + 1])

st.dataframe(
    df_visibile,
    use_container_width=True,
    hide_index=True
)
