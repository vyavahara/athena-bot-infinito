# ------------------------------------------------------------------------------
# 8. TABELLA ANALITICA CON FRAZIONI ESATTE
# ------------------------------------------------------------------------------
st.markdown("##### 📊 Tabella Analitica delle Frazioni Esatte")

display_rows = []
for idx, row in df.iterrows():
    display_rows.append({
        "Passo (n)": row["n"],
        "Spostamento Achille (dₙ)": f"{format_frac(row['d'])} m",
        "Posizione Achille (Aₙ)": f"{format_frac(row['A'])} m",
        "Spostamento Tartaruga (tₙ)": f"{format_frac(row['t'])} m",
        "Posizione Tartaruga (Tₙ)": f"{format_frac(row['T'])} m",
        "Distacco Residuo (Δsₙ)": f"{format_frac(row['delta_s'])} m",
    })

df_display = pd.DataFrame(display_rows)

def highlight_row(row):
    if row["Passo (n)"] == curr_step:
        return ["background-color: #dbeafe; font-weight: bold; color: #1e40af"] * len(row)
    return [""] * len(row)

st.dataframe(df_display.style.apply(highlight_row, axis=1), use_container_width=True)
