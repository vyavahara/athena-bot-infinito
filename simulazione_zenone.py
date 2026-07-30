from fractions import Fraction
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ------------------------------------------------------------------------------
# 1. CONFIGURAZIONE PAGINA E CSS CUSTOM
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Fase 1: Conflitto Cognitivo - Il Paradosso di Zenone",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    .main { background-color: #f8fafc; }
    .stApp { font-family: 'Inter', system-ui, -apple-system, sans-serif; }
    
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e3c72 50%, #2a5298 100%);
        color: #ffffff; 
        padding: 20px 24px; 
        border-radius: 12px;
        text-align: center; 
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.12);
    }
    .hero-banner h1 { 
        color: #ffffff !important; 
        font-weight: 800 !important; 
        font-size: 1.8rem !important; 
        margin: 0 !important; 
    }
    
    .epistemic-card {
        background-color: #ffffff; 
        border: 1px solid #cbd5e1;
        border-left: 6px solid #0284c7; 
        border-radius: 8px;
        padding: 14px 18px; 
        margin-bottom: 16px;
    }
    .epistemic-card h4 { 
        color: #0f172a; 
        margin-top: 0; 
        margin-bottom: 8px; 
        font-size: 1.1rem !important; 
        font-weight: 700; 
    }
    
    .socratic-card {
        background-color: #ffffff; 
        border: 1px solid #cbd5e1;
        border-left: 6px solid #1e3c72; 
        border-radius: 8px;
        padding: 16px 18px; 
        min-height: 280px;
    }
    .socratic-card h3 { 
        color: #1e3c72; 
        font-size: 1.2rem !important; 
        margin-top: 0; 
        margin-bottom: 10px; 
        font-weight: 700;
    }
    
    .cognitive-conflict-box {
        background-color: #fffbeb; 
        border: 1px solid #fde68a;
        border-left: 6px solid #f59e0b; 
        padding: 12px 16px;
        border-radius: 8px; 
        margin-top: 14px;
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
        font-size: 1rem !important; 
        line-height: 1.5; 
    }
    
    .fraction-badge {
        background-color: #e2e8f0; 
        border: 1px solid #94a3b8;
        padding: 2px 6px; 
        border-radius: 4px; 
        font-family: monospace;
        font-weight: bold; 
        color: #0f172a;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------------------
# 2. HELPER UTILITIES (FUNZIONI PURE)
# ------------------------------------------------------------------------------
def to_subscript(text: str) -> str:
    """Converte cifre e caratteri in pedici Unicode ufficiali (es. ₀, ₁, ₂, ₙ)."""
    sub_map = str.maketrans("0123456789n", "₀₁₂₃₄₅₆₇₈₉ₙ")
    return str(text).translate(sub_map)

def format_frac(f: Fraction) -> str:
    """Rende una frazione in formato stringa esatto (es. 100/9)."""
    if f.denominator == 1:
        return f"{f.numerator}"
    return f"{f.numerator}/{f.denominator}"

# ------------------------------------------------------------------------------
# 3. MODELLO MATEMATICO DEDUTTIVO (DOMINIO)
# ------------------------------------------------------------------------------
def compute_zeno_sequence(delta_s0: int, contraction_ratio: int, max_steps: int) -> pd.DataFrame:
    """
    Costruisce la successione geometrica delle configurazioni discrete.
    Nessuna variabile temporale: solo relazioni di incidenza spaziale su R.
    """
    delta_s0_frac = Fraction(delta_s0, 1)
    k_frac = Fraction(contraction_ratio, 1)
    
    records = []
    A_frac = Fraction(0, 1)
    T_frac = delta_s0_frac
    
    for n in range(max_steps + 1):
        if n == 0:
            d_frac = Fraction(0, 1)
            t_frac = Fraction(0, 1)
            delta_s_frac = delta_s0_frac
        else:
            prev_delta_s = records[n - 1]["delta_s"]
            d_frac = prev_delta_s                # Achille raggiunge T_(n-1)
            t_frac = prev_delta_s / k_frac       # La tartaruga avanza di 1/k del divario
            A_frac += d_frac
            T_frac += t_frac
            delta_s_frac = T_frac - A_frac

        records.append({
            "n": n,
            "A": A_frac,
            "d": d_frac,
            "T": T_frac,
            "t": t_frac,
            "delta_s": delta_s_frac,
            "A_float": float(A_frac),
            "T_float": float(T_frac),
            "d_float": float(d_frac),
            "t_float": float(t_frac),
            "delta_s_float": float(delta_s_frac),
        })
    return pd.DataFrame(records)

# ------------------------------------------------------------------------------
# 4. CONTROLLO DI STATO E SIDEBAR
# ------------------------------------------------------------------------------
st.markdown(
    """
<div class="hero-banner">
    <h1>🏃 🐢 Fase 1: Simulazione Discreta & Conflitto Cognitivo</h1>
</div>
""",
    unsafe_allow_html=True,
)

st.sidebar.header("⚙️ Parametri del Modello Geometrico")
delta_s0_input = st.sidebar.number_input(
    "Distacco Iniziale Δs₀ = m(A₀T₀) [metri]:",
    value=100, min_value=1, step=10
)
k_input = st.sidebar.number_input(
    "Fattore di contrazione spaziale (k):",
    value=10, min_value=2, max_value=100, step=1
)
max_steps_input = st.sidebar.slider(
    "Numero di suddivisioni logiche da calcolare (n):",
    min_value=1, max_value=15, value=8
)

# Inizializzazione Session State
if "step" not in st.session_state:
    st.session_state.step = 0

# Callback per gestione pulita dello stato senza desincronizzazioni
def set_step(new_step):
    st.session_state.step = max(0, min(new_step, max_steps_input))

col_b1, col_b2, col_b3, _ = st.columns([1, 1, 1, 2])
with col_b1:
    st.button("⏮️ Reset (n = 0)", on_click=set_step, args=(0,), use_container_width=True)
with col_b2:
    st.button("◀️ Precedente", on_click=set_step, args=(st.session_state.step - 1,), use_container_width=True)
with col_b3:
    st.button("▶️ Successivo", on_click=set_step, args=(st.session_state.step + 1,), use_container_width=True)

curr_step = st.session_state.step

# Esecuzione modello interno
df = compute_zeno_sequence(delta_s0_input, k_input, max_steps_input)
current_row = df.iloc[curr_step]

# ------------------------------------------------------------------------------
# 5. PREMESSA EPISTEMOLOGICA
# ------------------------------------------------------------------------------
st.markdown(
"""
<div class="epistemic-card">
<h4>📐 Inquadramento Assiomatico della Simulazione</h4>
<p>
Consideriamo la retta orientata ℝ come supporto spaziale. La simulazione modella una <b>successione discreta di configurazioni geometriche</b> $(A_n, T_n)_{n \in \mathbb{N}}$. 
Non stiamo misurando la durata temporale del movimento, ma l'evoluzione delle posizioni ad ogni passo logico $n$.
</p>
</div>
""",
unsafe_allow_html=True
)

# Metric Banner
m1, m2, m3, m4 = st.columns(4)
m1.metric("Passo Logico (n)", f"{curr_step}")
m2.metric("Punto Aₙ (Achille)", f"{format_frac(current_row['A'])} m")
m3.metric("Punto Tₙ (Tartaruga)", f"{format_frac(current_row['T'])} m")
m4.metric("Distacco Residuo Δsₙ", f"{format_frac(current_row['delta_s'])} m")

# ------------------------------------------------------------------------------
# 6. VISUALIZZAZIONE GRAFICA ADATTIVA (PLOTLY)
# ------------------------------------------------------------------------------
col_graph, col_athena = st.columns([1.2, 1.0])

with col_graph:
    st.markdown(f"##### 📍 Configurazione Spaziale al Passo n = {curr_step}")
    
    fig_track = go.Figure()
    
    A_val = current_row["A_float"]
    T_val = current_row["T_float"]
    delta_val = current_row["delta_s_float"]
    
    # Zoom adattivo: evita che i punti collassino visivamente ad alti passi n
    margin_x = max(delta_val * 2.5, 0.5) if curr_step > 0 else delta_s0_input * 0.2
    min_x = max(-2.0, A_val - margin_x)
    max_x = T_val + margin_x
    
    # Corsie
    fig_track.add_shape(type="line", x0=min_x, y0=1, x1=max_x, y1=1, line=dict(color="#86efac", width=4))
    fig_track.add_shape(type="line", x0=min_x, y0=0, x1=max_x, y1=0, line=dict(color="#93c5fd", width=4))
    
    # Segmento distacco residuo Δs_n
    fig_track.add_shape(
        type="line", x0=A_val, y0=0.5, x1=T_val, y1=0.5,
        line=dict(color="#ef4444", width=3, dash="dash")
    )
    
    # Marker Achille
    fig_track.add_trace(go.Scatter(
        x=[A_val], y=[0], mode="markers+text",
        marker=dict(symbol="circle", size=16, color="#1e3c72"),
        text=[f"🏃 <b>A{to_subscript(str(curr_step))}</b>"],
        textposition="top center", textfont=dict(size=14, color="#1e3c72"),
        hoverinfo="none", showlegend=False
    ))
    
    # Marker Tartaruga
    fig_track.add_trace(go.Scatter(
        x=[T_val], y=[1], mode="markers+text",
        marker=dict(symbol="circle", size=14, color="#15803d"),
        text=[f"🐢 <b>T{to_subscript(str(curr_step))}</b>"],
        textposition="top center", textfont=dict(size=14, color="#15803d"),
        hoverinfo="none", showlegend=False
    ))
    
    fig_track.update_layout(
        xaxis=dict(title="Coordinata sulla Retta (m)", range=[min_x, max_x], tickfont=dict(size=12)),
        yaxis=dict(tickvals=[0, 1], ticktext=["Corsia Achille", "Corsia Tartaruga"], range=[-0.5, 1.8]),
        height=300, margin=dict(l=10, r=20, t=20, b=10), template="plotly_white"
    )
    
    st.plotly_chart(fig_track, use_container_width=True)

# ------------------------------------------------------------------------------
# 7. MAIEUTICA SOCRATICA (ATHENA)
# ------------------------------------------------------------------------------
with col_athena:
    c_sub = to_subscript(str(curr_step))
    p_sub = to_subscript(str(curr_step - 1)) if curr_step > 0 else "0"
    n_sub = to_subscript(str(curr_step + 1))
    
    d_str = format_frac(current_row["d"])
    t_str = format_frac(current_row["t"])
    delta_str = format_frac(current_row["delta_s"])
    
    if curr_step == 0:
        socratic_text = f"""
        <div class="socratic-card">
            <h3>🏛️ Athena: Stato Iniziale (n = 0)</h3>
            <p><b>Configurazione:</b> Achille si trova nell'origine $A_0 = 0$, la Tartaruga occupa $T_0 = {delta_s0_input}\text{ m}$.</p>
            <p><b>Distacco Iniziale:</b> $\Delta s_0 = {delta_s0_input}\text{ m}$.</p>
            <div class="cognitive-conflict-box">
                <h4>🧠 Domanda Socratica:</h4>
                <div class="conflict-text">
                    Per poter raggiungere o superare la Tartaruga, concordi che Achille debba <i>necessariamente</i> occupare prima il punto geometrico $T_0$ in cui la Tartaruga si trova adesso?
                </div>
            </div>
        </div>
        """
    else:
        socratic_text = f"""
        <div class="socratic-card">
            <h3>🏛️ Athena: Analisi al Passo n = {curr_step}</h3>
            <p>1. <b>Spostamento di Achille:</b> $d_{c_sub} = {d_str}\text{ m}$, raggiungendo $A_{c_sub} = T_{p_sub}$.</p>
            <p>2. <b>Spostamento Tartaruga:</b> $t_{c_sub} = {t_str}\text{ m}$, raggiungendo $T_{c_sub}$.</p>
            <p>3. <b>Distacco Residuo:</b> $\Delta s_{c_sub} = m(A_{c_sub}T_{c_sub}) = \mathbf{{{delta_str}\text{{ m}}}}$.</p>
            <div class="cognitive-conflict-box">
                <h4>🧠 Cortocircuito Cognitivo:</h4>
                <div class="conflict-text">
                    La distanza residua $\Delta s_{c_sub} = {delta_str}\text{ m}$ è strettamente positiva ($\Delta s_{c_sub} > 0$).<br>
                    Per colmare questo nuovo divario, Achille non dovrà compiere un ulteriore spostamento $d_{n_sub} = {delta_str}\text{ m}$ per raggiungere $T_{c_sub}$? Se questo schema si ripetesse all'infinito, come potrebbe Achille azzerare il distacco?
                </div>
            </div>
        </div>
        """
    st.markdown(socratic_text, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 8. TABELLA ANALITICA CON FRAZIONI ESATTE
# ------------------------------------------------------------------------------
st.markdown("##### 📊 Tabella Analitica delle Frazioni Esatte")

display_rows = []
for idx, row in df.iterrows():
    display_rows.append({
        "Passo (n)": row["n"],
        "Posizione Achille (Aₙ)": f"{format_frac(row['A'])} m",
        "Spostamento Achille (dₙ)": f"{format_frac(row['d'])} m",
        "Posizione Tartaruga (Tₙ)": f"{format_frac(row['T'])} m",
        "Spostamento Tartaruga (tₙ)": f"{format_frac(row['t'])} m",
        "Distacco Residuo (Δsₙ)": f"{format_frac(row['delta_s'])} m",
    })

df_display = pd.DataFrame(display_rows)

def highlight_row(row):
    if row["Passo (n)"] == curr_step:
        return ["background-color: #dbeafe; font-weight: bold; color: #1e40af"] * len(row)
    return [""] * len(row)

st.dataframe(df_display.style.apply(highlight_row, axis=1), use_container_width=True)

# ------------------------------------------------------------------------------
# 9. CHIUSURA DIDATTICA E TRANSIZIONE ALLA FASE 2
# ------------------------------------------------------------------------------
st.markdown(
    """
<div style="background-color: #fef2f2; border: 1px solid #fecaca; border-left: 6px solid #ef4444; padding: 14px 18px; border-radius: 8px; margin-top: 16px;">
    <h4 style="color: #991b1b; margin-top:0; font-weight: 800;">⚡ Il Nodo Concettuale della Fase 1:</h4>
    <p style="color: #7f1d1d; font-weight: 600; margin-bottom: 0; line-height: 1.5;">
        La scomposizione discreta di Zenone dimostra che per qualsiasi $n \in \mathbb{N}$ finito si ha sempre $\Delta s_n > 0$. 
        L'illusione nasce dal confondere il <i>numero infinito di suddivisioni spaziali discrete</i> con la <i>durata del processo continuo</i>. 
        Per risolvere il paradosso occorre abbandonare la scansione passo-passo e passare alla <b>Fase 2 (Simulazione Cinematica Continua)</b> introducendo le equazioni orarie $s(t)$.
    </p>
</div>
""",
    unsafe_allow_html=True,
)
