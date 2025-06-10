import streamlit as st
import pandas as pd

st.set_page_config(page_title="Energievoorschot Checker", page_icon="🔌", layout="centered")
st.title("🔌 Energievoorschot Checker")

st.markdown("""
Upload je **verbruiksgegevens** en **voorschotinfo** om automatisch te berekenen of je moet bijbetalen of geld terugkrijgt aan het einde van je energiecontract.
""")

st.sidebar.header("📤 Gegevens invoeren")

elek_file = st.sidebar.file_uploader("📄 Elektriciteitsverbruik (CSV of Excel)")
gas_file = st.sidebar.file_uploader("📄 Gasverbruik (CSV of Excel)")

elek_tarief = st.sidebar.number_input("💶 Elektriciteitsprijs per kWh (alles inbegrepen)", value=0.2610, step=0.001)
gas_tarief = st.sidebar.number_input("💶 Gasprijs per kWh (alles inbegrepen)", value=0.0921, step=0.001)

vast_elek = st.sidebar.number_input("📦 Jaarlijkse vaste kosten elektriciteit (€)", value=90.72)
vast_gas = st.sidebar.number_input("📦 Jaarlijkse vaste kosten gas (€)", value=57.94)

voorschot_elek = st.sidebar.number_input("💳 Maandelijks voorschot elektriciteit (€)", value=55.0)
voorschot_gas = st.sidebar.number_input("💳 Maandelijks voorschot gas (€)", value=132.0)

maanden = st.sidebar.slider("📅 Aantal maanden in contractjaar", 1, 12, 12)

def lees_bestand(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

if elek_file and gas_file:
    df_elek = lees_bestand(elek_file)
    df_gas = lees_bestand(gas_file)

    totaal_elek = df_elek.iloc[:, 1].sum()
    totaal_gas = df_gas.iloc[:, 1].sum()

    kost_elek = totaal_elek * elek_tarief + vast_elek
    kost_gas = totaal_gas * gas_tarief + vast_gas

    betaald_elek = voorschot_elek * maanden
    betaald_gas = voorschot_gas * maanden

    saldo_elek = betaald_elek - kost_elek
    saldo_gas = betaald_gas - kost_gas

    totaal_kost = kost_elek + kost_gas
    totaal_betaald = betaald_elek + betaald_gas
    totaal_saldo = totaal_betaald - totaal_kost

    st.subheader("📊 Resultaten")
    col1, col2 = st.columns(2)
    col1.metric("⚡ Elektriciteit: saldo", f"€{saldo_elek:.2f}", delta_color="inverse")
    col2.metric("🔥 Gas: saldo", f"€{saldo_gas:.2f}", delta_color="inverse")
    st.metric("💰 Totaal saldo", f"€{totaal_saldo:.2f}", delta_color="inverse")

    if totaal_saldo < 0:
        resterend_maanden = 12 - len(df_elek)
        extra_per_maand = abs(totaal_saldo) / resterend_maanden if resterend_maanden > 0 else 0
        st.warning(f"📌 Tip: verhoog je voorschotten met ± €{extra_per_maand:.2f}/maand om uit te komen op €0.")

    st.markdown("### 📥 Detailtabellen")
    st.write("**Elektriciteitsverbruik**")
    st.dataframe(df_elek)
    st.write("**Gasverbruik**")
    st.dataframe(df_gas)
else:
    st.info("⬅️ Upload je gegevens in de zijbalk om te beginnen.")
