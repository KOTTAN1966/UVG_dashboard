import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="UVG-Prozess- & Personal-Dashboard", layout="centered")

st.title("💼 Prozess- und Personalanalyse – Unterhaltsvorschuss")

# Abschnitt 1 – Prozessorganisation (TOP 10)
st.header("1️⃣ TOP 10 Prozesse mit hohem Aufwand")
top_prozesse = []
for i in range(1, 11):
    p = st.text_input(f"{i}. Prozessbezeichnung", key=f"prozess_{i}")
    if p:
        top_prozesse.append(p)

prozessdaten = []
for p in top_prozesse:
    st.subheader(f"Details zu: {p}")
    schnittstellen_intern = st.text_input(f"Interne Schnittstellen bei {p}", key=f"int_{p}")
    schnittstellen_extern = st.text_input(f"Externe Schnittstellen bei {p}", key=f"ext_{p}")
    digital = st.text_input(f"Digitale Unterstützung bei {p}", key=f"dig_{p}")
    medienbruch = st.radio(f"Medienbrüche vorhanden bei {p}?", ["ja", "nein", "teilweise"], key=f"med_{p}")
    prozessklar = st.slider(f"Klarheit der Prozessbeschreibung bei {p} (1 = unklar, 5 = klar)", 1, 5, 3, key=f"klar_{p}")
    prozessdaten.append({"Prozess": p, "Medienbruch": medienbruch, "Prozessklarheit": prozessklar})

# Abschnitt 2 – Fallzahlen
tab_fallzahlen = []
st.header("2️⃣ Fallzahlen je Prozess")
for p in top_prozesse:
    fz = st.number_input(f"Fallzahl pro Jahr für {p}", min_value=0, value=0, key=f"fz_{p}")
    tab_fallzahlen.append({"Prozess": p, "Fallzahl": fz})

# Abschnitt 3 – Personalausstattung
st.header("3️⃣ Personalausstattung")
anzahl_mitarb = st.number_input("Anzahl Mitarbeitende im Bereich", min_value=0, value=0)
vzae = st.number_input("Vollzeitäquivalente (VZÄ)", min_value=0.0, value=0.0, step=0.1)
abwesenheit = st.slider("Geschätzte Abwesenheitsquote (%)", 0, 100, 10)

# Abschnitt 4 – Überlastungsindikatoren
st.header("4️⃣ Überlastungsindikatoren")
ind_1 = st.checkbox("Rückstaus / unbearbeitete Fälle")
ind_2 = st.checkbox("Regelmäßige Überstunden")
ind_3 = st.checkbox("Hohe Krankenstände / Fluktuation")
ind_4 = st.checkbox("Hinweise auf qualitative Überlastung (z. B. Beschwerden, Fehler)")

indikator_summe = sum([ind_1, ind_2, ind_3, ind_4])

st.markdown("---")
st.header("📊 Dashboard – Übersicht")

# Bewertung je Prozess (Ampel anhand Prozessklarheit und Medienbrüchen)
st.subheader("Prozessstatus")
for eintrag in prozessdaten:
    farbe = "🟢" if eintrag["Prozessklarheit"] >= 4 and eintrag["Medienbruch"] == "nein" else ("🟡" if eintrag["Prozessklarheit"] >= 3 else "🔴")
    st.write(f"{eintrag['Prozess']}: {farbe} Klarheit: {eintrag['Prozessklarheit']} – Medienbruch: {eintrag['Medienbruch']}")

# Personalbelastung (Fälle pro VZÄ)
st.subheader("📈 Personalbelastung")
for eintrag in tab_fallzahlen:
    fallzahl = eintrag["Fallzahl"]
    prozess = eintrag["Prozess"]
    if vzae > 0:
        faelle_pro_vzae = fallzahl / vzae
        status = "🟢" if faelle_pro_vzae < 200 else ("🟡" if faelle_pro_vzae < 400 else "🔴")
        st.write(f"{prozess}: {fallzahl} Fälle / {vzae:.1f} VZÄ → {faelle_pro_vzae:.1f} Fälle/VZÄ → {status}")

# Überlastung gesamt – Zeigerinstrument (Gauge)
st.subheader("🔎 Überlastung")
ampel = "🟢" if indikator_summe == 0 else ("🟡" if indikator_summe <= 2 else "🔴")
st.write(f"Anzahl aktiver Überlastungsindikatoren: {indikator_summe} → {ampel}")

# Zeiger mit Plotly anzeigen
fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = indikator_summe,
    title = {'text': "Überlastungsindikatoren (0–4)"},
    gauge = {
        'axis': {'range': [0, 4]},
        'bar': {'color': "darkred"},
        'steps': [
            {'range': [0, 1], 'color': "lightgreen"},
            {'range': [1, 3], 'color': "gold"},
            {'range': [3, 4], 'color': "red"}
        ]
    }
))
st.plotly_chart(fig)

st.markdown("""---
💾 Hinweis: Dieses Tool befindet sich im Aufbau. Weitere Visualisierungen (z. B. zusätzliche Tachos) und Exportfunktionen folgen.
""")