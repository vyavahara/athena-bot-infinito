from fractions import Fraction
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ------------------------------------------------------------------------------
# 1. CONFIGURAZIONE PAGINA ED ELEMENTI VISIVI (CSS)
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Fase 1: Simulazione Discreta - Paradosso di Zenone",
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
        padding: 18px 24px; 
        border-radius: 12px;
        text-align: center; 
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.12);
    }
    .hero-banner h1 { 
        color: #ffffff !important; 
        font-weight: 800 !important; 
        font-size: 1.75rem !important; 
        margin: 0 !important; 
    }
    
    .epistemic-card {
        background-color: #ffffff; 
        border: 1px solid #cbd5e1;
        border-left: 6px solid #0284c7; 
        border-radius: 8px;
        padding: 12px 18px; 
        margin-bottom: 16px;
    }
    .epistemic-card h4 { 
        color: #0f172a; 
        margin-top: 0; 
        margin-bottom: 6px; 
        font-size: 1.05rem !important; 
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
        font-size: 1.15rem !important; 
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
        font-size: 0.98rem !important; 
        line-height: 1.48; 
    }
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------------------
# 2. HELPER UTILITIES
# ------------------------------------------------------------------------------
def to_subscript(text: str) -> str:
    """Converte stringhe numeriche in pedici Unicode ufficiali (es. A₀, T₁, T₂)."""
    sub_map = str.maketrans("0123456789n", "₀₁₂₃₄₅₆₇₈₉ₙ")
    return str(text).translate(sub_map)

def format_frac(f: Fraction) -> str:
    """Restituisce la rappresentazione in frazione esatta per la tabella e le metriche."""
    if f.denominator == 1:
        return f"{f.numerator}"
    return f"{f.numerator}/{f.denominator}"

# ------------------------------------------------------------------------------
# 3. MODELLO MATEMATICO DEDUTTIVO (DOMINIO IN Q)
# ------------------------------------------------------------------------------
def compute_zeno_sequence(delta_s0: int, contraction_ratio: int, max_steps: int) -> pd.DataFrame:
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
            d_frac = prev_delta_s
            t_frac = prev_delta_s / k_frac
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
    min_value=1, max_value=12, value=6
)

