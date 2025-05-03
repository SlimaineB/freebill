import streamlit as st
import pandas as pd

def show():
    st.header("Gestion des Clients et Fournisseurs")

    if "config_data" not in st.session_state:
        st.session_state["config_data"] = pd.DataFrame(columns=["ID", "Nom", "Adresse", "SIRET", "Numéro TVA", "Type"])

    # Saisie des informations
    nom = st.text_input("Nom")
    adresse = st.text_input("Adresse")
    siret = st.text_input("SIRET")
    num_tva = st.text_input("Numéro de TVA")
    type_personne = st.selectbox("Type", ["Client", "Fournisseur"])  # Sélection du type

    if st.button("Ajouter"):
        new_id = len(st.session_state["config_data"]) + 1
        new_entry = {
            "ID": new_id, "Nom": nom, "Adresse": adresse,
            "SIRET": siret, "Numéro TVA": num_tva, "Type": type_personne
        }
        st.session_state["config_data"] = pd.concat([st.session_state["config_data"], pd.DataFrame([new_entry])], ignore_index=True)
        st.success(f"✅ {type_personne} {nom} ajouté avec succès !")

    # Filtre : Affichage des Clients ou Fournisseurs
    filtre = st.selectbox("Filtrer les résultats :", ["Tous", "Clients", "Fournisseurs"])
    
    if filtre == "Clients":
        data_filtered = st.session_state["config_data"][st.session_state["config_data"]["Type"] == "Client"]
    elif filtre == "Fournisseurs":
        data_filtered = st.session_state["config_data"][st.session_state["config_data"]["Type"] == "Fournisseur"]
    else:
        data_filtered = st.session_state["config_data"]

    st.dataframe(data_filtered)
