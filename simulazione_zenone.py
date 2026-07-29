import asyncio
from fractions import Fraction
from io import BytesIO

import edge_tts
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Configurazione della Pagina Streamlit con layout compatto
st.set_page_config(
    page_title="Athena - Laboratorio Socratico al Paradosso di Elea",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS per ridurre le interlinee e ottimizzare l'impatto visivo
st.markdown(
    """
<style>
    .main { background-color: #f8fafc; }
    .stApp { font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    
    /* Riduzione interlinee e padding generali */
    .block-container { padding-top: 1.2rem; padding-bottom: 1.2rem; }
    p { margin-bottom: 0.5rem; line-height: 1.4; }
    
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e3c72 60%, #2a5298 100%);
        color: #ffffff; padding: 16px 18px; border-radius: 10px;
        text-align: center; margin-bottom: 14px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .hero-banner h1 { color: #ffffff; font-weight: 800; font-size: 1.7rem; margin-bottom: 2px; }
    .hero-banner p { color: #94a3b8; font-size: 0.95rem; margin-bottom: 0; }
    
    .init-conditions-card {
        background-color: #ffffff; border: 1px solid #e2e8f0;
        border-left: 6px solid #0284c7; border-radius: 8px;
        padding: 12px 16px; margin-bottom: 14px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    .init-conditions-card h4 { color: #0f172a; margin-top: 0; margin-bottom: 6px; font-size: 1.0rem; font-weight: 700; }
    
    .athena-socratic-card {
        background-color: #ffffff; border: 1px solid #cbd5e1;
        border-left: 6px solid #1e3c72; border-radius: 8px;
        padding: 16px; margin-bottom: 14px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    .athena-socratic-card h3 { color: #1e3c72; font-size: 1.12rem; margin-top: 0; margin-bottom: 8px; }
    
    .fraction-badge {
        background-color: #f1f5f9; border: 1px solid #cbd5e1;
        padding: 2px 8px; border-radius: 4px; font-family: monospace;
        font-size: 0.95rem; font-weight: bold; color: #0f172a;
    }
    
    .cognitive-conflict-box {
        background-color: #fffbeb; border: 1px solid #fef3c7;
        border-left: 6px solid #f59e0b; padding: 12px 16px;
        border-radius: 6px; margin-top: 12px; margin-bottom: 6px;
    }
    .cognitive-conflict-box h4 { color: #b45309; margin-top: 0; margin-bottom: 4px; font-size: 1.0rem; }
    .conflict-text { color: #78350f; font-weight: 600; font-size: 0.98rem; line-height: 1.4; }

    div[data-testid="stDataFrame"] { font-size: 0.82rem !important; }
    [data-testid="stMetricValue"] { font-size: 1.2rem !important; font-weight: 700; }
</style>
""",
    unsafe_allow_html=True,
)


# Helper per la sintesi vocale di Athena
def genera_audio_athena(testo: str) -> BytesIO:
  """Genera l'audio in mp3 per le osservazioni di Athena."""

  async def _tts():
    communicate = edge_tts.Communicate(
        testo, voice="it-IT-ElsaNeural", rate="+0%"
    )
    data = b""
    async for chunk in communicate.stream():
      if chunk["type"] == "audio":
        data += chunk["data"]
    return data

  audio_bytes = asyncio.run(_tts())
  return BytesIO(audio_bytes)


# Header dell'App
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
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 12px; font-size: 0.92rem;">
        <span>🏃 <b>Posizione Iniziale Achille (A₀):</b> 0 m</span>
        <span>🐢 <b>Vantaggio Iniziale Tartaruga (T₀ = d₁):</b> {d0_val} m</span>
        <span>⚡ <b>Velocità:</b> Achille corre <b>10 volte più veloce</b> della Tartaruga</span>
        <span>⚖️ <b>Rapporto Relazionale (r):</b> 1/{r_denom} (frazione dello spostamento di Achille compiuta dalla Tartaruga)</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Metric Banner con pedici Unicode corretti
m1, m2, m3, m4 = st.columns(4)
with m1:
  st.metric("Passo Logico (n)", f"{int(current_data['Passo (n)'])}")
with m2:
  st.metric(
      "Posizione Aₙ (Achille)",
      f"{current_data['Punto Achille (Aₙ) [Frazione]']} m",
  )
with m3:
  st.metric(
      "Posizione Tₙ (Tartaruga)",
      f"{current_data['Punto Tartaruga (Tₙ) [Frazione]']} m",
  )
with m4:
  st.metric(
      "Distacco Residuo Δsₙ",
      f"{current_data['Distacco Residuo (Δsₙ) [Frazione]']} m",
  )

# --- 2. SIMULAZIONE VISIVA DINAMICA DELLA PISTA (Struttura Punto 1 & Immagine) ---
st.subheader(
    f"🏃🐢 Rappresentazione Spaziale della Pista al Passo n = {curr_step}"
)

fig_track = go.Figure()

pos_A_val = current_data["Pos_A_float"]
pos_T_val = current_data["Pos_T_float"]

# Retta spaziale (Pista)
max_x = max(d0_val * 1.25, pos_T_val * 1.08)
fig_track.add_shape(
    type="line",
    x0=0,
    y0=0,
    x1=max_x,
    y1=0,
    line=dict(color="#cbd5e1", width=6),
)

# Tracciamento dei punti notevoli esatti sulla retta (A₀, T₀=A₁, T₁=A₂, ecc.)
for k in range(min(curr_step + 2, len(df))):
  pos_ak = df.iloc[k]["Pos_A_float"]
  label_k = f"A₀ = 0" if k == 0 else f"A_{k} = T_{k-1}"
  fig_track.add_trace(
      go.Scatter(
          x=[pos_ak],
          y=[0],
          mode="markers+text",
          marker=dict(symbol="line-ns", size=14, color="#64748b"),
          text=[f"| {label_k}"],
          textposition="bottom center",
          hoverinfo="none",
      )
  )

# Segmento d_n percorso da Achille nell'ultimo passo
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
    xaxis=dict(title="Posizione sulla Retta Spaziale (metri)", range=[-5, max_x]),
    yaxis=dict(visible=False, range=[-0.6, 0.8]),
    height=190,
    margin=dict(l=20, r=20, t=25, b=20),
    template="plotly_white",
    showlegend=False,
)