if "step" not in st.session_state:
    st.session_state.step = 0

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
La pista è descritta sulla semiretta orientata ℝ. La simulazione genera la <b>successione delle configurazioni geometriche</b> (Aₙ, Tₙ).
Nessun riferimento al tempo <i>t</i>: analizziamo la paradossalità del conteggio discreto passo dopo passo.
</p>
</div>
""",
unsafe_allow_html=True
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Passo Logico (n)", f"{curr_step}")
m2.metric("Punto Aₙ (Achille)", f"{format_frac(current_row['A'])} m")
m3.metric("Punto Tₙ (Tartaruga)", f"{format_frac(current_row['T'])} m")
m4.metric("Distacco Residuo Δsₙ", f"{format_frac(current_row['delta_s'])} m")

# ------------------------------------------------------------------------------
# 6. VISUALIZZAZIONE GRAFICA PLOTLY (MULTI-LINEA CON MEMORIA STORICA ED AUTO-ZOOM)
# ------------------------------------------------------------------------------
col_graph, col_athena = st.columns([1.35, 1.0])

with col_graph:
    st.markdown(f"##### 📍 Diagramma a Cascata delle Posizioni (fino al passo n = {curr_step})")
    
    fig_track = go.Figure()
    
    current_A = current_row["A_float"]
    current_T = current_row["T_float"]
    delta_val = current_row["delta_s_float"]
    
    # Auto-zoom adattivo
    if curr_step >= 3 and delta_val < (delta_s0_input * 0.05):
        zoom_margin = max(delta_val * 4.0, 0.05)
        x_range_min = current_A - (zoom_margin * 0.5)
        x_range_max = current_T + zoom_margin
    else:
        x_range_min = - (delta_s0_input * 0.08)
        x_range_max = current_T + (delta_s0_input * 0.25)

    # Costruzione delle linee a cascata dal passo 0 fino a curr_step
    for step_idx in range(curr_step + 1):
        y_level = curr_step - step_idx
        
        row_step = df.iloc[step_idx]
        a_pos = row_step["A_float"]
        t_pos = row_step["T_float"]
        
        # 1. Linea di riferimento orizzontale
        fig_track.add_shape(
            type="line",
            x0=x_range_min, y0=y_level, x1=x_range_max, y1=y_level,
            line=dict(color="#cbd5e1", width=2)
        )

        # 2. Marcatori storici SOTTO la linea (corretto con line=dict(width=2))
        fig_track.add_trace(go.Scatter(
            x=[0], y=[y_level], mode="markers+text",
            marker=dict(symbol="line-ns", size=10, color="#64748b", line=dict(width=2, color="#64748b")),
            text=["A₀"], textposition="bottom center",
            textfont=dict(size=12, color="#475569"), hoverinfo="none", showlegend=False
        ))
        
        # Posizioni storiche delle tartarughe T_k per k <= step_idx
        for k in range(step_idx + 1):
            tk_pos = df.iloc[k]["T_float"]
            label_tk = f"T{to_subscript(str(k))}"
            
            fig_track.add_trace(go.Scatter(
                x=[tk_pos], y=[y_level], mode="markers+text",
                marker=dict(symbol="line-ns", size=10, color="#64748b", line=dict(width=2, color="#64748b")),
                text=[label_tk], textposition="bottom center",
                textfont=dict(size=12, color="#475569"), hoverinfo="none", showlegend=False
            ))
            
        # 3. Attori SOPRA la linea
        fig_track.add_trace(go.Scatter(
            x=[a_pos], y=[y_level + 0.18], mode="text+markers",
            marker=dict(symbol="circle", size=10, color="#1e3c72"),
            text=["🏃 <b>Achille</b>"], textposition="top center",
            textfont=dict(size=13, color="#1e3c72"), hoverinfo="none", showlegend=False
        ))
        
        fig_track.add_trace(go.Scatter(
            x=[t_pos], y=[y_level + 0.18], mode="text+markers",
            marker=dict(symbol="circle", size=8, color="#15803d"),
            text=["🐢 <b>Tartaruga</b>"], textposition="top center",
            textfont=dict(size=13, color="#15803d"), hoverinfo="none", showlegend=False
        ))

    y_tick_vals = list(range(curr_step + 1))
    y_tick_texts = [f"Passo {curr_step - y}" for y in y_tick_vals]

    fig_track.update_layout(
        xaxis=dict(
            title="Coordinata sulla Retta Orientata (m)",
            range=[x_range_min, x_range_max],
            tickfont=dict(size=12, color="#334155")
        ),
        yaxis=dict(
            tickvals=y_tick_vals,
            ticktext=y_tick_texts,
            range=[-0.5, curr_step + 0.7],
            tickfont=dict(size=12, color="#0f172a")
        ),
        height=max(320, 120 + curr_step * 65),
        margin=dict(l=20, r=20, t=20, b=20),
        template="plotly_white"
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
        socratic_html = f"""
        <div class="socratic-card">
            <h3>🏛️ Athena: Stato Iniziale (n = 0)</h3>
            <p><b>Configurazione:</b> Achille si trova nell'origine A₀ = 0, la Tartaruga occupa T₀ = {delta_s0_input} m.</p>
            <p><b>Distacco Iniziale:</b> Δs₀ = {delta_s0_input} m.</p>
            <div class="cognitive-conflict-box">
                <h4>🧠 Domanda Socratica:</h4>
                <div class="conflict-text">
                    Per poter raggiungere o superare la Tartaruga, concordi che Achille debba <i>necessariamente</i> occupare prima il punto geometrico T₀ dove la Tartaruga si trova adesso?
                </div>
            </div>
        </div>
        """
    else:
        socratic_html = f"""
        <div class="socratic-card">
            <h3>🏛️ Athena: Analisi al Passo n = {curr_step}</h3>
            <p>1. <b>Spostamento di Achille:</b> d{c_sub} = {d_str} m, raggiungendo A{c_sub} = T{p_sub}.</p>
            <p>2. <b>Spostamento Tartaruga:</b> t{c_sub} = {t_str} m, raggiungendo T{c_sub}.</p>
            <p>3. <b>Distacco Residuo:</b> Δs{c_sub} = m(A{c_sub}T{c_sub}) = <b>{delta_str} m</b>.</p>
            <div class="cognitive-conflict-box">
                <h4>🧠 Cortocircuito Cognitivo:</h4>
                <div class="conflict-text">
                    La distanza residua Δs{c_sub} = {delta_str} m è strettamente positiva (Δs{c_sub} &gt; 0).<br>
                    Per colmare questo nuovo divario, Achille non dovrà compiere un ulteriore spostamento d{n_sub} = {delta_str} m per raggiungere T{c_sub}? Se questo processo continua all'infinito, come potrà mai Achille azzerare il distacco?
                </div>
            </div>
        </div>
        """
    st.markdown(socratic_html, unsafe_allow_html=True)

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
# 9. CHIUSURA DIDATTICA
# ------------------------------------------------------------------------------
st.markdown(
    """
<div style="background-color: #fef2f2; border: 1px solid #fecaca; border-left: 6px solid #ef4444; padding: 14px 18px; border-radius: 8px; margin-top: 16px;">
    <h4 style="color: #991b1b; margin-top:0; font-weight: 800;">⚡ Il Nodo Concettuale della Fase 1:</h4>
    <p style="color: #7f1d1d; font-weight: 600; margin-bottom: 0; line-height: 1.5;">
        La scomposizione discreta di Zenone dimostra che per qualsiasi n finito si ha sempre Δsₙ &gt; 0. 
        L'illusione nasce dal confondere il <i>numero infinito di suddivisioni spaziali discrete</i> con la <i>durata del processo continuo</i>. 
        Per risolvere il paradosso occorre abbandonare la scansione passo-passo e passare alla <b>Fase 2 (Simulazione Cinematica Continua)</b> introducendo le equazioni orarie s(t).
    </p>
</div>
""",
    unsafe_allow_html=True,
)
