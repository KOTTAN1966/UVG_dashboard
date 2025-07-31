
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="UVG-Dashboard – Prozesse, Personal & Überlastung", layout="wide")
st.title("📋 Prozess- & Personalbewertung – Unterhaltsvorschuss")

# Modul 1 – TOP 10 Prozesse
st.header("1️⃣ Modul 1: TOP 10 Prozesse")
prozesse = []
for i in range(1, 11):
    col1, col2 = st.columns([2, 1])
    with col1:
        name = st.text_input(f"{i}. Prozessbezeichnung", key=f"prozess_{i}")
    with col2:
        fallzahl = st.number_input(f"Fallzahl/Jahr", min_value=0, step=1, key=f"fall_{i}")
    if name:
        schnittstelle_intern = st.text_input("Interne Schnittstellen", key=f"int_{i}")
        schnittstelle_extern = st.text_input("Externe Schnittstellen", key=f"ext_{i}")
        digital = st.slider("Digitalisierungsgrad (%)", 0, 100, 50, key=f"dig_{i}")
        medienbruch = st.radio("Medienbrüche vorhanden?", ["nein", "teilweise", "ja"], key=f"med_{i}")
        klarheit = st.slider("Klarheit der Prozessbeschreibung (1=unklar, 5=sehr klar)", 1, 5, 3, key=f"klar_{i}")
        prozesse.append({
            "Prozess": name,
            "Fallzahl": fallzahl,
            "Digital": digital,
            "Medienbruch": medienbruch,
            "Klarheit": klarheit
        })

# Modul 2 – Personalausstattung & Aufgabenverteilung
st.header("2️⃣ Modul 2: Personalausstattung")

vzae = st.number_input("Vollzeitäquivalente (VZÄ)", min_value=0.0, value=0.0, step=0.1)
anz_mitarb = st.number_input("Anzahl Mitarbeitende", min_value=0, value=0)
abwesenheit = st.slider("Abwesenheitsquote (%)", 0, 100, 10)

st.subheader("Zeitverteilung auf Aufgabenblöcke")
aufgaben = ["UVG-Anträge bearbeiten", "Unterhaltsprüfung", "Rückforderungen", "Sonstiges"]
verteilung = {}
for aufgabe in aufgaben:
    anteil = st.slider(f"{aufgabe}", 0, 100, 0, key=f"aufg_{aufgabe}")
    verteilung[aufgabe] = anteil

# Modul 3 – Überlastungsindikatoren
st.header("3️⃣ Modul 3: Überlastungsindikatoren")

rueckstau = st.selectbox("Rückstaus vorhanden?", ["Nein", "gelegentlich", "häufig"])
ueberstunden = st.selectbox("Regelmäßige Überstunden?", ["Nein", "gelegentlich", "häufig"])
auslastung = st.slider("Durchschnittliche Auslastung (1 = niedrig, 5 = hoch)", 1, 5, 3)
fehlzeiten = st.selectbox("Überdurchschnittliche Fehlzeiten?", ["Nein", "tendenziell", "ja"])
qual_indikator = st.radio("Hinweise auf qualitative Überlastung (Fehler, Beschwerden)?", ["Nein", "Ja"])

# Bewertung Überlastung
score = 0
if rueckstau == "gelegentlich": score += 0.5
elif rueckstau == "häufig": score += 1
if ueberstunden == "gelegentlich": score += 0.5
elif ueberstunden == "häufig": score += 1
if auslastung >= 4: score += 1
if fehlzeiten == "tendenziell": score += 0.5
elif fehlzeiten == "ja": score += 1
if qual_indikator == "Ja": score += 1

ampel = "🟢" if score <= 1 else ("🟡" if score <= 3 else "🔴")

st.markdown("---")
st.header("📊 Dashboard")

st.subheader("Überlastungsanzeige")
st.write(f"Überlastungsindikator-Score: {score} → {ampel}")

fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = score,
    title = {'text': "Überlastungsindikatoren (0–5)"},
    gauge = {
        'axis': {'range': [0, 5]},
        'bar': {'color': "darkred"},
        'steps': [
            {'range': [0, 1], 'color': "lightgreen"},
            {'range': [1, 3], 'color': "gold"},
            {'range': [3, 5], 'color': "red"}
        ]
    }
))
st.plotly_chart(fig)

st.markdown("💾 Weitere Module in Planung: Export, Vergleich, Simulation.")



# 📌 Automatisch generierte Optimierungsvorschläge
st.markdown("---")
st.header("💡 Optimierungsvorschläge (automatisch generiert)")

vorschlaege = []

# 1. Medienbrüche
medienbrueche = [p["Medienbruch"] for p in prozesse if "Medienbruch" in p]
if medienbrueche.count("ja") >= 2:
    vorschlaege.append({
        "Problem": "Mehrere Prozesse enthalten manuelle Zwischenschritte (Medienbrüche).",
        "Ziel": "Digitalisierungsgrad erhöhen und medienbruchfreie Abläufe schaffen.",
        "Massnahmen": [
            "Digitale Formulare einführen.",
            "Digitale Unterschrift oder Online-Antrag etablieren.",
            "Integration mit Fachanwendungen prüfen."
        ]
    })

# 2. Unklare Prozesse
unklare = [p["Klarheit"] for p in prozesse if "Klarheit" in p and p["Klarheit"] <= 3]
if len(unklare) >= 2:
    vorschlaege.append({
        "Problem": "Einige Prozesse sind unklar beschrieben oder schwer nachvollziehbar.",
        "Ziel": "Verbesserung der Prozessklarheit für alle Mitarbeitenden.",
        "Massnahmen": [
            "Einfache Ablaufdiagramme erstellen.",
            "Workshops mit Praxisbeteiligung durchführen."
        ]
    })

# 3. Hohe Fallbelastung
prozesse_mit_last = [p for p in prozesse if vzae > 0 and p["Fallzahl"] / vzae > 400]
if len(prozesse_mit_last) >= 1:
    vorschlaege.append({
        "Problem": "Mindestens ein Prozess hat eine sehr hohe Fallzahl je VZÄ.",
        "Ziel": "Reduktion der Arbeitslast und Verbesserung der Bearbeitungsqualität.",
        "Massnahmen": [
            "Kurzfristige Aufgabenpriorisierung.",
            "Mittel-/langfristige Personalbedarfsprüfung."
        ]
    })

# 4. Überlastung gesamt
if score > 3:
    vorschlaege.append({
        "Problem": "Gesamtbewertung zeigt Anzeichen struktureller Überlastung.",
        "Ziel": "Ursachen analysieren und nachhaltige Entlastung einleiten.",
        "Massnahmen": [
            "Kurzfristige Sofortmaßnahmen zur Entlastung.",
            "Klärung der Ursachen in einem internen Workshop.",
            "Führungskräfte-Coaching zum Umgang mit Belastung."
        ]
    })

# 5. Geringe Digitalisierung bei hohem Fallvolumen
low_digital = [p for p in prozesse if p["Digital"] < 50 and p["Fallzahl"] > 300]
if len(low_digital) >= 1:
    vorschlaege.append({
        "Problem": "Ein Prozess mit hoher Fallzahl ist nur gering digitalisiert.",
        "Ziel": "Erhöhung der Automatisierung bei Standardabläufen.",
        "Massnahmen": [
            "Automatisierung prüfen (OCR, Dokumentenlenkung).",
            "Schnittstellen zur elektronischen Akte nutzen."
        ]
    })

# Ausgabe
if vorschlaege:
    for i, v in enumerate(vorschlaege, 1):
        st.subheader(f"{i}. {v['Problem']}")
        st.markdown(f"**Ziel:** {v['Ziel']}")
        st.markdown("**Maßnahmen:**")
        for m in v["Massnahmen"]:
            st.markdown(f"- {m}")
else:
    st.info("Keine auffälligen Optimierungspotenziale erkannt (nach aktuellem Stand).")
