import streamlit as st
from ui import frais
import ui.config as config
import ui.config_entreprise as config_entreprise  # ✅ Correction ici
import ui.facture as facture

# Chargement du logo
st.sidebar.title("📊 Tableau de bord")

# Menu latéral structuré
option = st.sidebar.radio("📌 Navigation", ["🏢 Configuration Générale", "🏢 Configuration Entreprise", "🧾 Factures", "💰 Notes de frais"])

# Redirection vers les pages correspondantes
if option == "🏢 Configuration Générale":
    config.show()
elif option == "🏢 Configuration Entreprise":
    config_entreprise.show()
elif option == "🧾 Factures":
    facture.show()
elif option == "💰 Notes de frais":
    frais.show()
