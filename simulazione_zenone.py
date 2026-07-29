import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from decimal import Decimal, getcontext

# Impostiamo altissima precisione decimale (50 cifre)
getcontext().prec = 50

# Configurazione Pagina Streamlit
st.set_page_config(
    page_title="Il Paradosso di Zenone - Achille e la Tartaruga",
    page_icon="🐢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Stili CSS Personalizzati con Caratteri più Piccoli e Tabella Compatta
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 0.9rem;
    }
    .title-banner {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 16px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .title-banner h1 {
        color: #ffffff;
        font-weight: 700;
        font-size: 1.8rem;
        margin-bottom: 4px;
    }
    .title-banner p {
        color: #e0e6ed;
        font-size: 0.95rem;
        margin-bottom: 0;
    }
    .maieutic-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        border-radius: 8px;
        margin-top: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        font-size: 0.9rem;
    }
    .maieutic-box h3 {
        color: #856404;
        font-size: 1.15rem;
        margin-top: 0;
    }
    .formula-badge {
        background-color: #e3f2fd;
        border: 1px solid #90caf9;
        color: #0d47a1;
        padding: 6px 10px;
        border-radius: 6px;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        font-size: 0.85rem;
    }
    div[data-testid="stDataFrame"] {
        font-size: 0.82rem !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.3rem !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.8rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Banner di Titolo
st.markdown("""
<div class="title-banner">
    <h1>🏛️ Il Paradosso di Zenone: Achille e la Tartaruga</h1>
    <p>Simulazione Maieutica e Modellizzazione Discreta del Movimento</p>
</div>
""", unsafe_allow_html=True)

# Sidebar - Parametri della Simulazione
st.sidebar.header("⚙️ Parametri della Gara")
v_A = st.sidebar.number_input("Velocità Achille (v_A) [m/s]", value=10.0, step=1.0)
v_T = st.sidebar.number_input("Velocità Tartaruga (v_T) [m/s]", value=1.0, step=0.5)
d0 = st.sidebar.number_input("Vantaggio Iniziale Tartaruga (d0) [m]", value=100.0, step=10.0)

max_steps = st.sidebar.slider("Numero di passi da esplorare (n)", min_value=1, max_value=20, value=15)

# Inizializzazione Session State per il Passo Corrente
if 'step' not in st.session_state:
    st.session_state.step = 0

# Pulsanti di Controllo
col_btn1, col_btn2, col_btn3, col_btn4 = st.columns([1, 1, 1, 2])
with col_btn1:
    if st.button("⏮️ Reset"):
        st.session_state.step = 0
with col_btn2:
    if st.button("◀️ Passo Indietro") and st.session_state.step > 0:
        st.session_state.step -= 1
with col_btn3:
    if st.button("▶️ Passo Successivo") and st.session_state.step < max_steps:
        st.session_state.step += 1

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Passo Attuale:** n = {st.session_state.step}")

# Rapporto di contrazione
ratio_dec = Decimal(str(v_T)) / Decimal(str(v_A))

# Calcolo dei dati per tutti i passi
steps_data = []

s_A_dec = Decimal('0.0')
s_T_dec = Decimal(str(d0))
t_total_dec = Decimal('0.0')
gap_prev = Decimal(str(d0))

for n in range(max_steps + 1):
    gap_dec = Decimal(str(d0)) * (ratio_dec ** Decimal(n))
    
    # Formula analitica
    if n == 0:
        formula_str = f"{d0}"
    else:
        formula_str = f"{d0} · ({v_T}/{v_A})^{n}"
    
    # Calcolo dei tratti percorsi e tempo del singolo passo Δt
    if n == 0:
        dt_step = Decimal('0.0')
        tratto_A = Decimal('0.0')
        tratto_T = Decimal('0.0')
        dt_str = "0"
        tratto_A_str = "0"
        tratto_T_str = "0"
    else:
        dt_step = gap_prev / Decimal(str(v_A))
        tratto_A = gap_prev  # Achille percorre il gap precedente
        tratto_T = Decimal(str(v_T)) * dt_step  # La tartaruga percorre v_T * dt
        dt_str = f"{dt_step:.6e}"
        tratto_A_str = f"{tratto_A:.6e}"
        tratto_T_str = f"{tratto_T:.6e}"

    steps_data.append({
        'Passo': n,
        'Nel tempo t (s)': dt_str,
        'Tratto percorso da Achille (m)': tratto_A_str,
        'Posizione di Achille (m)': f"{s_A_dec:.6f}",
        'Tratto percorso dalla tartaruga (m)': tratto_T_str,
        'Posizione della Tartaruga (m)': f"{s_T_dec:.6f}",
        'Formula GAP': formula_str,
        'GAP Esponenziale (m)': f"{gap_dec:.6e}",
        'Gap Decimal Raw': gap_dec,
        'Pos_A_float': float(s_A_dec),
        'Pos_T_float': float(s_T_dec)
    })
    
    # Salviamo il gap attuale per il passo successivo
    gap_prev = gap_dec
    
    # Preparazione variabili per lo step n+1
    dt_next = gap_dec / Decimal(str(v_A))
    t_total_dec += dt_next
    s_A_dec = s_T_dec
    s_T_dec = s_T_dec + Decimal(str(v_T)) * dt_next

df = pd.DataFrame(steps_data)
current_data = df.iloc[st.session_state.step]

# Indicatori di Stato Principali
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Passo n", f"{int(current_data['Passo'])}")
with m2:
    st.metric("Posizione Achille", f"{current_data['Posizione di Achille (m)']} m")
with m3:
    st.metric("Posizione Tartaruga", f"{current_data['Posizione della Tartaruga (m)']} m")
with m4:
    st.metric("GAP Residuo Δs", f"{current_data['GAP Esponenziale (m)']} m")

st.markdown(f"**Formula del GAP al passo n = {st.session_state.step}:** <span class='formula-badge'>Δs = {current_data['Formula GAP']} m = {current_data['GAP Esponenziale (m)']} m</span>", unsafe_allow_html=True)

st.write("")

# VISUALIZZAZIONE GRAFICA INTERATTIVA (PLOTLY)
fig = go.Figure()

# Grafico 1: Vista Globale della Pista
fig.add_trace(go.Scatter(
    x=[current_data['Pos_A_float']], y=[1],
    mode='markers+text',
    name='Achille 🏃',
    marker=dict(symbol='triangle-right', size=20, color='#1f77b4'),
    text=["Achille"], textposition="top center"
))

fig.add_trace(go.Scatter(
    x=[current_data['Pos_T_float']], y=[1],
    mode='markers+text',
    name='Tartaruga 🐢',
    marker=dict(symbol='circle', size=16, color='#2ca02c'),
    text=["Tartaruga"], textposition="top center"
))

fig.add_shape(
    type="line",
    x0=current_data['Pos_A_float'], y0=1,
    x1=current_data['Pos_T_float'], y1=1,
    line=dict(color="red", width=3, dash="dot")
)

fig.update_layout(
    title=f"Rappresentazione Spaziale Globale al Passo n = {st.session_state.step}",
    xaxis=dict(title="Posizione sulla Pista (metri)", range=[-5, max(120, d0 * 1.25)]),
    yaxis=dict(visible=False, range=[0.5, 1.5]),
    height=180,
    margin=dict(l=20, r=20, t=35, b=25),
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Vista "Lente d'Ingrandimento" (Zoom sul GAP)
fig_zoom = go.Figure()

gap_val = float(current_data['Gap Decimal Raw'])
display_gap = gap_val if gap_val > 0 else 1e-15
pos_A = current_data['Pos_A_float']
pos_T = current_data['Pos_T_float']

fig_zoom.add_trace(go.Scatter(
    x=[0], y=[1],
    mode='markers+text',
    name='Achille',
    marker=dict(symbol='triangle-right', size=22, color='#1f77b4'),
    text=[f"Achille ({pos_A:.6f} m)"], textposition="bottom center"
))

fig_zoom.add_trace(go.Scatter(
    x=[display_gap], y=[1],
    mode='markers+text',
    name='Tartaruga',
    marker=dict(symbol='circle', size=18, color='#2ca02c'),
    text=[f"Tartaruga ({pos_T:.6f} m)"], textposition="bottom center"
))

fig_zoom.add_shape(
    type="line",
    x0=0, y0=1,
    x1=display_gap, y1=1,
    line=dict(color="crimson", width=5)
)

fig_zoom.update_layout(
    title=f"🔍 Lente d'Ingrandimento sul GAP Spaziale Residuo (Δs = {current_data['Formula GAP']} m)",
    xaxis=dict(title="Distanza Relativa da Achille (metri)", range=[-display_gap*0.2, display_gap*1.2]),
    yaxis=dict(visible=False, range=[0.5, 1.5]),
    height=200,
    margin=dict(l=20, r=20, t=35, b=25),
    template="plotly_white"
)

st.plotly_chart(fig_zoom, use_container_width=True)

# TABELLA DELLE POSIZIONI E DEL GAP CON TUTTE LE COLONNE RICHIESTE
st.subheader("📊 Tabella Analitica dei Passi (Logica Discreta di Zenone)")

# Evidenzia la riga corrente
def highlight_current(row):
    if row['Passo'] == st.session_state.step:
        return ['background-color: #d1ecf1; font-weight: bold'] * len(row)
    return [''] * len(row)

columns_to_show = [
    'Passo', 
    'Nel tempo t (s)', 
    'Tratto percorso da Achille (m)', 
    'Posizione di Achille (m)', 
    'Tratto percorso dalla tartaruga (m)', 
    'Posizione della Tartaruga (m)', 
    'Formula GAP',
    'GAP Esponenziale (m)'
]

display_df = df[columns_to_show].copy()

st.dataframe(display_df.style.apply(highlight_current, axis=1), use_container_width=True)

# BOX MAIEUTICO
st.markdown("""
<div class="maieutic-box">
    <h3>🤔 Riflessione </h3>
    <p><b>Osserva la struttura della tabella:</b> ad ogni passo $n$, Achille copre esattamente il <i>GAP del passo precedente</i>, mentre la tartaruga avanza di un ulteriore micro-tratto nello stesso intervallo di tempo $\Delta t$.</p>
    <p>La formula del GAP rimane della forma $100 \cdot \left(\frac{1}{10}\right)^n$, garantendo che per ogni $n$ finito tutti gli intervalli e il distacco siano <b>rigorosamente maggiori di zero</b> ($\Delta t > 0$, $\Delta s > 0$).</p>
    <hr style="border-top: 1px solid #ffe8a1;">
    <h4 style="color: #856404; text-align: center;">🎯 Domanda Chiave per la Classe:</h4>
    <p style="font-size: 1.1rem; font-weight: bold; text-align: center; color: #533f03;">
        "Se la somma dei singoli intervalli temporali $\Delta t$ e dei tratti percorsi forma una successione infinita di addendi strettamente positivi, come può il tempo totale e la distanza totale rimanere finiti consentendo ad Achille di raggiungere la tartaruga?"
    </p>
</div>
""", unsafe_allow_html=True)

# SCARICAMENTO DATI
csv_data = display_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Scarica la Tabella dei Dati (CSV)",
    data=csv_data,
    file_name="simulazione_zenone_completa.csv",
    mime="text/csv"
)
