from decimal import Decimal, getcontext
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Impostazione dell'elevata precisione decimale per preservare il paradosso
getcontext().prec = 50

# Configurazione della Pagina
st.set_page_config(
    page_title="Athena - Guida Socratica al Paradosso di Elea",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS: Design classico-greco moderno, responsive e ad alto impatto visivo
st.markdown(
    """
<style>
    .main { background-color: #f8fafc; }
    .stApp { font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    
    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e3c72 60%, #2a5298 100%);
        color: #ffffff;
        padding: 24px 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 24px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .hero-banner h1 {
        color: #ffffff;
        font-weight: 800;
        font-size: 2.1rem;
        margin-bottom: 6px;
        letter-spacing: -0.5px;
    }
    .hero-banner p {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 0;
    }
    
    /* Box Condizioni Iniziali */
    .init-conditions-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 6px solid #0284c7;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .init-conditions-card h4 {
        color: #0f172a;
        margin-top: 0;
        margin-bottom: 10px;
        font-size: 1.1rem;
        font-weight: 700;
    }
    
    /* Card Socratica Athena */
    .athena-socratic-card {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-left: 6px solid #1e3c72;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .athena-socratic-card h3 {
        color: #1e3c72;
        font-size: 1.25rem;
        margin-top: 0;
        margin-bottom: 12px;
    }
    
    /* Riquadro del Conflitto Cognitivo */
    .cognitive-conflict-box {
        background-color: #fffbeb;
        border: 1px solid #fef3c7;
        border-left: 6px solid #f59e0b;
        padding: 16px 20px;
        border-radius: 8px;
        margin-top: 16px;
        margin-bottom: 8px;
    }
    .cognitive-conflict-box h4 {
        color: #b45309;
        margin-top: 0;
        margin-bottom: 6px;
        font-size: 1.08rem;
        font-weight: 700;
    }
    .conflict-text {
        color: #78350f;
        font-weight: 600;
        font-size: 1.03rem;
        line-height: 1.5;
    }

    div[data-testid="stDataFrame"] { font-size: 0.85rem !important; }
    [data-testid="stMetricValue"] { font-size: 1.35rem !important; font-weight: 700; }
</style>
""",
    unsafe_allow_html=True,
)

# Header Athena
st.markdown(
    """
<div class="hero-banner">
    <h1>🏛️ Athena: Guida Socratica al Paradosso di Elea</h1>
    <p>Scomposizione logico-spaziale del movimento secondo la formulazione di Zenone</p>
</div>
""",
    unsafe_allow_html=True,
)

# Sidebar - Parametri puramente spaziali e relazionali
st.sidebar.header("⚙️ Impostazione della Pista")
d0_input = st.sidebar.number_input(
    "Vantaggio Iniziale Tartaruga (d₁ = T₀) [unità]:",
    value=100.0,
    step=10.0,
    min_value=1.0,
)
r_denom = st.sidebar.number_input(
    "Rapporto di contrazione dello spostamento (1/k):",
    value=10,
    min_value=2,
    max_value=100,
    step=1,
)
max_steps = st.sidebar.slider(
    "Numero di suddivisioni logiche (n):",
    min_value=1,
    max_value=20,
    value=15,
)

# Gestione Session State
if "step" not in st.session_state:
  st.session_state.step = 0

# Controlli di Navigazione
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
st.sidebar.markdown(f"**Passo Corrente:** n = {st.session_state.step}")

# Calcoli con Decimal
d0 = Decimal(str(d0_input))
r = Decimal("1") / Decimal(str(r_denom))

# Costruzione rigorosa della sequenza logica dei punti A_n, T_n e dei tratti d_n
steps_data = []
s_A = Decimal("0.0")
s_T = d0

for n in range(max_steps + 1):
  if n == 0:
    tratto_A = Decimal("0.0")
    tratto_T = Decimal("0.0")
    distacco = d0
  else:
    distacco_precedente = steps_data[n - 1]["Gap Decimal Raw"]
    tratto_A = distacco_precedente  # Achille raggiunge T_{n-1}
    tratto_T = tratto_A * r  # La tartaruga avanza proporzionalmente
    s_A += tratto_A
    s_T += tratto_T
    distacco = s_T - s_A

  formula_str = (
      f"{d0_input}" if n == 0 else f"{d0_input} · (1/{r_denom})^{n}"
  )

  steps_data.append({
      "Passo (n)": n,
      "Punto Achille (Aₙ)": f"{s_A:.6f}",
      "Tratto dₙ (Aₙ - Aₙ₋₁)": f"{tratto_A:.6e}" if n > 0 else "0",
      "Punto Tartaruga (Tₙ)": f"{s_T:.6f}",
      "Avanzamento (Tₙ - Tₙ₋₁)": f"{tratto_T:.6e}" if n > 0 else "0",
      "Formula Distacco": formula_str,
      "Distacco Residuo (Δsₙ)": f"{distacco:.6e}",
      "Gap Decimal Raw": distacco,
      "Tratto_A_raw": tratto_A,
      "Pos_A_float": float(s_A),
      "Pos_T_float": float(s_T),
  })

df = pd.DataFrame(steps_data)
curr_step = st.session_state.step
current_data = df.iloc[curr_step]

# --- 1. RIQUADRO CONDIZIONI INIZIALI ---
st.markdown(
    f"""
<div class="init-conditions-card">
    <h4>📋 Condizioni Iniziali della Sfida Logica (Passo n = 0)</h4>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 10px;">
        <span>🏃 <b>Posizione Iniziale Achille (A₀):</b> 0.000000</span>
        <span>🐢 <b>Vantaggio Iniziale Tartaruga (T₀ = d₁):</b> {d0_input} unità</span>
        <span>⚖️ <b>Rapporto Relazionale (r):</b> 1/{r_denom} (la tartaruga avanza di 1/{r_denom} di ogni tratto di Achille)</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Indicatori di Stato Spaziali
m1, m2, m3, m4 = st.columns(4)
with m1:
  st.metric("Passo Logico (n)", f"{int(current_data['Passo (n)'])}")
with m2:
  st.metric("Posizione Aₙ (Achille)", f"{current_data['Punto Achille (Aₙ)']}")
with m3:
  st.metric(
      "Posizione Tₙ (Tartaruga)", f"{current_data['Punto Tartaruga (Tₙ)']}"
  )
with m4:
  st.metric("Distacco Residuo Δsₙ", f"{current_data['Distacco Residuo (Δsₙ)']}")

# --- 2. GUIDA SOCRATICA ATHENA PASSO PASSO ---
st.markdown("---")

if curr_step == 0:
  st.markdown(
      f"""
    <div class="athena-socratic-card">
        <h3>🏛️ Athena: Stato Iniziale del Ragionamento (n = 0)</h3>
        <p><b>La Premessa di Zenone:</b> Achille è ai nastri di partenza al punto $A_0 = 0$. Alla Tartaruga viene concesso un vantaggio iniziale di $T_0 = {d0_input}$ unità di spazio.</p>
        <p><b>Stato Spaziale:</b> Nessun movimento si è ancora compiuto. Il distacco iniziale che separa i due corridori è esattamente il primo tratto $d_1 = {d0_input}$.</p>
        <div class="cognitive-conflict-box">
            <h4>❓ Quesito Socratico di Partenza:</h4>
            <div class="conflict-text">
                "Per poter raggiungere o superare la tartaruga, concordi con Zenone che Achille debba prima di tutto percorrere interamente il tratto d₁ per arrivare al punto T₀ dove la tartaruga si trova in questo preciso istante?"
            </div>
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )
else:
  tratto_a_val = current_data["Tratto dₙ (Aₙ - Aₙ₋₁)"]
  tratto_t_val = current_data["Avanzamento (Tₙ - Tₙ₋₁)"]
  gap_val = current_data["Distacco Residuo (Δsₙ)"]

  st.markdown(
      f"""
    <div class="athena-socratic-card">
        <h3>🏛️ Athena: Guida Socratica - Passo Logico n = {curr_step}</h3>
        <p><b>1. L'Azione di Achille:</b> Per azzerare il distacco del passo precedente, Achille percorre il tratto rettilineo <b>d_{curr_step} = {tratto_a_val}</b>, raggiungendo esattamente il punto $A_{curr_step}$ (che corrisponde al punto $T_{curr_step-1}$ occupato prima dalla tartaruga).</p>
        <p><b>2. Lo Spostamento della Tartaruga:</b> Nel medesimo intervallo di tempo logico, la tartaruga non rimane ferma: essa avanza dal punto $T_{curr_step-1}$ al nuovo punto $T_{curr_step}$, coprendo un ulteriore micro-tratto pari a <b>{tratto_t_val}</b> (ossia 1/{r_denom} del tratto $d_{curr_step}$).</p>
        <p><b>3. La Nuova Situazione Spaziale:</b> Achille è giunto dove si trovava la tartaruga, ma essa si trova ora più avanti in $T_{curr_step}$, lasciando un nuovo segmento residuo <code>Δs_{curr_step} = {gap_val}</code>.</p>
        <div class="cognitive-conflict-box">
            <h4>🧠 Il Cortocircuito Cognitivo al Passo {curr_step}:</h4>
            <div class="conflict-text">
                "Noti come questo nuovo distacco Δs_{curr_step} ({gap_val}), per quanto infinitesimo, sia <b>rigorosamente maggiore di zero</b>?<br><br>
                Se per ogni passo si genera sempre un nuovo segmento spaziale positivo che Achille deve obbligatoriamente coprire, quanti tratti rettilinei distinti d₁, d₂, d₃, ... dovrà compiere in totale?"
            </div>
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )

# --- 3. RAPPRESENTAZIONE DEI TRATTI RETTILINEI (d_1 + d_2 + ... + d_n) ---
st.subheader(
    f"📏 Scomposizione del Percorso di Achille nei Tratti Rettilinei (fino a n"
    f" = {curr_step})"
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
  tratto_val = float(df.iloc[k]["Tratto_A_raw"])
  color = palette[(k - 1) % len(palette)]
  fig_segments.add_trace(
      go.Bar(
          y=["Tratti di Achille"],
          x=[tratto_val],
          name=f"Tratto d_{k} ({tratto_val:.2e})",
          orientation="h",
          marker=dict(color=color),
          hoverinfo="name+x",
      )
  )

pos_T_curr = current_data["Pos_T_float"]
fig_segments.add_trace(
    go.Scatter(
        x=[pos_T_curr],
        y=["Tratti di Achille"],
        mode="markers+text",
        name=f"Tartaruga in T_{curr_step}",
        marker=dict(symbol="circle", size=15, color="#16a34a"),
        text=[f"🐢 T_{curr_step}"],
        textposition="top center",
    )
)

fig_segments.update_layout(
    barmode="stack",
    title=f"Somma discreta dei segmenti: S_{curr_step} = d₁ + d₂ + ... + d_{curr_step}",
    xaxis=dict(
        title="Distanza sulla Pista (unità di spazio)",
        range=[0, max(120, d0_input * 1.25)],
    ),
    yaxis=dict(visible=False),
    height=190,
    margin=dict(l=20, r=20, t=35, b=25),
    template="plotly_white",
    showlegend=True,
)

st.plotly_chart(fig_segments, use_container_width=True)

# --- 4. TABELLA ANALITICA COMPLETA ---
st.subheader("📊 Tabella Analitica dei Punti e dei Tratti (Discretizzazione)")


def highlight_current(row):
  if row["Passo (n)"] == st.session_state.step:
    return ["background-color: #e0f2fe; font-weight: bold; color: #0369a1"] * len(
        row
    )
  return [""] * len(row)


columns_to_show = [
    "Passo (n)",
    "Punto Achille (Aₙ)",
    "Tratto dₙ (Aₙ - Aₙ₋₁)",
    "Punto Tartaruga (Tₙ)",
    "Avanzamento (Tₙ - Tₙ₋₁)",
    "Formula Distacco",
    "Distacco Residuo (Δsₙ)",
]

st.dataframe(
    df[columns_to_show].style.apply(highlight_current, axis=1),
    use_container_width=True,
)

# Chiusura Maieutica Generatice di Tensione Epistemologica
st.markdown("---")
st.markdown(
    """
<div style="background-color: #fef2f2; border: 1px solid #fee2e2; border-left: 6px solid #ef4444; padding: 18px 20px; border-radius: 8px;">
    <h4 style="color: #991b1b; margin-top:0; font-weight: 700;">⚡ Il Nodo Filosofico ed Epistemologico di Elea:</h4>
    <p style="color: #7f1d1d; font-size: 1.05rem; font-weight: 500; margin-bottom: 0; line-height: 1.5;">
        "Se la scomposizione logica di Zenone dimostra che Achille deve percorrere una successione di <b>infiniti tratti rettilinei distinti (dₙ > 0)</b>, come fa la realtà del mondo sensibile a mostrare che la corsa si conclude e la tartaruga viene superata?"
    </p>
</div>
""",
    unsafe_allow_html=True,
)
