from fractions import Fraction
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ------------------------------------------------------------------------------
# CONFIGURAZIONE PAGINA
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Simulazione del Paradosso di Achille e la tartaruga",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------------------
# CSS PERSONALIZZATO (Stile Moderno, Contrasto Elevato e Font Maggiorati)
# ------------------------------------------------------------------------------
st.markdown(
    """
<style>
    .main { background-color: #f1f5f9; }
    .stApp { font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    
    .block-container { padding-top: 1rem !important; padding-bottom: 1.2rem !important; }
    div[data-testid="stVerticalBlock"] { gap: 0.8rem !important; }
    p { margin-bottom: 0.4rem !important; line-height: 1.5; font-size: 1.02rem !important; }
    
    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e3c72 50%, #2a5298 100%);
        color: #ffffff; 
        padding: 20px 24px; 
        border-radius: 12px;
        text-align: center; 
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 80px;
    }
    .hero-banner h1 { 
        color: #ffffff !important; 
        font-weight: 800 !important; 
        font-size: 1.85rem !important; 
        margin: 0 !important; 
        line-height: 1.25;
        letter-spacing: -0.5px;
    }
    
    /* Condizioni Iniziali */
    .init-conditions-card {
        background-color: #ffffff; 
        border: 1px solid #cbd5e1;
        border-left: 6px solid #0284c7; 
        border-radius: 8px;
        padding: 12px 18px; 
        margin-bottom: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }
    .init-conditions-card h4 { 
        color: #0f172a; 
        margin-top: 0; 
        margin-bottom: 6px; 
        font-size: 1.08rem !important; 
        font-weight: 700; 
    }
    .init-conditions-text {
        display: flex; 
        justify-content: space-around; 
        align-items: center; 
        flex-wrap: wrap; 
        gap: 12px; 
        font-size: 1.02rem !important;
        color: #334155;
    }
    
    /* Card Athena */
    .athena-socratic-card {
        background-color: #ffffff; 
        border: 1px solid #cbd5e1;
        border-left: 6px solid #1e3c72; 
        border-radius: 8px;
        padding: 16px 18px; 
        height: 100%;
        box-shadow: 0 3px 8px rgba(0,0,0,0.04);
    }
    .athena-socratic-card h3 { 
        color: #1e3c72; 
        font-size: 1.2rem !important; 
        margin-top: 0; 
        margin-bottom: 8px; 
        font-weight: 700;
    }
    
    /* Sezioni Titoli */
    .section-title {
        color: #0f172a; 
        font-weight: 800; 
        font-size: 1.22rem !important;
        margin-top: 16px; 
        margin-bottom: 6px;
    }
    .section-subtitle {
        color: #475569; 
        font-weight: 600; 
        font-size: 1.02rem !important;
        margin-top: 0px; 
        margin-bottom: 12px;
    }
    
    /* Frazioni Badge */
    .fraction-badge {
        background-color: #e2e8f0; 
        border: 1px solid #94a3b8;
        padding: 2px 7px; 
        border-radius: 5px; 
        font-family: monospace;
        font-size: 0.98rem !important; 
        font-weight: bold; 
        color: #0f172a;
    }
    
    /* Focus Box */
    .cognitive-conflict-box {
        background-color: #fffbeb; 
        border: 1px solid #fde68a;
        border-left: 6px solid #f59e0b; 
        padding: 12px 16px;
        border-radius: 8px; 
        margin-top: 12px;
        box-shadow: 0 2px 5px rgba(245, 158, 11, 0.08);
    }
    .cognitive-conflict-box h4 { 
        color: #b45309; 
        margin-top: 0; 
        margin-bottom: 4px; 
        font-size: 1.05rem !important; 
        font-weight: 800; 
    }
    .conflict-text { 
        color: #78350f; 
        font-weight: 600; 
        font-size: 1.02rem !important; 
        line-height: 1.45; 
    }

    /* Streamlit Components Font Size */
    div[data-testid="stDataFrame"] { font-size: 0.95rem !important; }
    [data-testid="stMetricValue"] { font-size: 1.35rem !important; font-weight: 800 !important; color: #0f172a; }
    [data-testid="stMetricLabel"] { font-size: 0.98rem !important; font-weight: 600 !important; color: #475569; }
</style>
""",
    unsafe_allow_html=True,
)


