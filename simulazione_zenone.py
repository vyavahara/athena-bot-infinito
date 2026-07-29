import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ------------------------------------------------------------------------------
# CONFIGURAZIONE PAGINA
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Athena - Laboratorio Paradosso & Limiti",
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
        <p class="header-subtitle">Laboratorio didattico: dalla scomposizione spaziale alla convergenza della serie</p>
    </div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# CALCOLO DATI BASE
# ------------------------------------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 0

x0_a, x0_t, rapporto = 0.0, 100.0, 0.1
passi_data = []
a_pos, t_pos = float(x0_a), float(x0_t)

for i in range(15):
    distanza = t_pos - a_pos
    # Calcolo algebrico esatto Sn secondo la scheda UMI-SIS (100 * (1 - (1/10)^(i+1)) / (1 - 1/10))
    s_n_fattore = (1.0 - (rapporto ** (i + 1))) / (1.0 - rapporto)
    s_n_valore = 100.0 * s_n_fattore
    
    passi_data.append({
        "Passo (n)": int(i),
        "Posizione Achille (m)": float(round(a_pos, 4)),
        "Posizione Tartaruga (m)": float(round(t_pos, 4)),
        "Distacco Δs (m)": float(round(distanza, 4)),
        "Tratto d_n (m)": float(round(100.0 * (rapporto ** i), 4)),
        "Somma Parziale S_n (m)": float(round(s_n_valore, 6))
    })
    a_pos = t_pos
    t_pos = t_pos + (distanza * rapporto)

# ------------------------------------------------------------------------------
# SEZIONE 1: SIMULAZIONE SPAZIALE INTERATTIVA
# ------------------------------------------------------------------------------
st.subheader("1. Scomposizione Spaziale della Corsa")

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

# Marcatori storici con pedici HTML nativi
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
    height=320,
    margin=dict(l=20, r=20, t=20, b=20),
    plot_bgcolor="white"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ------------------------------------------------------------------------------
# SEZIONE 2: LABORATORIO INTERATTIVO SULLE SOMME PARZIALI S_n E SUL LIMITE
# ------------------------------------------------------------------------------
st.subheader("2. Laboratorio Algebrico: Andamento e Limite di S_n")

tab1, tab2 = st.tabs(["📈 Grafico di Convergenza di S_n", "🧮 Calcolatore Algebrico Guidato"])

with tab1:
    st.markdown("Esplora l'andamento della successione delle somme parziali $S_n$ al crescere del numero di termini $n$[cite: 1].")
    
    # Grafico di convergenza Plotly
    df_chart = pd.DataFrame(passi_data[:n+1])
    
    fig_limit = go.Figure()
    
    # Punti della successione
    fig_limit.add_trace(go.Scatter(
        x=df_chart["Passo (n)"],
        y=df_chart["Somma Parziale S_n (m)"],
        mode="lines+markers",
        name="S_n (Somma Parziale)",
        line=dict(color="#2563eb", width=3),
        marker=dict(size=8, color="#1e3a8a")
    ))
    
    # Asintoto Limite (111.1111 m)
    fig_limit.add_trace(go.Scatter(
        x=[0, 14], y=[111.1111, 111.1111],
        mode="lines",
        name="Limite S_∞ = 111.1̄ m",
        line=dict(color="#dc2626", width=2, dash="dash")
    ))
    
    fig_limit.update_layout(
        xaxis=dict(title="Numero di passi (n)", dtick=1),
        yaxis=dict(title="Distanza percorsa da Achille S_n (m)", range=[90, 115]),
        height=350,
        margin=dict(l=20, r=20, t=30, b=20),
        plot_bgcolor="#f8fafc"
    )
    
    st.plotly_chart(fig_limit, use_container_width=True)

with tab2:
    st.markdown("### Studio analitico dell'infinitesimo $\\frac{1}{10^n}$[cite: 1]")
    
    # Slider interattivo per testare grandi valori di n
    n_test = st.slider("Seleziona il valore di n per calcolare S_n:", min_value=1, max_value=20, value=n+1 if n>0 else 1)
    
    # Calcolo analitico dinamico
    termine_infinitesimo = 1 / (10 ** n_test)
    sn_calcolata = 100 * ((1 - termine_infinitesimo) / 0.9)
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric(label=f"Termine (1/10)^{n_test}", value=f"{termine_infinitesimo:.2e}")
    col_b.metric(label=f"Fattore [1 - (1/10)^{n_test}] / 0.9", value=f"{((1 - termine_infinitesimo)/0.9):.8f}")
    col_c.metric(label=f"Somma S_{n_test} (metri)", value=f"{sn_calcolata:.6f} m")
    
    st.markdown(f"""
    > **Osservazione Guidata**:  
    > Per $n = {n_test}$, la quantità $\\frac{{1}}{{10^{{{n_test}}}}}$ vale **{termine_infinitesimo:.2e}**[cite: 1].  
    > Man mano che $n \\to \\infty$, questo termine diventa trascurabile (tende a $0$), consentendo a $S_n$ di stabilizzarsi sul valore limite finito $100 \\cdot \\frac{{10}}{{9}} = 111,\\bar{{1}}\\text{{ m}}$[cite: 1].
    """)

st.markdown("---")

# ------------------------------------------------------------------------------
# SEZIONE 3: TABELLA DATI DINAMICA
# ------------------------------------------------------------------------------
st.subheader("3. Tabella della Successione S_n")

df_totale = pd.DataFrame(passi_data)
st.dataframe(
    df_totale.iloc[:n + 1],
    use_container_width=True,
    hide_index=True
)
