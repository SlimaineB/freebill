import os
import streamlit as st
from service import db_service

def show():
    st.header("🏢 Configuration des Entreprises")

    # ✅ Sélection d'une entreprise
    entreprises = db_service.get_entreprises()
    noms_entreprises = [e["nom"] for e in entreprises] if entreprises else []
    nom_entreprise = st.selectbox("🔎 Sélectionner une entreprise", noms_entreprises)

    # Charger les infos de l'entreprise sélectionnée
    config = db_service.get_entreprise_by_name(nom_entreprise)[0] if nom_entreprise else {
        "nom": "", "adresse": "", "telephone": "", "email": "",
        "siret": "", "tva": "", "rib": "", "logo": "assets/logo.png",
        "tjm": 0.0, "libelle_court": ""  # ✅ Nouveau champ : Libellé Court
    }

    print(config)

    # Formulaire de modification
    config["nom"] = st.text_input("Nom de l'entreprise", config["nom"])
    config["adresse"] = st.text_area("Adresse complète", config["adresse"])
    config["telephone"] = st.text_input("Téléphone", config["telephone"])
    config["email"] = st.text_input("Email", config["email"])
    config["siret"] = st.text_input("Numéro SIRET", config["siret"])
    config["tva"] = st.text_input("Numéro TVA", config["tva"])
    config["rib"] = st.text_input("IBAN / RIB", config["rib"])
    config["logo"] = st.text_input("Chemin du logo", config["logo"])

    # ✅ Ajout du TJM et Libellé Court pour les factures
    config["tjm"] = st.number_input("💰 Taux Journalier Moyen (TJM)", min_value=0.0, format="%.2f", key="tjm")
    config["libelle_court"] = st.text_input("📝 Libellé Court (utilisé comme label par défaut sur les factures)", config["libelle_court"])

    # ✅ Enregistrer ou Mettre à jour l'entreprise
    if st.button("Enregistrer"):
        db_service.save_entreprise(config)
        st.success("✅ Configuration mise à jour avec succès !")

    # ✅ Aperçu du logo
    if os.path.exists(config["logo"]):
        st.image(config["logo"], width=150)

    # ✅ Supprimer l'entreprise sélectionnée
    if nom_entreprise and st.button("🗑️ Supprimer cette entreprise"):
        db_service.delete_entreprise(nom_entreprise)
        st.warning(f"⚠️ L'entreprise '{nom_entreprise}' a été supprimée !")
