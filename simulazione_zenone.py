import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ==========================================================
# CONFIGURAZIONE
# ==========================================================

st.set_page_config(
    page_title="Athena - Paradosso di Elea",
    page_icon="🏛️",
    layout="wide"
)

# ==========================================================
# STILE
# ==========================================================

st.markdown("""
<style>

.header-container {
    background: linear-gradient(135deg,#1e293b,#0f172a);
    padding:2rem;
    border-radius:12px;
    text-align:center;
    color:white;
}

.header-title {
    font-size:2.2rem;
    font-weight:700;
}

.header-subtitle {
    color:#cbd5e1;
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="header-container">

<div class="header-title">
🏛️ Athena: Achille e la Tartaruga
</div>

<div class="header-subtitle">
Esploriamo il paradosso di Zenone attraverso la costruzione infinita degli intervalli
</div>

</div>
""", unsafe_allow_html=True)


# ==========================================================
# STATO
# ==========================================================

if "step" not in st.session_state:
    st.session_state.step = 0


# ==========================================================
# MODELLO MATEMATICO
# ==========================================================

vantaggio_iniziale = 100
rapporto = 0.1

passi = []

achille = 0
tartaruga = vantaggio_iniziale


for n in range(12):

    distanza = tartaruga - achille

    passi.append({

        "n": n,
        "Achille": achille,
        "Tartaruga": tartaruga,
        "Distacco": distanza

    })

    # Achille raggiunge il punto precedente della tartaruga
    achille = tartaruga

    # la tartaruga percorre 1/10 del vantaggio perso
    tartaruga = tartaruga + distanza*rapporto



# ==========================================================
# CONTROLLI
# ==========================================================


c1,c2,c3 = st.columns([1,1,3])


with c1:
    if st.button("⬅️ Passo precedente"):
        if st.session_state.step > 0:
            st.session_state.step -= 1


with c2:
    if st.button("Passo successivo ➡️"):

        if st.session_state.step < len(passi)-1:
            st.session_state.step +=1



n = st.session_state.step


# ==========================================================
# PANNELLO ATHENA
# ==========================================================


dati = passi[n]


col1,col2,col3 = st.columns(3)


col1.metric(
    "Passo",
    n
)

col2.metric(
    "Posizione Achille",
    f"{dati['Achille']:.6f} m"
)

col3.metric(
    "Distanza residua",
    f"{dati['Distacco']:.6f} m"
)


domande = [

"Achille ha percorso 100 m. Perché non ha ancora raggiunto la tartaruga?",

"La distanza si riduce. Significa che prima o poi sparirà?",

"Ogni intervallo sembra più piccolo. Quanti intervalli dobbiamo considerare?",

"Se gli intervalli sono infiniti, la distanza totale può essere finita?"

]


st.info(
"🤖 Athena domanda:\n\n" +
domande[min(n,3)]
)



# ==========================================================
# GRAFICO
# ==========================================================


fig = go.Figure()


# pista Achille

fig.add_trace(go.Scatter(

    x=[0,130],
    y=[1,1],
    mode="lines",
    line=dict(width=4),
    showlegend=False

))


# pista tartaruga

fig.add_trace(go.Scatter(

    x=[0,130],
    y=[-1,-1],
    mode="lines",
    line=dict(width=4),
    showlegend=False

))


# punti storici Achille

for i in range(n+1):

    fig.add_trace(go.Scatter(

        x=[passi[i]["Achille"]],
        y=[1],
        mode="markers+text",
        text=[f"A{i}"],
        textposition="top center",
        marker=dict(size=9),
        showlegend=False

    ))


# punti storici tartaruga

for i in range(n+1):

    fig.add_trace(go.Scatter(

        x=[passi[i]["Tartaruga"]],
        y=[-1],
        mode="markers+text",
        text=[f"T{i}"],
        textposition="bottom center",
        marker=dict(size=9),
        showlegend=False

    ))



# tratto percorso Achille

if n>0:

    fig.add_trace(go.Scatter(

        x=[
            passi[n-1]["Achille"],
            passi[n]["Achille"]
        ],

        y=[1,1],

        mode="lines",

        line=dict(width=8),

        showlegend=False

    ))



# tratto tartaruga

if n>0:

    fig.add_trace(go.Scatter(

        x=[
            passi[n-1]["Tartaruga"],
            passi[n]["Tartaruga"]
        ],

        y=[-1,-1],

        mode="lines",

        line=dict(width=8),

        showlegend=False

    ))



# posizione attuale

fig.add_annotation(

    x=dati["Achille"],
    y=1.3,
    text="🏃 Achille",
    showarrow=False

)


fig.add_annotation(

    x=dati["Tartaruga"],
    y=-1.3,
    text="🐢 Tartaruga",
    showarrow=False

)


fig.update_layout(

    height=420,

    xaxis=dict(
        range=[-5,130],
        title="metri"
    ),

    yaxis=dict(
        range=[-2,2],
        visible=False
    ),

    showlegend=False

)


st.plotly_chart(
    fig,
    use_container_width=True
)



# ==========================================================
# TABELLA
# ==========================================================


st.subheader("Costruzione degli intervalli")


df=pd.DataFrame(passi[:n+1])

df["Distacco"]=df["Distacco"].round(6)

st.dataframe(
    df,
    hide_index=True,
    use_container_width=True
)
