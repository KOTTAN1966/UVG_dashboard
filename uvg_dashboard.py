
import streamlit as st

st.set_page_config(page_title="UVG-Prozess- & Personal-Dashboard", layout="centered")

st.title("💼 Prozess- und Personalanalyse – Unterhaltsvorschuss")

# Modul 1 – Reifegrad
st.header("1️⃣ Reifegradanalyse")
proz_doku = st.selectbox("Wie ist der Prozess dokumentiert?", ["nicht", "grob", "detailliert"])
aufgaben_verteilung = st.slider("Wie eindeutig ist die Aufgabenverteilung?", 1, 5, 3)

# Modul 2 – Personalbewertung
st.header("2️⃣ Personalbewertung")
pers_einsch = st.radio("Wie bewerten Sie die Personalausstattung?", ["deutlich zu gering", "eher zu gering", "passend", "eher zu hoch", "zu hoch"])
ueberlastung = st.radio("Gibt es regelmäßig Überlastung?", ["ja", "nein", "gelegentlich"])
ueberstunden = st.slider("Wie häufig fallen Überstunden an?", 1, 5, 3)
balance = st.slider("Wie ausgewogen ist das Verhältnis Aufgaben/Personal?", 1, 5, 3)

# Modul 3 – Bearbeitungszeiten
st.header("3️⃣ Fallzahlen & Bearbeitungszeit")
fallzahl = st.number_input("Fallzahl pro Jahr", min_value=0, value=800)
bearb_zeit = st.number_input("Ø Bearbeitungszeit pro Fall (Minuten)", min_value=0, value=45)
produktivstunden = st.number_input("Produktivstunden pro VZÄ", min_value=1, value=1400)

gesamtstunden = (fallzahl * bearb_zeit) / 60
bedarf_vzae = gesamtstunden / produktivstunden

st.markdown("---")
st.header("📊 Auswertung")

# Reifegrad-Bewertung
if proz_doku == "detailliert":
    reifegrad = "🟢 Hoch"
elif proz_doku == "grob":
    reifegrad = "🟠 Mittel"
else:
    reifegrad = "🔴 Niedrig"
st.subheader("Reifegrad")
st.write(f"Dokumentation: {proz_doku} → {reifegrad}")

# Personaleinschätzung Ampel
if pers_einsch in ["deutlich zu gering", "eher zu gering"]:
    personal_ampel = "🔴 Unterbesetzung"
elif pers_einsch in ["eher zu hoch", "zu hoch"]:
    personal_ampel = "🟢 Überdeckung"
else:
    personal_ampel = "🟡 Ausgeglichen"

st.subheader("Personalbewertung")
st.write(f"Einschätzung: {pers_einsch} → {personal_ampel}")

# VZÄ-Bedarf
st.subheader("VZÄ-Bedarf")
st.write(f"Benötigte Gesamtstunden: **{gesamtstunden:.1f} Std**")
st.write(f"Erforderliche VZÄ: **{bedarf_vzae:.2f}**")

st.markdown("""---  
💾 Dieses Mockup dient als Prototyp für dein zukünftiges Web-Dashboard. Eine Exportfunktion (PDF, Excel) und Benutzerverwaltung kann ergänzt werden.""")