st.plotly_chart(fig_track, use_container_width=True)

# --- 3. ACCOMPAGNAMENTO DIDATTICO STRUTTURATO DI ATHENA ---
st.markdown("---")

if curr_step == 0:
  testo_athena_audio = (
      f"Benvenuti al punto di partenza. Achille si trova in A₀ uguale a 0 metri,"
      f" mentre la Tartaruga ha un vantaggio iniziale di T₀ uguale a {d0_val} metri."
      f" Poiché Achille corre 10 volte più veloce della Tartaruga, per"
      f" raggiungerla deve prima percorrere interamente questo tratto iniziale"
      f" d₁ di {d0_val} metri. Riuscirà a superarla?"
  )

  st.markdown(
      f"""
    <div class="athena-socratic-card">
        <h3>🏛️ Athena: Osservazioni maieutiche sulle Condizioni Iniziali (n = 0)</h3>
        <p><b>1. Configurazione Spaziale di Partenza:</b> Achille è fermo al punto A₀ = 0 m. Alla Tartaruga viene assegnato il vantaggio iniziale T₀ = {d0_val} m.</p>
        <p><b>2. Il Primo Tratto d₁:</b> Il distacco iniziale tra i due corridori coincide esattamente con il segmento d₁ = {d0_val} m. Nessun movimento si è ancora compiuto.</p>
        <p><b>3. Relazione Cinematica:</b> Sapendo che Achille corre 10 volte più veloce della Tartaruga, il rapporto relazionale r = 1/{r_denom} indica che la Tartaruga percorrerà un decimo della distanza coperta da Achille nello stesso intervallo logico.</p>
        <div class="cognitive-conflict-box">
            <h4>❓ Quesito Socratico di Partenza:</h4>
            <div class="conflict-text">
                "Per poter raggiungere la Tartaruga, concordi con Zenone che Achille debba prima di tutto percorrere interamente il primo tratto d₁ = {d0_val} m per giungere al punto T₀ dove la Tartaruga si trova in questo istante?"
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

  testo_athena_audio = (
      f"Al passo logico n uguale a {curr_step}, Achille percorre il tratto d_{curr_step}"
      f" pari a {tratto_a_frac_str} metri e giunge dove si trovava prima la"
      " Tartaruga. Nello stesso tempo la Tartaruga avanza di"
      f" {tratto_t_frac_str} metri fino a T_{curr_step}. La somma totale"
      f" percorsa finora da Achille è S_{curr_step} pari a"
      f" {current_data['Punto Achille (Aₙ) [Frazione]']} metri. Il nuovo"
      f" distacco residuo è pari a {distacco_frac_str} metri, che è piccolo ma"
      " rigorosamente diverso da zero!"
  )

  st.markdown(
      f"""
    <div class="athena-socratic-card">
        <h3>🏛️ Athena: Guida Socratica - Passo Logico n = {curr_step}</h3>
        <p><b>1. L'Azione di Achille:</b> Per annullare il distacco precedente, Achille compie lo scatto coprendo il tratto rettilineo <span class="fraction-badge">d_{curr_step} = {tratto_a_frac_str} m</span>, giungendo esattamente al punto A_{curr_step} (che coincide con la posizione T_{curr_step-1} occupata in precedenza dalla Tartaruga).</p>
        <p><b>2. Lo Spostamento della Tartaruga:</b> Durante questo medesimo intervallo, la Tartaruga non rimane immobile: essa avanza dal punto T_{curr_step-1} al nuovo punto T_{curr_step}, coprendo una frazione pari a <span class="fraction-badge">1/{r_denom}</span> del tratto d_{curr_step}, ossia un micro-spostamento di <span class="fraction-badge">{tratto_t_frac_str} m</span>.</p>
        <p><b>3. La Somma dei Tratti Accumulati (Distanza Totale Percorsa Sₙ):</b><br>
        La quantità S_{curr_step} rappresenta la <i>distanza totale accumulata da Achille sulla pista dal momento della partenza</i>. Essa non viene fornita come un blocco unico, ma si costruisce sommando uno per uno i singoli tratti rettilinei compiuti ad ogni scatto:<br>
        <div style="margin: 10px 0; padding: 10px 14px; background-color: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; font-family: monospace; font-size: 1.0rem;">
            <b>S_{curr_step} = d₁ + d₂ + ... + d_{curr_step} = {somma_frazioni_str} = {current_data['Punto Achille (Aₙ) [Frazione]']} m</b>
        </div>
        <i>Rifletti: ad ogni passo si aggiunge un addendo dₙ sempre più piccolo. La somma parziale Sₙ cresce ad ogni scatto, ma si accumula avvicinandosi a una soglia senza superarla in un numero finito di passaggi.</i>
        </p>
        <p><b>4. Il Distacco Residuo Δsₙ:</b> Achille ha raggiunto la posizione precedente della Tartaruga, ma la Tartaruga si trova ora più avanti nel punto T_{curr_step}, lasciando un distacco residuo pari a <span class="fraction-badge">Δs_{curr_step} = {distacco_frac_str} m</span>.</p>
        <div class="cognitive-conflict-box">
            <h4>🧠 Il Cortocircuito Cognitivo al Passo {curr_step}:</h4>
            <div class="conflict-text">
                "Noti come la frazione che esprime il distacco residuo (Δs_{curr_step} = {distacco_frac_str} m), per quanto infinitesima, sia <b>rigorosamente diversa da zero</b>?<br><br>
                Se ad ogni passo la Tartaruga genera sempre un nuovo segmento positivo che Achille deve obbligatoriamente coprire, quanti tratti rettilinei distinti d₁, d₂, d₃, ... dovrà percorrere Achille in totale?"
            </div>
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )

