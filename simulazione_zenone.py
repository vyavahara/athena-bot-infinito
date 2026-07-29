from fractions import Fraction
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Configurazione della Pagina Streamlit
st.set_page_config(
    page_title="Athena - Laboratorio Socratico al Paradosso di Elea",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS per un'interfaccia elegante, chiara e ad alto valore didattico
st.markdown(
    """
<style>
    .main { background-color: #f8fafc; }
    .stApp { font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e3c72 60%, #2a5298 100%);
        color: #ffffff; padding: 22px 20px; border-radius: 12px;
        text-align: center; margin-bottom: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .hero-banner h1 { color: #ffffff; font-weight: 800; font-size: 2.0rem; margin-bottom: 4px; }
    .hero-banner p { color: #94a3b8; font-size: 1.0rem; margin-bottom: 0; }
    
    .init-conditions-card {
        background-color: #ffffff; border: 1px solid #e2e8f0;
        border-left: 6px solid #0284c7; border-radius: 10px;
        padding: 16px 20px; margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }
    .init-conditions-card h4 { color: #0f172a; margin-top: 0; margin-bottom: 8px; font-size: 1.05rem; }
    
    .athena-socratic-card {
        background-color: #ffffff; border: 1px solid #cbd5e1;
        border-left: 6px solid #1e3c72; border-radius: 10px;
        padding: 20px; margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }
    .athena-socratic-card h3 { color: #1e3c72; font-size: 1.2rem; margin-top: 0; }
    
    .fraction-badge {
        background-color: #f1f5f9; border: 1px solid #cbd5e1;
        padding: 4px 10px; border-radius: 6px; font-family: monospace;
        font-size: 1.0rem; font-weight: bold; color: #0f172a;
    }
    
    .cognitive-conflict-box {
        background-color: #fffbeb; border: 1px solid #fef3c7;
        border-left: 6px solid #f59e0b; padding: 16px 20px;
        border-radius: 8px; margin-top: 16px;
    }
    .cognitive-conflict-box h4 { color: #b45309; margin-top: 0; font-size: 1.05rem; }
    .conflict-text { color: #78350f; font-weight: 600; font-size: 1.02rem; line-height: 1.5; }

    div[data-testid="stDataFrame"] { font-size: 0.85rem !important; }
    [data-testid="stMetricValue"] { font-size: 1.3rem !important; font-weight: 700; }
</style>
""",
    unsafe_allow_html=True,
)

# Header Athena
st.markdown(
    """
<div class="hero-banner">
    <h1>🏛️ Athena: Guida Socratica al Paradosso di Elea</h1>
    <p>Laboratorio didattico di scomposizione logico-spaziale della corsa di Achille e la Tartaruga</p>
</div>
""",
    unsafe_allow_html=True,
)

# Sidebar - Impostazione dei Parametri Geometrici
st.sidebar.header("⚙️ Impostazione della Pista")
d0_val = st.sidebar.number_input(
    "Vantaggio Iniziale Tartaruga (T₀ = d₁) [unità]:",
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

# Gestione dello stato della navigazione
if "step" not in st.session_state:
  st.session_state.step = 0

col_btn1, col_btn2, col_btn3, _ = st.columns([1.2, 1.2, 1.2, 1.8])
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

# Calcolo rigoroso in frazioni matematiche esatte
d0_frac = Fraction(d0_val, 1)
r_frac = Fraction(1, r_denom)

steps_data = []
s_A_frac = Fraction(0, 1)
s_T_frac = d0_frac


def format_frac_html(f: Fraction) -> str:
  """Helper per rappresentare le frazioni in forma algebrica rigorosa."""
  if f.denominator == 1:
    return f"{f.numerator}"
  return f"{f.numerator}/{f.denominator}"


for n in range(max_steps + 1):
  if n == 0:
    tratto_A_frac = Fraction(0, 1)
    tratto_T_frac = Fraction(0, 1)
    distacco_frac = d0_frac
    formula_str = f"{d0_val}"
  else:
    distacco_precedente = steps_data[n - 1]["Distacco_Frac"]
    tratto_A_frac = distacco_precedente  # Achille raggiunge T_{n-1}
    tratto_T_frac = tratto_A_frac * r_frac  # La tartaruga avanza di 1/k
    s_A_frac += tratto_A_frac
    s_T_frac += tratto_T_frac
    distacco_frac = s_T_frac - s_A_frac
    formula_str = f"{d0_val} · (1/{r_denom})^{n}"

  steps_data.append({
      "Passo (n)": n,
      "Punto Achille (Aₙ) [Frazione]": format_frac_html(s_A_frac),
      "Tratto dₙ (Aₙ - Aₙ₋₁) [Frazione]": (
          format_frac_html(tratto_A_frac) if n > 0 else "0"
      ),
      "Punto Tartaruga (Tₙ) [Frazione]": format_frac_html(s_T_frac),
      "Avanzamento Tartaruga [Frazione]": (
          format_frac_html(tratto_T_frac) if n > 0 else "0"
      ),
      "Distacco Residuo (Δsₙ) [Frazione]": format_frac_html(distacco_frac),
      "Pos_A_float": float(s_A_frac),
      "Pos_T_float": float(s_T_frac),
      "Tratto_A_float": float(tratto_A_frac),
      "Distacco_Frac": distacco_frac,
      "Tratto_A_Frac": tratto_A_frac,
      "A_Frac": s_A_frac,
      "T_Frac": s_T_frac,
      "Formula": formula_str,
  })

df = pd.DataFrame(steps_data)
curr_step = st.session_state.step
current_data = df.iloc[curr_step]

# --- 1. CONDIZIONI INIZIALI PERMANENTI ---
st.markdown(
    f"""
<div class="init-conditions-card">
    <h4>📋 Condizioni Iniziali della Gara (Passo n = 0)</h4>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 10px;">
        <span>🏃 <b>Posizione Iniziale Achille (A₀):</b> 0</span>
        <span>🐢 <b>Vantaggio Iniziale Tartaruga (T₀ = d₁):</b> {d0_val} unità</span>
        <span>⚖️ <b>Rapporto Relazionale (r):</b> 1/{r_denom} del tratto di Achille</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Metric Banner con Frazioni
m1, m2, m3, m4 = st.columns(4)
with m1:
  st.metric("Passo Logico (n)", f"{int(current_data['Passo (n)'])}")
with m2:
  st.metric(
      "Posizione Aₙ (Achille)",
      f"{current_data['Punto Achille (Aₙ) [Frazione]']}",
  )
with m3:
  st.metric(
      "Posizione Tₙ (Tartaruga)",
      f"{current_data['Punto Tartaruga (Tₙ) [Frazione]']}",
  )
with m4:
  st.metric(
      "Distacco Residuo Δsₙ",
      f"{current_data['Distacco Residuo (Δsₙ) [Frazione]']}",
  )

# --- 2. SIMULAZIONE VISIVA DINAMICA DELLO SPOSTAMENTO SULLA PISTA ---
st.subheader(
    f"🏃🐢 Simulazione dello Spostamento sulla Pista al Passo n = {curr_step}"
)

fig_track = go.Figure()

pos_A_val = current_data["Pos_A_float"]
pos_T_val = current_data["Pos_T_float"]

# Retta spaziale (Pista)
max_x = max(d0_val * 1.3, pos_T_val * 1.1)
fig_track.add_shape(
    type="line",
    x0=0,
    y0=0,
    x1=max_x,
    y1=0,
    line=dict(color="#cbd5e1", width=6),
)

# Tratto d_n percorso da Achille nell'ultimo passo
if curr_step > 0:
  prev_A_val = df.iloc[curr_step - 1]["Pos_A_float"]
  fig_track.add_shape(
      type="line",
      x0=prev_A_val,
      y0=0,
      x1=pos_A_val,
      y1=0,
      line=dict(color="#2563eb", width=8),
  )

# Segmento del distacco residuo tra Achille e Tartaruga
fig_track.add_shape(
    type="line",
    x0=pos_A_val,
    y0=0,
    x1=pos_T_val,
    y1=0,
    line=dict(color="#dc2626", width=4, dash="dot"),
)

# Indicatore Achille
fig_track.add_trace(
    go.Scatter(
        x=[pos_A_val],
        y=[0],
        mode="markers+text",
        name="Achille (Aₙ)",
        marker=dict(symbol="triangle-right", size=22, color="#1e3c72"),
        text=[f"🏃 Achille A_{curr_step}"],
        textposition="top center",
    )
)

# Indicatore Tartaruga
fig_track.add_trace(
    go.Scatter(
        x=[pos_T_val],
        y=[0],
        mode="markers+text",
        name="Tartaruga (Tₙ)",
        marker=dict(symbol="circle", size=18, color="#16a34a"),
        text=[f"🐢 Tartaruga T_{curr_step}"],
        textposition="top center",
    )
)

fig_track.update_layout(
    xaxis=dict(
        title="Posizione sulla Retta Spaziale (unità)", range=[-5, max_x]
    ),
    yaxis=dict(visible=False, range=[-0.5, 0.8]),
    height=200,
    margin=dict(l=20, r=20, t=30, b=20),
    template="plotly_white",
    showlegend=False,
)

st.plotly_chart(fig_track, use_container_width=True)

# --- 3. ACCOMPAGNAMENTO DIDATTICO STRUTTURATO DI ATHENA ---
st.markdown("---")

if curr_step == 0:
  st.markdown(
      f"""
    <div class="athena-socratic-card">
        <h3>🏛️ Athena: Stato Iniziale del Ragionamento (n = 0)</h3>
        <p><b>1. La Configurazione Spaziale:</b> Achille si trova al punto di partenza $A_0 = 0$. Alla Tartaruga viene assegnato il vantaggio iniziale di $T_0 = {d0_val}$ unità.</p>
        <p><b>2. Il Primo Tratto d₁:</b> Il distacco iniziale che separa i due corridori è esattamente il tratto $d_1 = {d0_val}$. Nessun movimento si è ancora compiuto.</p>
        <div class="cognitive-conflict-box">
            <h4>❓ Quesito Socratico di Partenza:</h4>
            <div class="conflict-text">
                "Per raggiungere o superare la tartaruga, concordi con Zenone che Achille debba prima di tutto percorrere interamente il tratto d₁ = {d0_val} fino al punto T₀ dove la tartaruga si trova in questo preciso momento?"
            </div>
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )
else:
  tratto_a_frac_str = current_data["Tratto dₙ (Aₙ - Aₙ₋₁) [Frazione]"]
  tratto_t_frac_str = current_data["Avanzamento Tartaruga [Frazione]"]
  distacco_frac_str = current_data["Distacco Residuo (Δsₙ) [Frazione]"]

  # Costruzione algebrica della somma di frazioni
  somma_frazioni_list = [
      format_frac_html(df.iloc[k]["Tratto_A_Frac"])
      for k in range(1, curr_step + 1)
  ]
  somma_frazioni_str = " + ".join(somma_frazioni_list)

  st.markdown(
      f"""
    <div class="athena-socratic-card">
        <h3>🏛️ Athena: Guida Socratica - Passo Logico n = {curr_step}</h3>
        <p><b>1. L'Azione di Achille:</b> Per azzerare il distacco del passo precedente, Achille percorre il tratto rettilineo <span class="fraction-badge">d_{curr_step} = {tratto_a_frac_str}</span>, giungendo al punto $A_{curr_step}$ (che coincide con $T_{curr_step-1}$).</p>
        <p><b>2. Lo Spostamento della Tartaruga:</b> Nel medesimo tempo logico, la tartaruga avanza dal punto $T_{curr_step-1}$ al nuovo punto $T_{curr_step}$, coprendo la frazione <span class="fraction-badge">1/{r_denom}</span> di $d_{curr_step}$, ossia un tratto pari a <span class="fraction-badge">{tratto_t_frac_str}</span>.</p>
        <p><b>3. La Somma dei Tratti Accumulati:</b> Lo spazio totale percorso da Achille fino a questo passo è dato dalla somma dei singoli segmenti contigui:<br>
        <div style="margin: 10px 0; padding: 12px; background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; font-family: monospace;">
            <b>S_{curr_step} = d₁ + d₂ + ... + d_{curr_step} = {somma_frazioni_str} = {current_data['Punto Achille (Aₙ) [Frazione]']}</b>
        </div></p>
        <p><b>4. Il Distacco Residuo:</b> Achille ha coperto il segmento precedente, ma la tartaruga si trova ora nel punto $T_{curr_step}$, lasciando un distacco residuo pari a <span class="fraction-badge">Δs_{curr_step} = {distacco_frac_str}</span>.</p>
        <div class="cognitive-conflict-box">
            <h4>🧠 Il Cortocircuito Cognitivo al Passo {curr_step}:</h4>
            <div class="conflict-text">
                "Noti come la frazione che esprime il distacco residuo (Δs_{curr_step} = {distacco_frac_str}), per quanto infinitesima, sia <b>rigorosamente diversa da zero</b>?<br><br>
                Se per ogni passo $n$ la tartaruga genera sempre un nuovo segmento positivo che Achille deve obbligatoriamente coprire, quanti tratti rettilinei distinti d₁, d₂, d₃, ... dovrà percorrere Achille in totale?"
            </div>
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )

# --- 4. SCOMPOSIZIONE DEI TRATTI RETTILINEI (BARRE CUMULATE) ---
st.subheader(
    f"📏 Scomposizione dei Tratti Rettilinei di Achille (fino a n = {curr_step})"
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
  tratto_frac_label = df.iloc[k]["Tratto dₙ (Aₙ - Aₙ₋₁) [Frazione]"]
  color = palette[(k - 1) % len(palette)]
  fig_segments.add_trace(
      go.Bar(
          y=["Tratti Achille"],
          x=[tratto_val],
          name=f"Tratto d_{k} ({tratto_frac_label})",
          orientation="h",
          marker=dict(color=color),
          hoverinfo="name+x",
      )
  )

fig_segments.add_trace(
    go.Scatter(
        x=[pos_T_val],
        y=["Tratti Achille"],
        mode="markers+text",
        name=f"Tartaruga in T_{curr_step}",
        marker=dict(symbol="circle", size=14, color="#16a34a"),
        text=[f"🐢 T_{curr_step}"],
        textposition="top center",
    )
)

fig_segments.update_layout(
    barmode="stack",
    title=f"Successione dei segmenti percorsi: S_{curr_step} = d₁ + d₂ + ... + d_{curr_step}",
    xaxis=dict(
        title="Distanza sulla Pista (unità di spazio)", range=[0, max_x]
    ),
    yaxis=dict(visible=False),
    height=180,
    margin=dict(l=20, r=20, t=35, b=25),
    template="plotly_white",
    showlegend=True,
)

st.plotly_chart(fig_segments, use_container_width=True)

# --- 5. TABELLA ANALITICA COMPLETA IN FRAZIONI ---
st.subheader("📊 Tabella Analitica dei Punti e dei Tratti (In Frazioni Esatte)")


def highlight_current(row):
  if row["Passo (n)"] == st.session_state.step:
    return ["background-color: #e0f2fe; font-weight: bold; color: #0369a1"] * len(
        row
    )
  return [""] * len(row)


columns_to_show = [
    "Passo (n)",
    "Punto Achille (Aₙ) [Frazione]",
    "Tratto dₙ (Aₙ - Aₙ₋₁) [Frazione]",
    "Punto Tartaruga (Tₙ) [Frazione]",
    "Avanzamento Tartaruga [Frazione]",
    "Formula",
    "Distacco Residuo (Δsₙ) [Frazione]",
]

st.dataframe(
    df[columns_to_show].style.apply(highlight_current, axis=1),
    use_container_width=True,
)

# Chiusura Maieutica Generatrice della Tensione Epistemologica
st.markdown("---")
st.markdown(
    """
<div style="background-color: #fef2f2; border: 1px solid #fee2e2; border-left: 6px solid #ef4444; padding: 18px 20px; border-radius: 8px;">
    <h4 style="color: #991b1b; margin-top:0; font-weight: 700;">⚡ Il Cortocircuito Epistemologico di Elea:</h4>
    <p style="color: #7f1d1d; font-size: 1.05rem; font-weight: 500; margin-bottom: 0; line-height: 1.5;">
        "Se la scomposizione logica di Zenone dimostra che Achille deve percorrere una successione di <b>infiniti tratti rettilinei distinti (dₙ > 0)</b> espressi da frazioni sempre più piccole ma mai nulle, come fa l'esperienza reale del mondo sensibile a mostrare che la corsa si conclude e la tartaruga viene superata?"
    </p>
</div>
""",
    unsafe_allow_html=True,
)
