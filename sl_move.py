import streamlit as st

st.title("Vergleich Schweiz vs. Spanien")

st.sidebar.header("Eingabeparameter")

# Eingabewerte
brutto = st.sidebar.number_input("Bruttojahreseinkommen", value=60000.0, step=1000.0)
steuersatz_ch = st.sidebar.slider("Steuersatz Schweiz (%)", min_value=0.0, max_value=50.0, value=20.0)
steuersatz_es = st.sidebar.slider("Steuersatz Spanien (%)", min_value=0.0, max_value=50.0, value=30.0)

soz_ch = st.sidebar.slider("Sozialversicherungsbeiträge Schweiz (%)", min_value=0.0, max_value=20.0, value=10.0)
soz_es = st.sidebar.slider("Sozialversicherungsbeiträge Spanien (%)", min_value=0.0, max_value=20.0, value=7.0)

kk_ch = st.sidebar.number_input("Monatl. Krankenkasse Schweiz (CHF/EUR)", value=400.0, step=50.0)
kk_es = st.sidebar.number_input("Monatl. Krankenkasse Spanien (CHF/EUR)", value=100.0, step=10.0)

miete_ch = st.sidebar.number_input("Monatl. Miete Schweiz (CHF/EUR)", value=2000.0, step=100.0)
miete_es = st.sidebar.number_input("Monatl. Miete Spanien (CHF/EUR)", value=1200.0, step=100.0)

leb_ch = st.sidebar.number_input("Jährl. Lebenshaltungskosten Schweiz (CHF/EUR)", value=12000.0, step=1000.0)
leb_es = st.sidebar.number_input("Jährl. Lebenshaltungskosten Spanien (CHF/EUR)", value=10000.0, step=1000.0)

wechselkurs = st.sidebar.number_input("Wechselkurs (CHF zu EUR)", value=1.0, step=0.01)

# Berechnungen für die Schweiz
steuern_ch = brutto * (steuersatz_ch / 100.0)
sozial_ch = brutto * (soz_ch / 100.0)
kk_ch_jahr = kk_ch * 12
miete_ch_jahr = miete_ch * 12

netto_ch = brutto - steuern_ch - sozial_ch - kk_ch_jahr
gesamtkosten_ch = steuern_ch + sozial_ch + kk_ch_jahr + miete_ch_jahr + leb_ch
sparpotenzial_ch = netto_ch - (miete_ch_jahr + leb_ch)

# Berechnungen für Spanien
steuern_es = brutto * (steuersatz_es / 100.0)
sozial_es = brutto * (soz_es / 100.0)
kk_es_jahr = kk_es * 12
miete_es_jahr = miete_es * 12

netto_es = brutto - steuern_es - sozial_es - kk_es_jahr
gesamtkosten_es = steuern_es + sozial_es + kk_es_jahr + miete_es_jahr + leb_es
sparpotenzial_es = netto_es - (miete_es_jahr + leb_es)

# Vergleich
if netto_ch > netto_es:
    empfehlung_netto = "Schweiz"
else:
    empfehlung_netto = "Spanien"

if sparpotenzial_ch > sparpotenzial_es:
    empfehlung_spar = "Schweiz"
else:
    empfehlung_spar = "Spanien"

col1, col2 = st.columns(2)

with col1:
    st.subheader("Schweiz")
    st.write(f"Nettoeinkommen: {netto_ch:.2f}")
    st.write(f"Sparpotenzial: {sparpotenzial_ch:.2f}")
    st.write(f"Gesamtkosten: {gesamtkosten_ch:.2f}")

with col2:
    st.subheader("Spanien")
    st.write(f"Nettoeinkommen: {netto_es:.2f}")
    st.write(f"Sparpotenzial: {sparpotenzial_es:.2f}")
    st.write(f"Gesamtkosten: {gesamtkosten_es:.2f}")

st.markdown("---")
st.subheader("Empfehlung")
st.write(f"Basierend auf Nettoeinkommen: **{empfehlung_netto}** ist vorteilhafter.")
st.write(f"Basierend auf Sparpotenzial: **{empfehlung_spar}** ist vorteilhafter.")

# Optionale weitere Kriterien:
# Hier können noch mehr Kriterien oder Gewichtungen eingeführt werden,
# um eine Gesamtbewertung abzugeben.