# Lettore Audio per le Osservazioni di Athena (Indicazione 6)
col_aud1, col_aud2 = st.columns([1, 4])
with col_aud1:
  if st.button(
      f"🔊 Ascolta Athena (Passo n = {curr_step})", key=f"audio_btn_{curr_step}"
  ):
    audio_data = genera_audio_athena(testo_athena_audio)
    st.audio(audio_data, format="audio/mp3")

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
          name=f"Tratto d_{k} ({tratto_frac_label} m)",
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
    xaxis=dict(title="Distanza sulla Pista (metri)", range=[0, max_x]),
    yaxis=dict(visible=False),
    height=170,
    margin=dict(l=20, r=20, t=30, b=20),
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

# --- 6. CHIUSURA MAIEUTICA ED AUDIO FINALE ---
st.markdown("---")

testo_cortocircuito = (
    "Il Cortocircuito Epistemologico di Elea. Se la scomposizione logica di"
    " Zenone dimostra che Achille deve percorrere una successione di infiniti"
    " tratti rettilinei distinti dₙ maggiori di zero espressi da frazioni"
    " sempre più piccole ma mai nulle, come fa l'esperienza reale del mondo"
    " sensibile a mostrare che la corsa si conclude e la tartaruga viene"
    " superata?"
)

st.markdown(
    """
<div style="background-color: #fef2f2; border: 1px solid #fee2e2; border-left: 6px solid #ef4444; padding: 16px 18px; border-radius: 8px;">
    <h4 style="color: #991b1b; margin-top:0; font-weight: 700;">⚡ Il Cortocircuito Epistemologico di Elea:</h4>
    <p style="color: #7f1d1d; font-size: 1.02rem; font-weight: 500; margin-bottom: 0; line-height: 1.4;">
        "Se la scomposizione logica di Zenone dimostra che Achille deve percorrere una successione di <b>infiniti tratti rettilinei distinti (dₙ > 0)</b> espressi da frazioni sempre più piccole ma mai nulle, come fa l'esperienza reale del mondo sensibile a mostrare che la corsa si conclude e la tartaruga viene superata?"
    </p>
</div>
""",
    unsafe_allow_html=True,
)

col_aud_fin1, col_aud_fin2 = st.columns([1, 4])
with col_aud_fin1:
  if st.button("🔊 Ascolta il Cortocircuito", key="audio_final_btn"):
    audio_final_data = genera_audio_athena(testo_cortocircuito)
    st.audio(audio_final_data, format="audio/mp3")
