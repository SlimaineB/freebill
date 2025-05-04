import streamlit as st
import pandas as pd
import service.db_service as db_service  # Remplacez ceci par votre module de gestion de la base de données

def show():
    st.header("Gestion des Clients et Fournisseurs")

    # Chargement des données depuis la base de données
    config_data = db_service.get_all_clients_fournisseurs()  # Une fonction pour récupérer les clients et fournisseurs

    # Formulaire d'ajout
    nom = st.text_input("Nom")
    adresse = st.text_input("Adresse")
    siret = st.text_input("SIRET")
    num_tva = st.text_input("Numéro de TVA")
    type_personne = st.selectbox("Type", ["Client", "Fournisseur"]) 

    if st.button("Ajouter"):
        if type_personne == "Client":
            new_id = db_service.add_client(nom, adresse, siret, num_tva)
        else:
            new_id = db_service.add_fournisseur(nom, adresse, siret, num_tva)
        st.success(f"✅ {type_personne} {nom} ajouté avec succès !")

    # Filtre
    filtre = st.selectbox("Filtrer les résultats :", ["Tous", "Clients", "Fournisseurs"])
    if filtre == "Clients":
        data_filtered = [row for row in config_data if row["Type"] == "Client"]
    elif filtre == "Fournisseurs":
        data_filtered = [row for row in config_data if row["Type"] == "Fournisseur"]
    else:
        data_filtered = config_data

    st.dataframe(pd.DataFrame(data_filtered))

    # Suppression d'un client/fournisseur
    if data_filtered:
        id_to_delete = st.selectbox("Sélectionner un ID à supprimer", [row["ID"] for row in data_filtered])
        if st.button("Supprimer"):
            db_service.delete(id_to_delete)
            st.success("🗑️ Suppression réussie !")
