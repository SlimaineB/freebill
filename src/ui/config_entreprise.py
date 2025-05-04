import streamlit as st
from service import db_service

def show():
    st.header("🏢 Configuration de l'Entreprise")



    # Charger les infos actuelles
    config = db_service.get_entreprise_info() or {
        "nom": "", "adresse": "", "telephone": "", "email": "",
        "siret": "", "tva": "", "rib": "", "logo": "assets/logo.png"
    }

    # Formulaire de modification
    config["nom"] = st.text_input("Nom de l'entreprise", config["nom"])
    config["adresse"] = st.text_area("Adresse complète", config["adresse"])
    config["telephone"] = st.text_input("Téléphone", config["telephone"])
    config["email"] = st.text_input("Email", config["email"])
    config["siret"] = st.text_input("Numéro SIRET", config["siret"])
    config["tva"] = st.text_input("Numéro TVA", config["tva"])
    config["rib"] = st.text_input("IBAN / RIB", config["rib"])
    config["logo"] = st.text_input("Chemin du logo", config["logo"])

    # Sauvegarde des infos
    if st.button("Enregistrer"):
        db_service.save_entreprise_info(config)
        st.success("✅ Configuration mise à jour avec succès !")

    # Aperçu du logo
    st.image(config["logo"], width=150)

    # Suppression des infos
    if st.button("🔄 Réinitialiser"):
        db_service.reset_entreprise_info()
        st.warning("⚠️ Les données ont été supprimées !")