# ------------------------------------------------------------------------------
# FUNZIONI DI UTILITÀ
# ------------------------------------------------------------------------------
def to_subscript(text: str) -> str:
    """Sostituisce le cifre e la lettera 'n' con le corrispettive Unicode a pedice."""
    sub_map = str.maketrans("0123456789n", "₀₁₂₃₄₅₆₇₈₉ₙ")
    return str(text).translate(sub_map)


def format_frac_html(f: Fraction) -> str:
    """Rende le frazioni esatte in modo chiaro e leggibile."""
    if f.denominator == 1:
        return f"{f.numerator}"
    return f"{f.numerator}/{f.denominator}"


# ------------------------------------------------------------------------------
# INTESTAZIONE
# ------------------------------------------------------------------------------
st.markdown(
    """
<div class="hero-banner">
    <h1>Simulazione del Paradosso di Achille e la tartaruga</h1>
</div>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------------------
# SIDEBAR - PARAMETRI GEOMETRICI
# ------------------------------------------------------------------------------
st.sidebar.header("⚙️ Impostazione della Pista")
d0_val = st.sidebar.number_input(
    "Misura del vantaggio iniziale d₁ = m(A₀T₀) [metri]:",
    value=100,
    step=10,
    min_value=1,
)
r_denom = st.sidebar.number_input(
    "Rapporto di contrazione relazionale (1/k):",
    value=10,
    min_value=2,
    max_value=100,
    step=1,
)
max_steps = st.sidebar.slider(
    "Numero di suddivisioni logiche da esplorare (n):",
    min_value=1,
    max_value=15,
    value=10,
)

# Gestione Stato Navigazione
if "step" not in st.session_state:
    st.session_state.step = 0

col_btn1, col_btn2, col_btn3, _ = st.columns([1.2, 1.2, 1.2, 2.4])
with col_btn1:
    if st.button("⏮️ Stato Iniziale (n = 0)"):
        st.session_state.step = 0
with col_btn2:
    if st.button("◀️ Passo Precedente") and st.session_state.step > 0:
        st.session_state.step -= 1
with col_btn3:
    if st.button("▶️ Passo Successivo") and st.session_state.step < max_steps:
        st.session_state.step += 1

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Passo Selezionato:** n = {st.session_state.step}")

# ------------------------------------------------------------------------------
# CALCOLI CON FRAZIONI ESATTE
# ------------------------------------------------------------------------------
d0_frac = Fraction(d0_val, 1)
r_frac = Fraction(1, r_denom)

steps_data = []
s_A_frac = Fraction(0, 1)
s_T_frac = d0_frac

for n in range(max_steps + 1):
    if n == 0:
        tratto_A_frac = Fraction(0, 1)
        tratto_T_frac = Fraction(0, 1)
        distacco_frac = d0_frac
    else:
        distacco_precedente = steps_data[n - 1]["Distacco_Frac"]
        tratto_A_frac = distacco_precedente
        tratto_T_frac = tratto_A_frac * r_frac
        s_A_frac += tratto_A_frac
        s_T_frac += tratto_T_frac
        distacco_frac = s_T_frac - s_A_frac

    steps_data.append({
        "Passo n": n,
        "Misura tratto d_n (m)": format_frac_html(tratto_A_frac),
        "Misura posizione s_A (m)": format_frac_html(s_A_frac),
        "Misura posizione s_T (m)": format_frac_html(s_T_frac),
        "Misura distacco Δs_n (m)": format_frac_html(distacco_frac),
        "Pos_A_float": float(s_A_frac),
        "Pos_T_float": float(s_T_frac),
        "Tratto_A_float": float(tratto_A_frac),
        "Distacco_Frac": distacco_frac,
        "Tratto_A_Frac": tratto_A_frac,
    })

df = pd.DataFrame(steps_data)
curr_step = st.session_state.step
current_data = df.iloc[curr_step]

# ------------------------------------------------------------------------------
# 1. CONDIZIONI INIZIALI
# ------------------------------------------------------------------------------
st.markdown(
    f"""
<div class="init-conditions-card">
    <h4>📋 Condizioni Iniziali della Gara (Passo n = 0)</h4>
    <div class="init-conditions-text">
        <span><b>Posizione iniziale Achille s_A(0):</b> 0 m</span>
        <span><b>Misura vantaggio iniziale d₁ = m(A₀T₀):</b> {d0_val} m</span>
        <span>⚡ <b>Rapporto velocità:</b> v_A = {r_denom} · v_T</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Metric Banner
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Passo Logico (n)", f"{int(current_data['Passo n'])}")
with m2:
    st.metric(
        "Posizione s_A (Achille)",
        f"{current_data['Misura posizione s_A (m)']} m",
    )
with m3:
    st.metric(
        "Posizione s_T (Tartaruga)",
        f"{current_data['Misura posizione s_T (m)']} m",
    )
with m4:
    st.metric(
        "Misura distacco Δsₙ",
        f"{current_data['Misura distacco Δs_n (m)']} m",
    )

# ------------------------------------------------------------------------------
# 2. VISUALIZZAZIONE PRINCIPALE
# ------------------------------------------------------------------------------
col_left, col_right = st.columns([1.15, 1.0])

with col_left:
    st.markdown(
        f"<div class='section-title'>📍 Piste Parallele e Rappresentazione Spaziale (n = {curr_step})</div>",
        unsafe_allow_html=True,
    )

    fig_track = go.Figure()

    pos_A_val = current_data["Pos_A_float"]
    pos_T_val = current_data["Pos_T_float"]
    
    max_x = max(d0_val * 1.35, pos_T_val * 1.25 + 35)

    # Corsia Tartaruga (y = 1)
    fig_track.add_shape(
        type="line",
        x0=0, y0=1, x1=max_x, y1=1,
        line=dict(color="#86efac", width=5),
    )
    # Corsia Achille (y = 0)
    fig_track.add_shape(
        type="line",
        x0=0, y0=0, x1=max_x, y1=0,
        line=dict(color="#93c5fd", width=5),
    )

    # Marcatori notevoli dei punti geometrici
    for k in range(min(curr_step + 2, len(df))):
        pos_ak = df.iloc[k]["Pos_A_float"]
        show_label = (k == 0) or (k == curr_step and curr_step > 0)
        
        if k == 0:
            label_k = "A₀ = 0"
        else:
            label_k = f"A{to_subscript(str(k))} = T{to_subscript(str(k-1))}"

        fig_track.add_trace(
            go.Scatter(
                x=[pos_ak], y=[0],
                mode="markers+text" if show_label else "markers",
                marker=dict(symbol="line-ns", size=14, color="#334155"),
                text=[f"| {label_k}"] if show_label else None,
                textposition="bottom center",
                textfont=dict(size=14, color="#334155", family="Arial, sans-serif"),
                hoverinfo="none",
                showlegend=False,
            )
        )

    # Segmento geometrico A_{n-1} A_n percorso da Achille nell'ultimo passo
    if curr_step > 0:
        prev_A_val = df.iloc[curr_step - 1]["Pos_A_float"]
        fig_track.add_shape(
            type="line",
            x0=prev_A_val, y0=0, x1=pos_A_val, y1=0,
            line=dict(color="#1d4ed8", width=7),
        )

    # Segmento geometrico A_n T_n rappresentante il distacco residuo
    fig_track.add_shape(
        type="line",
        x0=pos_A_val, y0=0.5, x1=pos_T_val, y1=0.5,
        line=dict(color="#b91c1c", width=4, dash="dash"),
    )

    # Etichette di posizione dei punti A_n e T_n
    fig_track.add_trace(
        go.Scatter(
            x=[pos_A_val], y=[0],
            mode="markers+text",
            marker=dict(symbol="triangle-right", size=20, color="#1e3c72"),
            text=[f" <b>ACHILLE (A{to_subscript(str(curr_step))})</b> ➔"],
            textposition="top right",
            textfont=dict(size=15, color="#1e3c72"),
            hoverinfo="none",
            showlegend=False,
            cliponaxis=False,
        )
    )

    fig_track.add_trace(
        go.Scatter(
            x=[pos_T_val], y=[1],
            mode="markers+text",
            marker=dict(symbol="triangle-right", size=18, color="#15803d"),
            text=[f" <b>TARTARUGA (T{to_subscript(str(curr_step))})</b> ➔"],
            textposition="top right",
            textfont=dict(size=15, color="#15803d"),
            hoverinfo="none",
            showlegend=False,
            cliponaxis=False,
        )
    )

    fig_track.update_layout(
        xaxis=dict(
            title=dict(text="Asse della Posizione Spaziale s (metri)", font=dict(size=15, color="#0f172a")),
            range=[-5, max_x],
            tickfont=dict(size=13, color="#334155")
        ),
        yaxis=dict(
            tickvals=[0, 1],
            ticktext=["Corsia Achille", "Corsia Tartaruga"],
            range=[-0.5, 1.5],
            tickfont=dict(size=14, color="#0f172a")
        ),
        height=290,
        margin=dict(l=10, r=25, t=10, b=10),
        template="plotly_white",
        showlegend=False,
    )

    st.plotly_chart(fig_track, use_container_width=True)

with col_right:
    if curr_step == 0:
        st.markdown(
            f"""
      <div class="athena-socratic-card">
          <h3>🏛️ Osservazioni (n = 0)</h3>
          <p><b>1. Configurazione Spaziale:</b> Achille si trova nella posizione iniziale $A_0$ ($s_A = 0\\text{{ m}}$). La Tartaruga occupa il punto $T_0$ con un vantaggio rappresentato dal segmento $A_0T_0$.</p>
          <p><b>2. Misura Iniziale d₁:</b> La misura della lunghezza del segmento $A_0T_0$ è $d_1 = {d0_val}\\text{{ m}}$.</p>
          <p><b>3. Relazione Cinematica:</b> Achille corre {r_denom} volte più veloce. La misura dello spostamento della Tartaruga è pari a $1/{r_denom}$ della misura del tratto percorso da Achille nello stesso intervallo temporale.</p>
          <div class="cognitive-conflict-box">
              <h4>🧠 Focus:</h4>
              <div class="conflict-text">
                  "Per raggiungere la Tartaruga, concordi con Zenone che Achille debba prima di tutto coprire la misura del primo tratto $d_1 = {d0_val}\\text{{ m}}$ per giungere nel punto $T_0$ dove si trova la Tartaruga?"
              </div>
          </div>
      </div>
      """,
            unsafe_allow_html=True,
        )
    else:
        tratto_a_frac_str = current_data["Misura tratto d_n (m)"]
        tratto_t_frac_str = format_frac_html(
            Fraction(current_data["Tratto_A_Frac"], r_denom)
        )
        distacco_frac_str = current_data["Misura distacco Δs_n (m)"]

        somma_frazioni_list = [
            format_frac_html(df.iloc[k]["Tratto_A_Frac"])
            for k in range(1, curr_step + 1)
        ]
        somma_frazioni_str = " + ".join(somma_frazioni_list)

        c_step_sub = to_subscript(str(curr_step))
        prev_step_sub = to_subscript(str(curr_step - 1))
        next_step_sub = to_subscript(str(curr_step + 1))

        st.markdown(
            f"""
      <div class="athena-socratic-card">
          <h3>🏛️ Athena: Guida Socratica - Passo n = {curr_step}</h3>
          <p><b>1. Spostamento di Achille:</b> Achille percorre il segmento $A_{{{prev_step_sub}}}A_{{{c_step_sub}}}$ di misura <span class="fraction-badge">d{c_step_sub} = {tratto_a_frac_str} m</span>, giungendo nel punto $A_{{{c_step_sub}}}$ (coincidente con la posizione precedente $T_{{{prev_step_sub}}}$ della Tartaruga).</p>
          <p><b>2. Spostamento della Tartaruga:</b> Nello stesso intervallo, la Tartaruga avanza nel punto $T_{{{c_step_sub}}}$, percorrendo un tratto di misura <span class="fraction-badge">{tratto_t_frac_str} m</span> (pari a 1/{r_denom} di $d_{{{c_step_sub}}}$).</p>
          <p><b>3. Misura della Posizione Cumulata s_A:</b><br>
          <div style="margin: 6px 0; padding: 8px 12px; background-color: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; font-family: monospace; font-size: 0.98rem;">
              <b>s_A({c_step_sub}) = d₁ + ... + d{c_step_sub} = {somma_frazioni_str} = {current_data['Misura posizione s_A (m)']} m</b>
          </div>
          </p>
          <p><b>4. Misura del Distacco Residuo Δsₙ:</b> Il nuovo segmento di distacco $A_{{{c_step_sub}}}T_{{{c_step_sub}}}$ ha misura pari a <span class="fraction-badge">Δs{c_step_sub} = {distacco_frac_str} m</span>.</p>
          <div class="cognitive-conflict-box">
              <h4>🧠 Focus:</h4>
              <div class="conflict-text">
                  "Per azzerare la misura del distacco residuo $\\Delta s_{{{c_step_sub}}} = {distacco_frac_str}\\text{{ m}}$, concordi con Zenone che Achille debba ora percorrere un tratto di misura $d_{{{next_step_sub}}} = {distacco_frac_str}\\text{{ m}}$ per giungere nel punto $T_{{{c_step_sub}}}$?"
              </div>
          </div>
      </div>
      """,
            unsafe_allow_html=True,
        )

# ------------------------------------------------------------------------------
# 3. SCOMPOSIZIONE CUMULATA DEI TRATTI RETTILINEI
# ------------------------------------------------------------------------------
st.markdown(
    f"<div class='section-title'>📏 Scomposizione Additiva delle Misure dei Tratti d_n"
    f" (fino al passo n = {curr_step})</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='section-subtitle'>Somma delle misure dei segmenti percorsi da Achille: s_A(n) = d₁ +"
    " d₂ + ... + dₙ</div>",
    unsafe_allow_html=True,
)

fig_segments = go.Figure()
palette = [
    "#2563eb", "#d97706", "#16a34a", "#dc2626", "#9333ea",
    "#0891b2", "#db2777", "#ca8a04", "#0284c7"
]

for k in range(1, curr_step + 1):
    tratto_val = df.iloc[k]["Tratto_A_float"]
    tratto_frac_label = df.iloc[k]["Misura tratto d_n (m)"]
    color = palette[(k - 1) % len(palette)]
    k_sub = to_subscript(str(k))
    fig_segments.add_trace(
        go.Bar(
            y=["Tratti Achille"],
            x=[tratto_val],
            name=f"Tratto d{k_sub} ({tratto_frac_label} m)",
            orientation="h",
            marker=dict(color=color),
            hoverinfo="name+x",
        )
    )

curr_step_sub = to_subscript(str(curr_step))

fig_segments.add_trace(
    go.Scatter(
        x=[pos_T_val],
        y=["Tratti Achille"],
        mode="markers+text",
        marker=dict(symbol="triangle-right", size=16, color="#15803d"),
        text=[f"  <b>TARTARUGA (T{curr_step_sub})</b> ➔"],
        textposition="top right",
        textfont=dict(size=14, color="#15803d"),
        hoverinfo="none",
        showlegend=False,
        cliponaxis=False,
    )
)

fig_segments.update_layout(
    barmode="stack",
    xaxis=dict(
        title=dict(text="Misura della Posizione Spaziale s (metri)", font=dict(size=14, color="#0f172a")),
        range=[0, max_x],
        tickfont=dict(size=12, color="#334155")
    ),
    yaxis=dict(visible=False),
    height=140,
    margin=dict(l=10, r=25, t=10, b=10),
    template="plotly_white",
    showlegend=True,
    legend=dict(font=dict(size=13))
)

st.plotly_chart(fig_segments, use_container_width=True)

# ------------------------------------------------------------------------------
# 4. TABELLA ANALITICA
# ------------------------------------------------------------------------------
st.markdown(
    "<div class='section-title'>📊 Tabella Analitica delle Misure di Posizione e Distacco</div>",
    unsafe_allow_html=True,
)


def highlight_current(row):
    if row["Passo n"] == st.session_state.step:
        return ["background-color: #dbeafe; font-weight: bold; color: #1e40af"] * len(
            row
        )
    return [""] * len(row)


columns_requested = [
    "Passo n",
    "Misura tratto d_n (m)",
    "Misura posizione s_A (m)",
    "Misura posizione s_T (m)",
    "Misura distacco Δs_n (m)",
]

st.dataframe(
    df[columns_requested].style.apply(highlight_current, axis=1),
    use_container_width=True,
)

# ------------------------------------------------------------------------------
# 5. CHIUSURA MAIEUTICA
# ------------------------------------------------------------------------------
st.markdown(
    """
<div style="background-color: #fef2f2; border: 1px solid #fecaca; border-left: 6px solid #ef4444; padding: 14px 18px; border-radius: 8px; margin-top: 14px; box-shadow: 0 2px 6px rgba(239, 68, 68, 0.08);">
    <h4 style="color: #991b1b; margin-top:0; font-weight: 800; font-size: 1.08rem !important;">⚡ Il Cortocircuito Epistemologico di Elea:</h4>
    <p style="color: #7f1d1d; font-size: 1.02rem !important; font-weight: 600; margin-bottom: 0; line-height: 1.48;">
        "Se la scomposizione logica di Zenone dimostra che Achille deve percorrere una successione di <b>infiniti tratti rettilinei distinti di misura positiva (dₙ > 0)</b> espressi da frazioni sempre più piccole ma mai nulle, come fa l'esperienza reale del mondo sensibile a mostrare che la corsa si conclude e la misura del distacco si annulla?"
    </p>
</div>
""",
    unsafe_allow_html=True,
)
