import streamlit as st
from ui import frais
import ui.config as config
import ui.facture as facture


# Menu latéral
st.sidebar.title("Menu")
option = st.sidebar.radio("Choisir une page :", ["Configuration", "Factures", "Notes de frais"])

if option == "Configuration":
    config.show()
elif option == "Factures":
    facture.show()
elif option == "Notes de frais":
    frais.show()
