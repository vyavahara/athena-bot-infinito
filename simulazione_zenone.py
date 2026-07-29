from fractions import Fraction
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ------------------------------------------------------------------------------
# CONFIGURAZIONE PAGINA
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Simulazione del Paradosso di Achille e la Tartaruga",
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
    .main { background-color: #f8fafc; }
    .stApp { font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    
    .block-container { padding-top: 1rem !important; padding-bottom: 1.2rem !important; }
    div[data-testid="stVerticalBlock"] { gap: 0.8rem !important; }
    p { margin-bottom: 0.4rem !important; line-height: 1.5; font-size: 1.05rem !important; }
    
    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e3c72 50%, #2a5298 100%);
        color: #ffffff; 
        padding: 20px 24px; 
        border-radius: 12px;
        text-align: center; 
        margin-bottom: 14px;
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
    }
    
    /* Condizioni Iniziali e Modello Matematico */
    .init-conditions-card, .math-model-card {
        background-color: #ffffff; 
        border: 1px solid #cbd5e1;
        border-left: 6px solid #0284c7; 
        border-radius: 8px;
        padding: 12px 18px; 
        margin-bottom: 14px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }
    .init-conditions-card h4, .math-model-card h4 { 
        color: #0f172a; 
        margin-top: 0; 
        margin-bottom: 6px; 
        font-size: 1.1rem !important; 
        font-weight: 700; 
    }
    .init-conditions-text {
        display: flex; 
        justify-content: space-around; 
        align-items: center; 
        flex-wrap: wrap; 
        gap: 12px; 
        font-size: 1.05rem !important;
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
        font-size: 1.22rem !important; 
        margin-top: 0; 
        margin-bottom: 8px; 
        font-weight: 700;
    }
    
    /* Sezioni Titoli */
    .section-title {
        color: #0f172a; 
        font-weight: 800; 
        font-size: 1.25rem !important;
        margin-top: 16px; 
        margin-bottom: 6px;
    }
    .section-subtitle {
        color: #475569; 
        font-weight: 600; 
        font-size: 1.05rem !important;
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
        font-size: 1rem !important; 
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
        margin-top: 14px;
        box-shadow: 0 2px 5px rgba(245, 158, 11, 0.08);
    }
    .cognitive-conflict-box h4 { 
        color: #b45309; 
        margin-top: 0; 
        margin-bottom: 4px; 
        font-size: 1.08rem !important; 
        font-weight: 800; 
    }
    .conflict-text { 
        color: #78350f; 
        font-weight: 600; 
        font-size: 1.05rem !important; 
        line-height: 1.48; 
    }

    div[data-testid="stDataFrame"] { font-size: 0.98rem !important; }
    [data-testid="stMetricValue"] { font-size: 1.4rem !important; font-weight: 800 !important; color: #0f172a; }
    [data-testid="stMetricLabel"] { font-size: 1rem !important; font-weight: 600 !important; color: #475569; }
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------------------
# FUNZIONE HELPER PER CONVERTIRE CIFRE IN PEDICI UNICODE CORRETTI
# ------------------------------------------------------------------------------
def to_subscript(text: str) -> str:
    """Converte cifre e indicatori in pedici Unicode ufficiali puliti (es. ₀, ₁, ₂, ₙ)."""
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
    <h1>🏃 🐢 Simulazione del Paradosso di Achille e la Tartaruga</h1>
</div>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------------------
# DEFINIZIONE FORMALE DEL MODELLO MATEMATICO (Riquadro Introduttivo)
# ------------------------------------------------------------------------------
st.markdown(
    """
<div class="math-model-card">
    <h4>📐 Modello Matematico del Paradosso</h4>
    <p style="margin-bottom: 6px; color: #334155;">
        La corsia è una semiretta orientata con origine O. Ad ogni punto della corsia è 
        associata una coordinata reale non negativa che ne determina la posizione geometrica
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------------------
# SIDEBAR - PARAMETRI GEOMETRICI
# ------------------------------------------------------------------------------
st.sidebar.header("⚙️ Impostazione della Pista")
delta_s0_val = st.sidebar.number_input(
    "Misura del distacco iniziale Δs₀ = m(A₀T₀) [metri]:",
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
# MODELLO MATEMATICO INTERNO E CALCOLI CON FRAZIONI ESATTE
# ------------------------------------------------------------------------------
delta_s0_frac = Fraction(delta_s0_val, 1)
contraction_frac = Fraction(1, r_denom)

steps_data = []

# Relazioni matematiche formali iniziali:
# A₀ = 0
# T₀ = Δs₀
A_frac = Fraction(0, 1)
T_frac = delta_s0_frac

for n in range(max_steps + 1):
    if n == 0:
        d_frac = Fraction(0, 1)
        t_frac = Fraction(0, 1)
        delta_s_frac = delta_s0_frac
    else:
        # Relazioni matematiche formali iterative per ogni step n:
        # A₀ = 0
        # T₀ = Δs₀
        # Δsₙ = Tₙ - Aₙ
        # dₙ = Δsₙ₋₁
        # tₙ = Δsₙ₋₁ / k
        # Aₙ = Aₙ₋₁ + dₙ
        # Tₙ = Tₙ₋₁ + tₙ
        delta_s_precedente = steps_data[n - 1]["delta_s"]
        d_frac = delta_s_precedente
        t_frac = delta_s_precedente / Fraction(r_denom, 1)
        A_frac += d_frac
        T_frac += t_frac
        delta_s_frac = T_frac - A_frac

    # Struttura interna contenente solo dati matematici grezzi
    steps_data.append({
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
        <span>🏃 <b>Posizione iniziale di Achille A₀:</b> 0 m</span>
        <span>🏃 <b>Posizione iniziale della Tartaruga T₀:</b> 100 m</span>
        <span>🐢 <b>Distacco iniziale Δs₀ = d(A₀;T₀) ossia la distanza tra le ascisse di A₀ e T₀ :</b> {delta_s0_val} m</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Metric Banner con etichette geometriche rigorose aggiornate
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Passo Logico (n)", f"{int(current_data['n'])}")
with m2:
    st.metric("Aₙ", f"{format_frac_html(current_data['A'])} m")
with m3:
    st.metric("Tₙ", f"{format_frac_html(current_data['T'])} m")
with m4:
    st.metric("Δsₙ", f"{format_frac_html(current_data['delta_s'])} m")

# ------------------------------------------------------------------------------
# 2. VISUALIZZAZIONE PRINCIPALE
# ------------------------------------------------------------------------------
col_left, col_right = st.columns([1.15, 1.0])

with col_left:
    st.markdown(
        f"<div class='section-title'>🏃 🐢 Piste Parallele e Rappresentazione (n = {curr_step})</div>",
        unsafe_allow_html=True,
    )

    fig_track = go.Figure()

    A_val = current_data["A_float"]
    T_val = current_data["T_float"]
    
    # Range ampio per evitare tagli del testo sul lato destro dell'asse X
    max_x = max(delta_s0_val * 1.40, T_val * 1.30 + 40)

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

    # Marcatori dei punti geometrici A_k
    for k in range(min(curr_step + 2, len(df))):
        pos_ak = df.iloc[k]["A_float"]
        show_label = (k == 0) or (k == curr_step and curr_step > 0)
        label_k = "A₀ = 0" if k == 0 else f"A{to_subscript(str(k))} = T{to_subscript(str(k-1))}"

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

    # Segmento percorso da Achille nello step corrente
    if curr_step > 0:
        prev_A_val = df.iloc[curr_step - 1]["A_float"]
        fig_track.add_shape(
            type="line",
            x0=prev_A_val, y0=0, x1=A_val, y1=0,
            line=dict(color="#1d4ed8", width=7),
        )

    # Segmento rappresentante il distacco residuo Δsₙ
    fig_track.add_shape(
        type="line",
        x0=A_val, y0=0.5, x1=T_val, y1=0.5,
        line=dict(color="#b91c1c", width=4, dash="dash"),
    )

    # Marcatori di Achille e Tartaruga
    fig_track.add_trace(
        go.Scatter(
            x=[A_val], y=[0],
            mode="markers+text",
            marker=dict(symbol="circle", size=16, color="#1e3c72"),
            text=[f" 🏃 <b>Achille (A{to_subscript(str(curr_step))})</b>"],
            textposition="top right",
            textfont=dict(size=15, color="#1e3c72"),
            hoverinfo="none",
            showlegend=False,
            cliponaxis=False,
        )
    )

    fig_track.add_trace(
        go.Scatter(
            x=[T_val], y=[1],
            mode="markers+text",
            marker=dict(symbol="circle", size=14, color="#15803d"),
            text=[f" 🐢 <b>Tartaruga (T{to_subscript(str(curr_step))})</b>"],
            textposition="top right",
            textfont=dict(size=15, color="#15803d"),
            hoverinfo="none",
            showlegend=False,
            cliponaxis=False,
        )
    )

    fig_track.update_layout(
        xaxis=dict(
            title=dict(text="Coordinata sulla Retta Orientata (metri)", font=dict(size=15, color="#0f172a")),
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
        margin=dict(l=10, r=30, t=10, b=10),
        template="plotly_white",
        showlegend=False,
    )

    st.plotly_chart(fig_track, use_container_width=True)

with col_right:
    c_step_sub = to_subscript(str(curr_step))
    prev_step_sub = to_subscript(str(curr_step - 1)) if curr_step > 0 else "0"
    next_step_sub = to_subscript(str(curr_step + 1))

    if curr_step == 0:
        st.markdown(
            f"""
      <div class="athena-socratic-card">
          <h3>🏛️ Osservazioni (n = 0)</h3>
          <p><b>1. Configurazione Spaziale:</b> Achille occupa la posizione A₀ = 0. La Tartaruga occupa la posizione T₀, determinando il segmento di distacco iniziale A₀T₀.</p>
          <p><b>2. Distacco Iniziale Δs₀:</b> La misura del segmento residuo iniziale è Δs₀ = d(A₀;T₀) = {delta_s0_val} m.</p>
          <p><b>3. Relazione geometrica iterativa:</b> Per ogni step n, lo spostamento della Tartaruga ha misura tₙ = Δsₙ₋₁ / {r_denom}.</p>
          <div class="cognitive-conflict-box">
              <h4>🧠 Focus:</h4>
              <div class="conflict-text">
                  Per raggiungere la Tartaruga, concordi con Zenone che Achille debba prima di tutto compiere lo spostamento d₁ = Δs₀ = {delta_s0_val} m per giungere nel punto T₀ dove si trova ora la Tartaruga?
              </div>
          </div>
      </div>
      """,
            unsafe_allow_html=True,
        )
    else:
        d_str = format_frac_html(current_data["d"])
        t_str = format_frac_html(current_data["t"])
        delta_s_str = format_frac_html(current_data["delta_s"])

        somma_frazioni_list = [
            format_frac_html(df.iloc[k]["d"])
            for k in range(1, curr_step + 1)
        ]
        somma_frazioni_str = " + ".join(somma_frazioni_list)

        relazione_base = f"A₁ = T₀" if curr_step == 1 else f"A{c_step_sub} = T{to_subscript(str(curr_step - 1))}"

        st.markdown(
            f"""
      <div class="athena-socratic-card">
          <h3>🏛️ Athena: Guida Socratica - Passo n = {curr_step}</h3>
          <p><b>1. Spostamento di Achille:</b> Achille compie lo spostamento d{c_step_sub} (misura del segmento A{prev_step_sub}A{c_step_sub}) pari a <span class="fraction-badge">d{c_step_sub} = {d_str} m</span>, raggiungendo il punto geometrico A{c_step_sub} (coincidente con la precedente posizione T{prev_step_sub} della Tartaruga, applicando la relazione fondamentale <b>{relazione_base}</b>).</p>
          <p><b>2. Spostamento della Tartaruga:</b> Nello stesso step, la Tartaruga compie lo spostamento t{c_step_sub} (misura del segmento T{prev_step_sub}T{c_step_sub}) pari a <span class="fraction-badge">t{c_step_sub} = {t_str} m</span> (ottenuto come Δs{prev_step_sub} / {r_denom}), raggiungendo il punto geometrico T{c_step_sub}.</p>
          <p><b>3. Posizione Aₙ:</b><br>
          <div style="margin: 6px 0; padding: 8px 12px; background-color: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; font-family: monospace; font-size: 0.98rem;">
              <b>A{c_step_sub} = d₁ + ... + d{c_step_sub} = {somma_frazioni_str} = {format_frac_html(current_data['A'])} m</b>
          </div>
          </p>
          <p><b>4. Distacco Residuo Δsₙ:</b> Il segmento A{c_step_sub}T{c_step_sub} ha misura pari a <span class="fraction-badge">Δs{c_step_sub} = {delta_s_str} m</span>.</p>
          <div class="cognitive-conflict-box">
              <h4>🧠 Focus:</h4>
              <div class="conflict-text">
                  Per azzerare il distacco residuo Δs{c_step_sub} = {delta_s_str} m, concordi con Zenone che Achille debba ora compiere lo spostamento d{next_step_sub} = Δs{c_step_sub} = {delta_s_str} m per giungere nel punto T{c_step_sub}?
              </div>
          </div>
      </div>
      """,
            unsafe_allow_html=True,
        )

# ------------------------------------------------------------------------------
# 3. SCOMPOSIZIONE CUMULATA DEGLI SPOSTAMENTI
# ------------------------------------------------------------------------------
st.markdown(
    f"<div class='section-title'>📏 Aₙ = d₁ + d₂ + ... + dₙ (fino al passo n = {curr_step})</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='section-subtitle'>Posizione di Achille come somma dei segmenti percorsi: Aₙ = d₁ +"
    " d₂ + ... + dₙ</div>",
    unsafe_allow_html=True,
)

fig_segments = go.Figure()
palette = [
    "#2563eb", "#d97706", "#16a34a", "#dc2626", "#9333ea",
    "#0891b2", "#db2777", "#ca8a04", "#0284c7"
]

for k in range(1, curr_step + 1):
    d_val = df.iloc[k]["d_float"]
    d_frac_label = format_frac_html(df.iloc[k]["d"])
    color = palette[(k - 1) % len(palette)]
    k_sub = to_subscript(str(k))
    fig_segments.add_trace(
        go.Bar(
            y=["Spostamenti Achille"],
            x=[d_val],
            name=f"Spostamento d{k_sub} ({d_frac_label} m)",
            orientation="h",
            marker=dict(color=color),
            hoverinfo="name+x",
        )
    )

curr_step_sub = to_subscript(str(curr_step))

fig_segments.add_trace(
    go.Scatter(
        x=[T_val],
        y=["Spostamenti Achille"],
        mode="markers+text",
        marker=dict(symbol="circle", size=14, color="#15803d"),
        text=[f" 🐢 <b>Tartaruga (T{curr_step_sub})</b>"],
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
        title=dict(text="Posizione Aₙ (metri)", font=dict(size=14, color="#0f172a")),
        range=[0, max_x],
        tickfont=dict(size=12, color="#334155")
    ),
    yaxis=dict(visible=False),
    height=140,
    margin=dict(l=10, r=30, t=10, b=10),
    template="plotly_white",
    showlegend=True,
    legend=dict(font=dict(size=13))
)

st.plotly_chart(fig_segments, use_container_width=True)

# ------------------------------------------------------------------------------
# 4. TABELLA ANALITICA
# ------------------------------------------------------------------------------
st.markdown(
    "<div class='section-title'>📊 Tabella Analitica del Modello Geometrico</div>",
    unsafe_allow_html=True,
)

def highlight_current(row):
    if row["Passo n"] == st.session_state.step:
        return ["background-color: #dbeafe; font-weight: bold; color: #1e40af"] * len(
            row
        )
    return [""] * len(row)

# Formattazione formale della tabella a partire dai dati grezzi
display_data = []
for idx, row in df.iterrows():
    display_data.append({
        "Passo n": row["n"],
        "Punto Aₙ - coordinata sulla retta": f"{format_frac_html(row['A'])} m",
        "Misura dello spostamento dₙ": f"{format_frac_html(row['d'])} m",
        "Punto Tₙ - coordinata sulla retta": f"{format_frac_html(row['T'])} m",
        "Misura dello spostamento tₙ": f"{format_frac_html(row['t'])} m",
        "Distacco residuo Δsₙ": f"{format_frac_html(row['delta_s'])} m",
    })

df_display = pd.DataFrame(display_data)

columns_requested = [
    "Passo n",
    "Punto Aₙ - coordinata sulla retta",
    "Misura dello spostamento dₙ",
    "Punto Tₙ - coordinata sulla retta",
    "Misura dello spostamento tₙ",
    "Distacco residuo Δsₙ",
]

st.dataframe(
    df_display[columns_requested].style.apply(highlight_current, axis=1),
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
        Se la scomposizione logica di Zenone dimostra che Achille deve compiere una successione di infiniti spostamenti di misura positiva (dₙ > 0), ogni passo finito lascia inevitabilmente un distacco positivo Δsₙ > 0. Come fa la costruzione geometrica a svilupparsi senza che la misura del distacco residuo diventi mai esattamente zero in un numero finito di passi?
    </p>
</div>
""",
    unsafe_allow_html=True,
)
