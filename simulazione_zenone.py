import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from decimal import Decimal, getcontext

# Impostiamo altissima precisione decimale per evitare l'arrotondamento a zero a floating point (fino a 50 cifre)
getcontext().prec = 50

# Configurazione Pagina Streamlit
st.set_page_config(
    page_title="Il Paradosso di Zenone - Achille e la Tartaruga",
    page_icon="🐢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Stili CSS Personalizzati per un'Estetica Accattivante e Professionale
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .title-banner {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 24px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .title-banner h1 {
        color: #ffffff;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .title-banner p {
        color: #e0e6ed;
        font-size: 1.1rem;
    }
    .maieutic-box {
        background-color: #fff3cd;
        border-left: 6px solid #ffc107;
        padding: 20px;
        border-radius: 8px;
        margin-top: 25px;
        margin-bottom: 25px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .maieutic-box h3 {
        color: #856404;
        margin-top: 0;
    }
    .formula-badge {
        background-color: #e3f2fd;
        border: 1px solid #90caf9;
        color: #0d47a1;
        padding: 8px 12px;
        border-radius: 6px;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
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

max_steps = st.sidebar.slider("Numero di Passi da Esplorare (n)", min_value=1, max_value=20, value=15)

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

# Rapporto di contrazione k = v_T / v_A
ratio = v_T / v_A
ratio_dec = Decimal(str(v_T)) / Decimal(str(v_A))

# Calcolo dei dati per tutti i passi usando sia Decimal (alta precisione) che stringhe di formule simboliche
steps_data = []
s_A_dec = Decimal('0.0')
s_T_dec = Decimal(str(d0))
t_total_dec = Decimal('0.0')

for n in range(max_steps + 1):
    gap_dec = Decimal(str(d0)) * (ratio_dec ** Decimal(n))
    
    # Costruzione della formula simbolica non sviluppata
    if n == 0:
        formula_str = f"{d0}"
    else:
        formula_str = f"{d0} · ({v_T}/{v_A})^{n}"
    
    # Formattazione scientifica senza perdita di precisione per n elevati
    # Sfruttiamo Decimal per evitare che la rappresentazione IEEE 754 float porti a 0.0
    gap_float = float(gap_dec)
    
    steps_data.append({
        'Passo (n)': n,
        'Tempo Totale (s)': float(t_total_dec),
        'Posizione Achille s_A (m)': float(s_A_dec),
        'Posizione Tartaruga s_T (m)': float(s_T_dec),
        'Formula Analitica Non Sviluppata': formula_str,
        'Gap Δs (m, Decimal)': gap_dec,
        'GAP Esponenziale': f"{gap_dec:.6e}" if gap_dec != 0 else f"{d0}·({ratio})^{n}"
    })
    
    # Prossimo passo secondo la logica di Zenone
    dt_dec = gap_dec / Decimal(str(v_A))
    t_total_dec += dt_dec
    s_A_dec = s_T_dec
    s_T_dec = s_T_dec + Decimal(str(v_T)) * dt_dec

df = pd.DataFrame(steps_data)
current_data = df.iloc[st.session_state.step]

# Indicatori di Stato
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Passo n", f"{int(current_data['Passo (n)'])}")
with m2:
    st.metric("Posizione Achille", f"{current_data['Posizione Achille s_A (m)']:.6f} m")
with m3:
    st.metric("Posizione Tartaruga", f"{current_data['Posizione Tartaruga s_T (m)']:.6f} m")
with m4:
    st.metric("GAP Residuo Δs (Notazione)", f"{current_data['GAP Esponenziale']} m")

st.markdown(f"**Formula del GAP al passo n = {st.session_state.step}:** <span class='formula-badge'>Δs = {current_data['Formula Analitica Non Sviluppata']} m</span>", unsafe_allow_html=True)

st.write("")

# VISUALIZZAZIONE GRAFICA INTERATTIVA (PLOTLY)
fig = go.Figure()

# Grafico 1: Vista Globale della Pista
fig.add_trace(go.Scatter(
    x=[current_data['Posizione Achille s_A (m)']], y=[1],
    mode='markers+text',
    name='Achille 🏃',
    marker=dict(symbol='triangle-right', size=22, color='#1f77b4'),
    text=["Achille"], textposition="top center"
))

fig.add_trace(go.Scatter(
    x=[current_data['Posizione Tartaruga s_T (m)']], y=[1],
    mode='markers+text',
    name='Tartaruga 🐢',
    marker=dict(symbol='circle', size=18, color='#2ca02c'),
    text=["Tartaruga"], textposition="top center"
))

# Segmento del GAP
fig.add_shape(
    type="line",
    x0=current_data['Posizione Achille s_A (m)'], y0=1,
    x1=current_data['Posizione Tartaruga s_T (m)'], y1=1,
    line=dict(color="red", width=4, dash="dot")
)

fig.update_layout(
    title=f"Rappresentazione Spaziale Globale al Passo n = {st.session_state.step}",
    xaxis=dict(title="Posizione sulla Pista (metri)", range=[-5, max(120, d0 * 1.25)]),
    yaxis=dict(visible=False, range=[0.5, 1.5]),
    height=200,
    margin=dict(l=20, r=20, t=40, b=30),
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Vista "Lente d'Ingrandimento" (Zoom sul GAP)
fig_zoom = go.Figure()

gap_val = float(current_data['Gap Δs (m, Decimal)'])
# Se il gap_val è infinitamente piccolo, manteniamo comunque una distanza simbolica visiva normalizzata = 1
display_gap = gap_val if gap_val > 0 else 1e-15
pos_A = current_data['Posizione Achille s_A (m)']
pos_T = current_data['Posizione Tartaruga s_T (m)']

fig_zoom.add_trace(go.Scatter(
    x=[0], y=[1],
    mode='markers+text',
    name='Achille',
    marker=dict(symbol='triangle-right', size=26, color='#1f77b4'),
    text=[f"Achille ({pos_A:.8f} m)"], textposition="bottom center"
))

fig_zoom.add_trace(go.Scatter(
    x=[display_gap], y=[1],
    mode='markers+text',
    name='Tartaruga',
    marker=dict(symbol='circle', size=22, color='#2ca02c'),
    text=[f"Tartaruga ({pos_T:.8f} m)"], textposition="bottom center"
))

fig_zoom.add_shape(
    type="line",
    x0=0, y0=1,
    x1=display_gap, y1=1,
    line=dict(color="crimson", width=6)
)

fig_zoom.update_layout(
    title=f"🔍 Lente d'Ingrandimento sul GAP Spaziale Residuo (Δs = {current_data['Formula Analitica Non Sviluppata']} m)",
    xaxis=dict(title="Distanza Relativa da Achille (metri)", range=[-display_gap*0.2, display_gap*1.2]),
    yaxis=dict(visible=False, range=[0.5, 1.5]),
    height=220,
    margin=dict(l=20, r=20, t=40, b=30),
    template="plotly_white"
)

st.plotly_chart(fig_zoom, use_container_width=True)

# TABELLA DELLE POSIZIONI E DEL GAP (NOTAZIONE ESPONENZIALE E FORMULA NON SVILUPPATA)
st.subheader("📊 Tabella Comparativa dei Passi (Logica di Zenone)")

# Evidenzia la riga corrente
def highlight_current(row):
    if row['Passo (n)'] == st.session_state.step:
        return ['background-color: #d1ecf1; font-weight: bold'] * len(row)
    return [''] * len(row)

display_df = df[['Passo (n)', 'Tempo Totale (s)', 'Posizione Achille s_A (m)', 'Posizione Tartaruga s_T (m)', 'Formula Analitica Non Sviluppata', 'GAP Esponenziale']].copy()
display_df.columns = ['Passo (n)', 'Tempo Acquisito (s)', 'Posizione Achille (m)', 'Posizione Tartaruga (m)', 'Formula del GAP (Non Sviluppata)', 'GAP Residuo Δs (Notazione Esponenziale)']

st.dataframe(display_df.style.apply(highlight_current, axis=1), use_container_width=True)

# BOX MAIEUTICO - LA DOMANDA EPISTEMICA DI ATHENA
st.markdown(f"""
<div class="maieutic-box">
    <h3>🤔 Riflessione Maieutica (Il Nodo Concettuale)</h3>
    <p><b>Osserva la colonna "Formula del GAP (Non Sviluppata)":</b> al passo $n$, la distanza è data da $100 \cdot \left(\frac{{1}}{{10}}\right)^n$.</p>
    <p>Poiché la base $\frac{{1}}{{10}} > 0$, una potenziale elevata a qualsiasi numero intero $n$ <b>è rigorosamente e matematicamente maggiore di zero</b> ($\Delta s > 0$). Non sarà mai esattamente $0$, qualunque sia il valore di $n$.</p>
    <hr style="border-top: 1px solid #ffe8a1;">
    <h4 style="color: #856404; text-align: center;">🎯 Domanda Chiave per la Classe:</h4>
    <p style="font-size: 1.25rem; font-weight: bold; text-align: center; color: #533f03;">
        "Se in questa successione il distacco non diventa mai zero per nessun passo $n$, come fa Achille nella realtà a superare la tartaruga? Come può una somma infinita di intervalli temporali e spaziali produrre un risultato finito?"
    </p>
</div>
""", unsafe_allow_html=True)

# SCARICAMENTO DATI
csv_data = display_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Scarica la Tabella dei Dati (CSV)",
    data=csv_data,
    file_name="simulazione_paradosso_zenone_rigoroso.csv",
    mime="text/csv"
)
