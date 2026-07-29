import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ------------------------------------------------------------------------------
# CONFIGURAZIONE PAGINA
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Athena - Paradosso di Elea & Il Limite",
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
        <p class="header-subtitle">Laboratorio didattico: dalla scomposizione spaziale alla somma di infiniti termini</p>
    </div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# CALCOLO DATI E INIZIALIZZAZIONE
# ------------------------------------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 0

x0_a, x0_t, rapporto = 0.0, 100.0, 0.1
passi_data = []
a_pos, t_pos = float(x0_a), float(x0_t)

for i in range(15):
    distanza = t_pos - a_pos
    # Calcolo della somma parziale S_n per il fattore tra parentesi (1 + 1/10 + ...)
    s_n_fattore = (1.0 - (rapporto ** (i + 1))) / (1.0 - rapporto) if i >= 0 else 1.0
    
    passi_data.append({
        "Passo (n)": int(i),
        "Posizione Achille (m)": float(round(a_pos, 4)),
        "Posizione Tartaruga (m)": float(round(t_pos, 4)),
        "Distacco Δs (m)": float(round(distanza, 4)),
        "Somma Parziale S_n (m)": float(round(100 * s_n_fattore, 4))
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
# GRAFICO PLOTLY CON PEDICI FORMATTATI IN HTML
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

# Marcatori ed etichette storiche con pedici HTML nativi
for i in range(n + 1):
    pos_a = passi_data[i]["Posizione Achille (m)"]
    label_html = "A<sub>0</sub>" if i == 0 else f"A<sub>{i}</sub> = T<sub>{i-1}</sub>"
    y_off = -0.35 if (i % 2 == 0) else -0.75

    fig.add_trace(go.Scatter(
        x=[pos_a], y=[0],
        mode="markers",
        marker=dict(color="#1e3a8a", size=7),
        showlegend=False,
        hoverinfo="text",
        text=f"Passo {i}: {pos_a} m"
    ))

    x_anchor_val = "center"
    if i >= 3 and (i == n or i == n - 1):
        x_anchor_val = "left" if (i % 2 == 0) else "right"

    fig.add_annotation(
        x=pos_a, y=y_off,
        text=f"| {label_html}",
        showarrow=False,
        xanchor=x_anchor_val,
        font=dict(size=11, color="#334155")
    )

# Segmento d'avanzamento corrente
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

# Posizionamento verticale non sovrapposto
y_achille = 0.40
y_tartaruga = 0.70 if dist_attuale < 12.0 else 0.40

fig.add_annotation(
    x=curr_a, y=y_achille, text="🏃 Achille",
    showarrow=False, font=dict(size=14, color="#0f172a"), xanchor="center"
)

fig.add_annotation(
    x=curr_t, y=y_tartaruga, text="🐢 Tartaruga",
    showarrow=False, font=dict(size=14, color="#0f172a"), xanchor="center"
)

fig.update_layout(
    xaxis=dict(range=[-5, 120], zeroline=False, showgrid=False, title="Spazio (metri)"),
    yaxis=dict(range=[-1.1, 1.0], zeroline=False, showgrid=False, showticklabels=False),
    height=330,
    margin=dict(l=20, r=20, t=20, b=20),
    plot_bgcolor="white"
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------------------------
# FORMALIZZAZIONE MATEMATICA E GUIDA SOCRATICA (Scheda Liceo Matematico)
# ------------------------------------------------------------------------------
st.markdown("### 📐 Formalizzazione Matematica: La Serie delle Somme Parziali")

col_mat1, col_mat2 = st.columns([1, 1])

with col_mat1:
    st.markdown("""
    La distanza totale percorsa da Achille per raggiungere la tartaruga si esprime come somma di infiniti tratti rettilinei:
    $$S = 100 + 10 + 1 + \\frac{1}{10} + \\frac{1}{100} + \\dots + \\frac{1}{10^n} + \\dots$$
    
    Raccogliendo il vantaggio iniziale $100\\text{ m}$:
    $$S = 100 \\cdot \\left(1 + \\frac{1}{10} + \\frac{1}{100} + \\dots + \\frac{1}{10^{n-1}} + \\dots\\right)$$
    """)

with col_mat2:
    st.markdown("""
    Calcoliamo la successione delle somme parziali $S_n$ per l'espressione tra parentesi:
    $$(1 - \\frac{1}{10})S_n = 1 - \\frac{1}{10^n} \\implies S_n = \\frac{1 - \\frac{1}{10^n}}{1 - \\frac{1}{10}}$$
    
    Quando $n \\to \\infty$, il termine $\\frac{1}{10^n} \\to 0$. Pertanto:
    $$\\lim_{n \\to \\infty} S_n = \\frac{1}{1 - \\frac{1}{10}} = \\frac{10}{9}$$
    """)

# Esito numerico finale
st.success(f"**Risultato del Limite**: Achille raggiunge la Tartaruga a $100 \\cdot \\frac{{10}}{{9}} = 111,\\bar{{1}}\\text{{ metri}}$. La somma di infiniti termini è finita!")

st.markdown("---")

# ------------------------------------------------------------------------------
# TABELLA DATI DINAMICA
# ------------------------------------------------------------------------------
st.subheader("📊 Successione delle Somme Parziali S_n")

df_totale = pd.DataFrame(passi_data)
st.dataframe(
    df_totale.iloc[:n + 1],
    use_container_width=True,
    hide_index=True
)
