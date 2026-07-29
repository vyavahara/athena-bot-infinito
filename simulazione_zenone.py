from fractions import Fraction
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ------------------------------------------------------------------------------
# CONFIGURAZIONE PAGINA
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Athena - Laboratorio Socratico al Paradosso di Elea",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------------------
# CSS PERSONALIZZATO
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
        color: #ffffff; padding: 12px 16px; border-radius: 8px;
        text-align: center; margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .hero-banner h1 { color: #ffffff; font-weight: 800; font-size: 1.5rem; margin-bottom: 2px; }
    .hero-banner p { color: #94a3b8; font-size: 0.88rem; margin-bottom: 0; }
    
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
        border-left: 5px solid #f59e0b; padding: 8px 10px;
        border-radius: 6px; margin-top: 8px;
    }
    .cognitive-conflict-box h4 { color: #b45309; margin-top: 0; margin-bottom: 2px; font-size: 0.9rem; }
    .conflict-text { color: #78350f; font-weight: 600; font-size: 0.88rem; line-height: 1.35; }

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
    <h1>🏛️ Athena: Guida Socratica al Paradosso di Elea</h1>
    <p>Laboratorio didattico di scomposizione logico-spaziale della corsa di Achille e la Tartaruga</p>
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
# 1. CONDIZIONI INIZIALI
# ------------------------------------------------------------------------------
st.markdown(
    f"""
<div class="init-conditions-card">
    <h4>📋 Condizioni Iniziali della Gara (Passo n = 0)</h4>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 8px; font-size: 0.88rem;">
        <span>🏃 <b>Posizione Iniziale Achille (A₀):</b> 0 m</span>
        <span>🐢 <b>Vantaggio Iniziale Tartaruga (T₀ = d₁):</b> {d0_val} m</span>
        <span>⚡ <b>Velocità:</b> Achille corre <b>{r_denom} volte più veloce</b> della Tartaruga</span>
        <span>⚖️ <b>Rapporto Relazionale (r):</b> 1/{r_denom} (frazione dello spostamento compiuta dalla Tartaruga)</span>
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
      f"<div class='section-title'>🏃🐢 Piste Parallele e Posizione (n ="
      f" {curr_step})</div>",
      unsafe_allow_html=True,
  )

  fig_track = go.Figure()

  pos_A_val = current_data["Pos_A_float"]
  pos_T_val = current_data["Pos_T_float"]
  max_x = max(d0_val * 1.25, pos_T_val * 1.08)

  # Corsia Tartaruga (y = 1)
  fig_track.add_shape(
      type="line",
      x0=0,
      y0=1,
      x1=max_x,
      y1=1,
      line=dict(color="#bbf7d0", width=4),
  )
  # Corsia Achille (y = 0)
  fig_track.add_shape(
      type="line",
      x0=0,
      y0=0,
      x1=max_x,
      y1=0,
      line=dict(color="#bfdbfe", width=4),
  )

  # Marcatori notevoli con pedici Unicode
  for k in range(min(curr_step + 2, len(df))):
    pos_ak = df.iloc[k]["Pos_A_float"]
    if k == 0:
      label_k = "A₀ = 0"
    else:
      label_k = f"A{to_subscript(str(k))} = T{to_subscript(str(k-1))}"

    fig_track.add_trace(
        go.Scatter(
            x=[pos_ak],
            y=[0],
            mode="markers+text",
            marker=dict(symbol="line-ns", size=10, color="#64748b"),
            text=[f"| {label_k}"],
            textposition="bottom center",
            hoverinfo="none",
            showlegend=False,
        )
    )

  # Tratto d_n compiuto da Achille nell'ultimo scatto
  if curr_step > 0:
    prev_A_val = df.iloc[curr_step - 1]["Pos_A_float"]
    fig_track.add_shape(
        type="line",
        x0=prev_A_val,
        y0=0,
        x1=pos_A_val,
        y1=0,
        line=dict(color="#2563eb", width=6),
    )

  # Segmento orizzontale del Vantaggio Residuo
  fig_track.add_shape(
      type="line",
      x0=pos_A_val,
      y0=0.5,
      x1=pos_T_val,
      y1=0.5,
      line=dict(color="#dc2626", width=3, dash="dash"),
  )

  # Icona Achille (y = 0)
  fig_track.add_trace(
      go.Scatter(
          x=[pos_A_val],
          y=[0],
          mode="markers+text",
          name="Achille",
          marker=dict(symbol="triangle-right", size=18, color="#1e3c72"),
          text=[f"🏃 Achille (A{to_subscript(str(curr_step))})"],
          textposition="top center",
          showlegend=False,
      )
  )

  # Icona Tartaruga (y = 1)
  fig_track.add_trace(
      go.Scatter(
          x=[pos_T_val],
          y=[1],
          mode="markers+text",
          name="Tartaruga",
          marker=dict(symbol="circle", size=14, color="#16a34a"),
          text=[f"🐢 Tartaruga (T{to_subscript(str(curr_step))})"],
          textposition="top center",
          showlegend=False,
      )
  )

  fig_track.update_layout(
      xaxis=dict(
          title="Distanza sulla Retta Spaziale (metri)", range=[-5, max_x]
      ),
      yaxis=dict(
          tickvals=[0, 1],
          ticktext=["Corsia Achille", "Corsia Tartaruga"],
          range=[-0.5, 1.5],
      ),
      height=270,
      margin=dict(l=10, r=10, t=10, b=10),
      template="plotly_white",
      showlegend=False,
  )

  st.plotly_chart(fig_track, use_container_width=True)

with col_right:
  if curr_step == 0:
    st.markdown(
        f"""
      <div class="athena-socratic-card">
          <h3>🏛️ Athena: Osservazioni maieutiche (n = 0)</h3>
          <p><b>1. Configurazione Spaziale:</b> Achille è fermo al punto A₀ = 0 m. La Tartaruga parte con il vantaggio iniziale T₀ = {d0_val} m.</p>
          <p><b>2. Il Primo Tratto d₁:</b> Il distacco iniziale coincide con il segmento d₁ = {d0_val} m. Nessun movimento si è ancora compiuto.</p>
          <p><b>3. Relazione Cinematica:</b> Achille corre {r_denom} volte più veloce. Il rapporto r = 1/{r_denom} indica che la Tartaruga percorrerà un decimo della distanza di Achille nello stesso intervallo.</p>
          <div class="cognitive-conflict-box">
              <h4>❓ Quesito Socratico di Partenza:</h4>
              <div class="conflict-text">
                  "Per raggiungere la Tartaruga, concordi con Zenone che Achille debba prima di tutto percorrere il primo tratto d₁ = {d0_val} m per giungere in T₀ dove la Tartaruga si trova ora?"
              </div>
          </div>
      </div>
      """,
        unsafe_allow_html=True,
    )
  else:
    tratto_a_frac_str = current_data["Tratto percorso da Achille"]
    tratto_t_frac_str = format_frac_html(
        Fraction(current_data["Tratto_A_Frac"], r_denom)
    )
    distacco_frac_str = current_data["Vantaggio della tartaruga"]

    somma_frazioni_list = [
        format_frac_html(df.iloc[k]["Tratto_A_Frac"])
        for k in range(1, curr_step + 1)
    ]
    somma_frazioni_str = " + ".join(somma_frazioni_list)

    c_step_sub = to_subscript(str(curr_step))
    prev_step_sub = to_subscript(str(curr_step - 1))

    st.markdown(
        f"""
      <div class="athena-socratic-card">
          <h3>🏛️ Athena: Guida Socratica - Passo n = {curr_step}</h3>
          <p><b>1. Azione di Achille:</b> Achille copre il tratto <span class="fraction-badge">d{c_step_sub} = {tratto_a_frac_str} m</span>, giungendo in A{c_step_sub} (ex posizione T{prev_step_sub} della Tartaruga).</p>
          <p><b>2. Spostamento Tartaruga:</b> Nello stesso tempo, la Tartaruga avanza in T{c_step_sub}, coprendo il micro-tratto <span class="fraction-badge">{tratto_t_frac_str} m</span> (pari a 1/{r_denom} di d{c_step_sub}).</p>
          <p><b>3. Distanza Totale Accumulata Sₙ:</b><br>
          <div style="margin: 4px 0; padding: 6px 10px; background-color: #f8fafc; border: 1px solid #cbd5e1; border-radius: 4px; font-family: monospace; font-size: 0.88rem;">
              <b>S{c_step_sub} = d₁ + ... + d{c_step_sub} = {somma_frazioni_str} = {current_data['Posizione raggiunta da Achille']} m</b>
          </div>
          </p>
          <p><b>4. Vantaggio Residuo Δsₙ:</b> Vi è un nuovo segmento residuo pari a <span class="fraction-badge">Δs{c_step_sub} = {distacco_frac_str} m</span>.</p>
          <div class="cognitive-conflict-box">
              <h4>🧠 Cortocircuito Cognitivo al Passo {curr_step}:</h4>
              <div class="conflict-text">
                  "Il vantaggio residuo (Δs{c_step_sub} = {distacco_frac_str} m) è <b>rigorosamente diverso da zero</b>.<br>
                  Se ad ogni passo si genera un nuovo segmento positivo, quanti tratti d₁, d₂, d₃, ... dovrà compiere Achille in totale?"
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
    f"<div class='section-title'>📏 Scomposizione dei Tratti Rettilinei di Achille"
    f" (fino a n = {curr_step})</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='section-subtitle'>Successione dei segmenti percorsi: Sₙ = d₁ +"
    " d₂ + ... + dₙ</div>",
    unsafe_allow_html=True,
)

fig_segments = go.Figure()
palette = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#bcbd22",
    "#17becf",
]

for k in range(1, curr_step + 1):
  tratto_val = df.iloc[k]["Tratto_A_float"]
  tratto_frac_label = df.iloc[k]["Tratto percorso da Achille"]
  color = palette[(k - 1) % len(palette)]
  k_sub = to_subscript(str(k))
  fig_segments.add_trace(
      go.Bar(
          y=["Tratti Achille"],
          x=[tratto_val],
          name=f"d{k_sub} ({tratto_frac_label} m)",
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
        name=f"Tartaruga in T{curr_step_sub}",
        marker=dict(symbol="circle", size=12, color="#16a34a"),
        text=[f"🐢 T{curr_step_sub}"],
        textposition="top center",
        showlegend=True,
    )
)

fig_segments.update_layout(
    barmode="stack",
    xaxis=dict(title="Distanza sulla Pista (metri)", range=[0, max_x]),
    yaxis=dict(visible=False),
    height=130,
    margin=dict(l=10, r=10, t=10, b=10),
    template="plotly_white",
    showlegend=True,
)

st.plotly_chart(fig_segments, use_container_width=True)

# ------------------------------------------------------------------------------
# 4. TABELLA ANALITICA
# ------------------------------------------------------------------------------
st.markdown(
    "<div class='section-title'>📊 Tabella Analitica dei Punti e dei"
    " Tratti</div>",
    unsafe_allow_html=True,
)


def highlight_current(row):
  if row["Passo n"] == st.session_state.step:
    return ["background-color: #e0f2fe; font-weight: bold; color: #0369a1"] * len(
        row
    )
  return [""] * len(row)


columns_requested = [
    "Passo n",
    "Tratto percorso da Achille",
    "Posizione raggiunta da Achille",
    "Posizione della tartaruga",
    "Vantaggio della tartaruga",
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
<div style="background-color: #fef2f2; border: 1px solid #fee2e2; border-left: 5px solid #ef4444; padding: 10px 14px; border-radius: 6px; margin-top: 10px;">
    <h4 style="color: #991b1b; margin-top:0; font-weight: 700; font-size: 0.95rem;">⚡ Il Cortocircuito Epistemologico di Elea:</h4>
    <p style="color: #7f1d1d; font-size: 0.90rem; font-weight: 500; margin-bottom: 0; line-height: 1.35;">
        "Se la scomposizione logica di Zenone dimostra che Achille deve percorrere una successione di <b>infiniti tratti rettilinei distinti (dₙ > 0)</b> espressi da frazioni sempre più piccole ma mai nulle, come fa l'esperienza reale del mondo sensibile a mostrare che la corsa si conclude e la tartaruga viene superata?"
    </p>
</div>
""",
    unsafe_allow_html=True,
)
