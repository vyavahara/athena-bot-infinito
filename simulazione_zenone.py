from fractions import Fraction
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ------------------------------------------------------------------------------
# CONFIGURAZIONE PAGINA
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Simulazione del Paradosso di Achille e la tartaruga",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------------------
# CSS PERSONALIZZATO (Con centramento verticale del banner e flip icone)
# ------------------------------------------------------------------------------
st.markdown(
    """
<style>
    .main { background-color: #f8fafc; }
    .stApp { font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    
    .block-container { padding-top: 0.8rem !important; padding-bottom: 0.8rem !important; }
    div[data-testid="stVerticalBlock"] { gap: 0.6rem !important; }
    p { margin-bottom: 0.3rem !important; line-height: 1.35; }
    
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e3c72 60%, #2a5298 100%);
        color: #ffffff; padding: 16px; border-radius: 8px;
        text-align: center; margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 70px;
    }
    .hero-banner h1 { 
        color: #ffffff; 
        font-weight: 800; 
        font-size: 1.55rem; 
        margin: 0 !important; 
        line-height: 1.2;
    }
    
    /* Classe per riflettere le emoji orizzontalmente verso destra */
    .flip-right {
        display: inline-block;
        transform: scaleX(-1);
    }
    
    .init-conditions-card {
        background-color: #ffffff; border: 1px solid #e2e8f0;
        border-left: 5px solid #0284c7; border-radius: 6px;
        padding: 8px 12px; margin-bottom: 10px;
    }
    .init-conditions-card h4 { color: #0f172a; margin-top: 0; margin-bottom: 4px; font-size: 0.95rem; font-weight: 700; }
    
    .athena-socratic-card {
        background-color: #ffffff; border: 1px solid #cbd5e1;
        border-left: 5px solid #1e3c72; border-radius: 6px;
        padding: 12px; height: 100%;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .athena-socratic-card h3 { color: #1e3c72; font-size: 1.02rem; margin-top: 0; margin-bottom: 6px; }
    
    .section-title {
        color: #0f172a; font-weight: 700; font-size: 1.1rem;
        margin-top: 14px; margin-bottom: 4px;
    }
    .section-subtitle {
        color: #475569; font-weight: 600; font-size: 0.92rem;
        margin-top: 0px; margin-bottom: 10px;
    }
    
    .fraction-badge {
        background-color: #f1f5f9; border: 1px solid #cbd5e1;
        padding: 1px 5px; border-radius: 4px; font-family: monospace;
        font-size: 0.88rem; font-weight: bold; color: #0f172a;
    }
    
    .cognitive-conflict-box {
        background-color: #fffbeb; border: 1px solid #fef3c7;
        border-left: 5px solid #f59e0b; padding: 10px 12px;
        border-radius: 6px; margin-top: 10px;
    }
    .cognitive-conflict-box h4 { color: #b45309; margin-top: 0; margin-bottom: 3px; font-size: 0.92rem; font-weight: 700; }
    .conflict-text { color: #78350f; font-weight: 600; font-size: 0.89rem; line-height: 1.38; }

    div[data-testid="stDataFrame"] { font-size: 0.85rem !important; }
    [data-testid="stMetricValue"] { font-size: 1.1rem !important; font-weight: 700; }
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
    <h1><span class="flip-right">🏃‍♂️</span> <span class="flip-right">🐢</span> Simulazione del Paradosso di Achille e la tartaruga</h1>
</div>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------------------
# SIDEBAR - PARAMETRI GEOMETRICI
# ------------------------------------------------------------------------------
st.sidebar.header("⚙️ Impostazione della Pista")
d0_val = st.sidebar.number_input(
    "Vantaggio Iniziale Tartaruga (T₀ = d₁) [metri]:",
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
        "Tratto percorso da Achille": format_frac_html(tratto_A_frac),
        "Posizione raggiunta da Achille": format_frac_html(s_A_frac),
        "Posizione della tartaruga": format_frac_html(s_T_frac),
        "Vantaggio della tartaruga": format_frac_html(distacco_frac),
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
# 1. CONDIZIONI INIZIALI (Icone adeguate e orientate a destra con .flip-right)
# ------------------------------------------------------------------------------
st.markdown(
    f"""
<div class="init-conditions-card">
    <h4>📋 Condizioni Iniziali della Gara (Passo n = 0)</h4>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 8px; font-size: 0.88rem;">
        <span><span class="flip-right">🏃‍♂️</span> <b>Posizione Iniziale Achille (A₀):</b> 0 m</span>
        <span><span class="flip-right">🐢</span> <b>Vantaggio Iniziale Tartaruga (T₀ = d₁):</b> {d0_val} m</span>
        <span>⚡ <b>Velocità:</b> Achille corre <b>{r_denom} volte più veloce</b> della Tartaruga</span>
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
        "Posizione Aₙ (Achille)",
        f"{current_data['Posizione raggiunta da Achille']} m",
    )
with m3:
    st.metric(
        "Posizione Tₙ (Tartaruga)",
        f"{current_data['Posizione della tartaruga']} m",
    )
with m4:
    st.metric(
        "Vantaggio Δsₙ (Tartaruga)",
        f"{current_data['Vantaggio della tartaruga']} m",
    )

# ------------------------------------------------------------------------------
# 2. VISUALIZZAZIONE PRINCIPALE
# ------------------------------------------------------------------------------
col_left, col_right = st.columns([1.1, 1.0])

with col_left:
    st.markdown(
        f"<div class='section-title'><span class='flip-right'>🏃‍♂️</span><span class='flip-right'>🐢</span> Piste Parallele e Posizione (n ="
        f" {curr_step})</div>",
        unsafe_allow_html=True,
    )

    fig_track = go.Figure()

    pos_A_val = current_data["Pos_A_float"]
    pos_T_val = current_data["Pos_T_float"]
