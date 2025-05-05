import streamlit as st
from service import db_service
from ui import frais
import ui.config_client_fournisseur as config_client_fournisseur
import ui.config_entreprise as config_entreprise  # ✅ Correction ici
import ui.facture as facture

# Initialiser la BDD
db_service.init_db()

#Page size to all available
st.set_page_config(layout="wide")

# Chargement du logo
st.sidebar.title("📊 Tableau de bord")



# Menu latéral structuré
option = st.sidebar.radio("📌 Navigation", ["🏢 Configuration Client/Fournisseur", "🏢 Configuration Entreprise", "🧾 Factures", "💰 Notes de frais"])

# Redirection vers les pages correspondantes
if option == "🏢 Configuration Client/Fournisseur":
    config_client_fournisseur.show()
elif option == "🏢 Configuration Entreprise":
    config_entreprise.show()
elif option == "🧾 Factures":
    facture.show()
elif option == "💰 Notes de frais":
    frais.show()
