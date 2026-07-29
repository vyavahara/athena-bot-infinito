from fractions import Fraction
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ==============================================================================
# CONFIGURAZIONE PAGINA
# ==============================================================================

st.set_page_config(
    page_title="Paradosso di Achille e la tartaruga - Zenone",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==============================================================================
# CSS PERSONALIZZATO
# ==============================================================================

st.markdown(
    """
<style>

.main {
    background-color: #f8fafc;
}

.stApp {
    font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 1.2rem !important;
}


p {
    margin-bottom: 0.45rem !important;
    line-height: 1.5;
    font-size: 1.05rem !important;
}


/* ---------------- HERO ---------------- */

.hero-banner {

    background:
    linear-gradient(
        135deg,
        #0f172a 0%,
        #1e3c72 50%,
        #2a5298 100%
    );

    color:white;

    padding:20px 24px;

    border-radius:12px;

    text-align:center;

    margin-bottom:14px;

    box-shadow:
    0 4px 12px rgba(15,23,42,.15);

}


.hero-banner h1 {

    color:white !important;

    font-weight:800 !important;

    font-size:1.85rem !important;

    margin:0 !important;

}


/* ---------------- CARD ---------------- */


.math-model-card,
.init-conditions-card,
.athena-socratic-card {


    background:white;

    border:1px solid #cbd5e1;

    border-radius:8px;

    padding:16px 18px;

    margin-bottom:14px;

    box-shadow:
    0 3px 8px rgba(0,0,0,.04);

}


/* bordo laterale */

.math-model-card,
.init-conditions-card {

    border-left:
    6px solid #0284c7;

}


.athena-socratic-card {

    border-left:
    6px solid #1e3c72;

}


.math-model-card h4,
.init-conditions-card h4 {

    color:#0f172a;

    font-weight:800;

    margin-top:0;

}


/* ---------------- TITOLI ---------------- */


.section-title {

    color:#0f172a;

    font-size:1.25rem !important;

    font-weight:800;

    margin-top:16px;

}


.section-subtitle {

    color:#475569;

    font-weight:600;

}


/* ---------------- FRAZIONI ---------------- */


.fraction-badge {


    background:#e2e8f0;

    border:
    1px solid #94a3b8;

    padding:
    3px 8px;

    border-radius:5px;

    font-family:
    monospace;

    font-weight:bold;

}



/* ---------------- CONFLITTO COGNITIVO ---------------- */


.cognitive-conflict-box {


    background:#fffbeb;

    border:
    1px solid #fde68a;


    border-left:
    6px solid #f59e0b;


    padding:
    12px 16px;


    border-radius:8px;


    margin-top:14px;

}



.cognitive-conflict-box h4 {


    color:#b45309;

    font-weight:800;

}


.conflict-text {


    color:#78350f;

    font-weight:600;

}


/* metriche */

[data-testid="stMetricValue"] {

    font-size:1.4rem !important;

    font-weight:800 !important;

}


[data-testid="stMetricLabel"] {

    font-size:1rem !important;

    font-weight:600 !important;

}


</style>
""",
    unsafe_allow_html=True,
)



# ==============================================================================
# FUNZIONI HELPER
# ==============================================================================


def to_subscript(value: int | str) -> str:
    """
    Converte numeri nei pedici Unicode.
    Esempio:
    3 -> ₃
    """

    mapping = str.maketrans(
        "0123456789n",
        "₀₁₂₃₄₅₆₇₈₉ₙ"
    )

    return str(value).translate(mapping)



def format_fraction(value: Fraction) -> str:
    """
    Visualizzazione leggibile delle frazioni.
    Mantiene internamente Fraction.
    """

    if value.denominator == 1:
        return str(value.numerator)

    return f"{value.numerator}/{value.denominator}"



def fraction_to_float(value: Fraction) -> float:
    """
    Conversione consentita esclusivamente
    per Plotly.
    """

    return float(value)



# ==============================================================================
# MODELLO MATEMATICO DI ZENONE
# COSTRUZIONE GEOMETRICA ITERATIVA
# ==============================================================================


def genera_costruzione_zenone(
        distacco_iniziale: int,
        k: int,
        numero_passi: int
):
    """
    Genera la successione geometrica del paradosso.

    NON rappresenta un moto.
    NON introduce il tempo.
    NON introduce velocità.

    Costruisce solamente:

    A₀ = 0

    T₀ = Δs₀

    Δsₙ = Tₙ - Aₙ

    dₙ = Δsₙ₋₁

    tₙ = Δsₙ₋₁/k

    Aₙ = Aₙ₋₁ + dₙ

    Tₙ = Tₙ₋₁ + tₙ

    """

    dati = []


    delta0 = Fraction(distacco_iniziale,1)


    A = Fraction(0,1)

    T = delta0



    for n in range(numero_passi + 1):


        if n == 0:

            d = Fraction(0,1)

            t = Fraction(0,1)

            delta = delta0



        else:


            delta_precedente = dati[-1]["delta"]


            # Achille raggiunge geometricamente
            # il precedente punto della tartaruga

            d = delta_precedente



            # La tartaruga acquisisce un nuovo segmento

            t = delta_precedente / Fraction(k,1)



            A = A + d

            T = T + t



            delta = T - A



        dati.append(

            {

            "n":n,

            "A":A,

            "T":T,

            "d":d,

            "t":t,

            "delta":delta,

            }

        )


    return pd.DataFrame(dati)



# ==============================================================================
# FINE PARTE 1/3
# ==============================================================================
# ==============================================================================
# INTESTAZIONE
# ==============================================================================


st.markdown(
    """
<div class="hero-banner">

<h1>
📐 🏃 🐢
Simulazione geometrica del Paradosso di Achille e la tartaruga
</h1>

</div>
""",
    unsafe_allow_html=True,
)



# ==============================================================================
# MODELLO MATEMATICO PRESENTATO ALL'UTENTE
# ==============================================================================


st.markdown(
    """

<div class="math-model-card">

<h4>📐 Modello matematico della costruzione di Zenone</h4>


<p>

La traiettoria è rappresentata come una retta orientata.
Ogni punto è identificato dalla propria coordinata reale.

Le successioni
<b>(Aₙ)</b> e <b>(Tₙ)</b>
rappresentano le posizioni geometriche associate ai passi successivi della costruzione.

</p>


<p>

La simulazione non introduce il tempo né il concetto fisico di velocità:
mostra esclusivamente la costruzione iterativa dei segmenti descritta da Zenone.

</p>


<p>

<b>
Aₙ = posizione geometrica di Achille
</b>

<br>

<b>
Tₙ = posizione geometrica della tartaruga
</b>

</p>


</div>

""",
    unsafe_allow_html=True,
)




# ==============================================================================
# SIDEBAR
# ==============================================================================


st.sidebar.header(
    "⚙️ Parametri della costruzione geometrica"
)



delta_s0_val = st.sidebar.number_input(

    "Distacco iniziale Δs₀ = m(A₀T₀) [metri]",

    min_value=1,

    value=100,

    step=10,

)



k_val = st.sidebar.number_input(

    "Rapporto geometrico k con dₙ = k · tₙ",

    min_value=2,

    max_value=100,

    value=10,

    step=1,

)



max_steps = st.sidebar.slider(

    "Numero di passi logici n",

    min_value=1,

    max_value=15,

    value=10,

)



# ==============================================================================
# GESTIONE STATO STREAMLIT
# ==============================================================================


if "step" not in st.session_state:

    st.session_state.step = 0



# evita che lo step rimanga fuori range
if st.session_state.step > max_steps:

    st.session_state.step = max_steps



col1, col2, col3, _ = st.columns(
    [1.2,1.2,1.2,2.4]
)



with col1:

    if st.button(
        "⏮️ Stato iniziale n=0"
    ):

        st.session_state.step = 0



with col2:

    if st.button(
        "◀️ Passo precedente"
    ):

        if st.session_state.step > 0:

            st.session_state.step -= 1



with col3:

    if st.button(
        "▶️ Passo successivo"
    ):

        if st.session_state.step < max_steps:

            st.session_state.step += 1



st.sidebar.markdown("---")

st.sidebar.write(
    f"**Passo selezionato:** n = {st.session_state.step}"
)



# ==============================================================================
# GENERAZIONE MODELLO
# ==============================================================================


df = genera_costruzione_zenone(

    distacco_iniziale=delta_s0_val,

    k=k_val,

    numero_passi=max_steps

)



curr_step = st.session_state.step


current = df.iloc[curr_step]




# ==============================================================================
# CONDIZIONI INIZIALI
# ==============================================================================


st.markdown(

f"""

<div class="init-conditions-card">

<h4>
📋 Configurazione iniziale
</h4>


<p>

🏃
<b>A₀ = 0 m</b>

&nbsp;&nbsp;&nbsp;


🐢
<b>T₀ = Δs₀ = {delta_s0_val} m</b>


</p>


<p>

La relazione tra i segmenti costruiti è:

<b>
dₙ = {k_val} · tₙ
</b>

</p>


</div>

""",

unsafe_allow_html=True

)



# ==============================================================================
# METRICHE PRINCIPALI
# ==============================================================================


m1,m2,m3,m4 = st.columns(4)



with m1:

    st.metric(

        "Passo logico n",

        str(curr_step)

    )


with m2:

    st.metric(

        f"A{to_subscript(curr_step)}",

        format_fraction(current["A"])+" m"

    )


with m3:

    st.metric(

        f"T{to_subscript(curr_step)}",

        format_fraction(current["T"])+" m"

    )


with m4:

    st.metric(

        f"Δs{to_subscript(curr_step)}",

        format_fraction(current["delta"])+" m"

    )




# ==============================================================================
# VISUALIZZAZIONE PRINCIPALE
# ==============================================================================


left,right = st.columns(
    [1.15,1]
)



with left:


    st.markdown(

        f"""
<div class="section-title">

🏃 🐢 Rappresentazione spaziale della costruzione (n={curr_step})

</div>
""",

        unsafe_allow_html=True

    )



    fig = go.Figure()



    A_float = fraction_to_float(current["A"])

    T_float = fraction_to_float(current["T"])



    max_x = max(

        float(delta_s0_val)*1.45,

        T_float*1.25 + 30

    )



    # pista Achille

    fig.add_shape(

        type="line",

        x0=0,

        x1=max_x,

        y0=0,

        y1=0,

        line=dict(

            width=6,

            color="#93c5fd"

        )

    )



    # pista tartaruga

    fig.add_shape(

        type="line",

        x0=0,

        x1=max_x,

        y0=1,

        y1=1,

        line=dict(

            width=6,

            color="#86efac"

        )

    )



    # punti precedenti A_k

    for k in range(curr_step+1):


        x = fraction_to_float(
            df.iloc[k]["A"]
        )


        fig.add_trace(

            go.Scatter(

                x=[x],

                y=[0],

                mode="markers",

                marker=dict(

                    size=9,

                    color="#334155"

                ),

                hoverinfo="skip",

                showlegend=False

            )

        )



    # segmento appena costruito

    if curr_step>0:


        precedente = fraction_to_float(

            df.iloc[curr_step-1]["A"]

        )


        fig.add_shape(

            type="line",

            x0=precedente,

            x1=A_float,

            y0=0,

            y1=0,

            line=dict(

                width=8,

                color="#1d4ed8"

            )

        )




    # distacco residuo


    fig.add_shape(

        type="line",

        x0=A_float,

        x1=T_float,

        y0=.5,

        y1=.5,

        line=dict(

            width=4,

            dash="dash",

            color="#b91c1c"

        )

    )



    # Achille


    fig.add_trace(

        go.Scatter(

            x=[A_float],

            y=[0],

            mode="markers+text",

            marker=dict(

                size=18,

                color="#1e3c72"

            ),

            text=[

                f"🏃 A{to_subscript(curr_step)}"

            ],

            textposition="top center",

            cliponaxis=False,

            showlegend=False

        )

    )



    # tartaruga


    fig.add_trace(

        go.Scatter(

            x=[T_float],

            y=[1],

            mode="markers+text",

            marker=dict(

                size=18,

                color="#15803d"

            ),

            text=[

                f"🐢 T{to_subscript(curr_step)}"

            ],

            textposition="top center",

            cliponaxis=False,

            showlegend=False

        )

    )



    fig.update_layout(

        height=320,

        margin=dict(

            l=20,

            r=80,

            t=20,

            b=20

        ),

        xaxis=dict(

            title="Coordinata sulla retta orientata (m)",

            range=[-5,max_x]

        ),

        yaxis=dict(

            tickvals=[0,1],

            ticktext=[

                "Achille",

                "Tartaruga"

            ],

            range=[-.5,1.5]

        ),

        template="plotly_white"

    )



    st.plotly_chart(

        fig,

        use_container_width=True

    )
# ==============================================================================
# ATHENA - GUIDA SOCRATICA
# ==============================================================================


with right:


    step_sub = to_subscript(curr_step)


    if curr_step == 0:


        st.markdown(

f"""

<div class="athena-socratic-card">

<h3>
🏛️ Athena: osservazione iniziale
</h3>


<p>

<b>1. Configurazione geometrica</b>

<br>

Achille è collocato nel punto:

<b>A₀ = 0</b>

mentre la tartaruga è nel punto:

<b>T₀ = {delta_s0_val} m</b>.

</p>


<p>

<b>2. Primo segmento della costruzione</b>

<br>

Il distacco iniziale è:

<span class="fraction-badge">

Δs₀ = m(A₀T₀) = {delta_s0_val} m

</span>

</p>


<p>

<b>3. Ragionamento di Zenone</b>

<br>

Per raggiungere la posizione T₀,
Achille deve costruire il segmento:

<span class="fraction-badge">

d₁ = Δs₀

</span>

</p>


<div class="cognitive-conflict-box">


<h4>

🧠 Domanda

</h4>


<div class="conflict-text">


Se ogni raggiungimento di un punto genera
un nuovo segmento da costruire,
la procedura può concludersi dopo un numero finito di passi?


</div>


</div>


</div>

""",

unsafe_allow_html=True

)



    else:


        d = format_fraction(current["d"])

        t = format_fraction(current["t"])

        delta = format_fraction(current["delta"])



        somma = " + ".join(

            [

            format_fraction(df.iloc[i]["d"])

            for i in range(1,curr_step+1)

            ]

        )



        st.markdown(

f"""

<div class="athena-socratic-card">


<h3>

🏛️ Athena: passo n = {curr_step}

</h3>



<p>

<b>1. Costruzione del segmento di Achille</b>

<br>


Achille raggiunge geometricamente il punto precedente della tartaruga:

<br>

<b>

A{step_sub}=T{to_subscript(curr_step-1)}

</b>


<br>


perché:

<br>


<span class="fraction-badge">

d{step_sub}=Δs{to_subscript(curr_step-1)}={d} m

</span>


</p>



<p>

<b>2. Nuovo segmento della tartaruga</b>

<br>


La costruzione aggiunge un nuovo tratto:


<span class="fraction-badge">

t{step_sub}=Δs{to_subscript(curr_step-1)}/{k_val}
={t} m

</span>


</p>



<p>

<b>3. Coordinata raggiunta da Achille</b>


<div style="

background:#f8fafc;

border:1px solid #cbd5e1;

padding:10px;

border-radius:6px;

font-family:monospace;

">


s_A({step_sub})

=

d₁+d₂+...+d{step_sub}

<br>

=

{somma}

<br>

=

{format_fraction(current["A"])} m


</div>


</p>



<p>

<b>4. Nuovo distacco residuo</b>

<br>


Il segmento ancora presente è:

<span class="fraction-badge">

Δs{step_sub}={delta} m

</span>


</p>



<div class="cognitive-conflict-box">


<h4>

🧠 Conflitto cognitivo

</h4>


<div class="conflict-text">


Se Δs{step_sub} è ancora positivo,
Zenone richiede un nuovo segmento:

<br>


d{to_subscript(curr_step+1)}

=

Δs{step_sub}


<br>


Come può una successione di segmenti positivi
portare al raggiungimento?


</div>


</div>



</div>


""",

unsafe_allow_html=True

)




# ==============================================================================
# SOMMA DEGLI SPOSTAMENTI DI ACHILLE
# ==============================================================================


st.markdown(

f"""

<div class="section-title">

📏 Decomposizione della posizione di Achille

</div>

<div class="section-subtitle">

s_A(n)=d₁+d₂+...+dₙ

fino al passo n={curr_step}

</div>

""",

unsafe_allow_html=True

)



fig_bar = go.Figure()



for i in range(1,curr_step+1):


    valore = fraction_to_float(

        df.iloc[i]["d"]

    )


    fig_bar.add_trace(

        go.Bar(

            x=[valore],

            y=["Segmenti costruiti"],

            orientation="h",

            name=(

                f"d{to_subscript(i)} = "

                f"{format_fraction(df.iloc[i]['d'])} m"

            )

        )

    )



fig_bar.update_layout(

    barmode="stack",

    height=170,

    template="plotly_white",

    margin=dict(

        l=20,

        r=40,

        t=20,

        b=20

    ),

    xaxis_title="Coordinata sulla retta (m)",

    yaxis_visible=False

)



st.plotly_chart(

    fig_bar,

    use_container_width=True

)




# ==============================================================================
# TABELLA ANALITICA
# ==============================================================================


st.markdown(

"""

<div class="section-title">

📊 Tabella analitica della costruzione

</div>

""",

unsafe_allow_html=True

)



tabella=[]



for _,row in df.iterrows():


    tabella.append(

        {

        "Passo n":

            row["n"],


        "Aₙ":

            format_fraction(row["A"])+" m",


        "dₙ":

            format_fraction(row["d"])+" m",


        "Tₙ":

            format_fraction(row["T"])+" m",


        "tₙ":

            format_fraction(row["t"])+" m",


        "Δsₙ":

            format_fraction(row["delta"])+" m"

        }

    )



df_tabella=pd.DataFrame(tabella)



def evidenzia(row):


    if row["Passo n"]==curr_step:

        return [

            "background-color:#dbeafe;font-weight:bold"

        ]*len(row)


    return [""]*len(row)



st.dataframe(

    df_tabella.style.apply(

        evidenzia,

        axis=1

    ),

    use_container_width=True

)



# ==============================================================================
# CHIUSURA EPISTEMOLOGICA
# ==============================================================================


st.markdown(

"""

<div class="cognitive-conflict-box">


<h4>

⚡ Il problema posto da Zenone

</h4>


<div class="conflict-text">


La costruzione mostra che:


<br><br>


• ogni passo finito lascia un distacco positivo;

<br>

• Achille raggiunge sempre il punto precedente della tartaruga;

<br>

• la tartaruga conserva sempre un nuovo segmento residuo.


<br><br>


La domanda filosofica e matematica diventa:


<br>


<b>

Come può una successione infinita di costruzioni
con segmenti positivi produrre il raggiungimento?

</b>


<br><br>


La simulazione rappresenta il paradosso.
La sua eventuale soluzione richiederà strumenti matematici successivi.

</div>


</div>

""",

unsafe_allow_html=True

)
