import streamlit as st
import pandas as pd
from service import db_service
from service.export_service import generate_pdf  # Import de la fonction d’export PDF

def show():

    tab1, tab2 = st.tabs(["💰 Nouvelle Facture", "🔍 Recherche Factures"])

    with tab1:
        new_facture()  # Ta fonction de création de factures

    with tab2:
        search_factures()  # Fonction de recherche des factu


def new_facture():

    st.header("🧾 Gestion des Factures")

    # Initialisation des données
    if "factures_data" not in st.session_state:
        st.session_state["factures_data"] = pd.DataFrame(columns=["ID", "Date", "Client", "Total HT", "TVA", "Total TTC"])
    
    if "ligne_factures" not in st.session_state:
        st.session_state["ligne_factures"] = []

    date_facture = st.date_input("📅 Date")
 
    # Sélection de l'entrteprise
    print(db_service.get_entreprises())
    print(db_service.get_clients())
    if len(db_service.get_entreprises()) > 0:
        entreprise_selection = st.selectbox("Sélectionner votre entreprise", [entreprise["nom"] for entreprise in db_service.get_entreprises()])
    else:
        st.warning("⚠️ Aucune entreprise enregistrée. Ajoutez-en dans l'onglet Configuration Entreprise.")
        entreprise_selection = None


    # Sélection du client
    if len(db_service.get_clients()) > 0:
        client_selection = st.selectbox("Sélectionner un client", [client["nom"] for client in db_service.get_clients()])
    else:
        st.warning("⚠️ Aucun client enregistré. Ajoutez-en dans l'onglet Configuration Client/Fournisseur.")
        client_selection = None

    # Ajout des lignes de factures
    st.subheader("📌 Ajouter une ligne à la facture")
    description = st.text_input("Description du produit/service")
    quantite = st.number_input("Quantité", min_value=1)
    montant_unitaire = st.number_input("Montant unitaire (€)", min_value=0.0, format="%.2f")
    taux_tva = st.selectbox("Taux de TVA (%)", [5.5, 10, 20])
    facture_num = st.text_input("Numéro de facture")

    if st.button("Ajouter Ligne"):
        montant_ht = quantite * montant_unitaire
        montant_tva = montant_ht * (taux_tva / 100)
        montant_ttc = montant_ht + montant_tva
        
        ligne = {"Description": description, "Quantité": quantite, "Montant Unitaire": montant_unitaire, "TVA": taux_tva, "Total TTC": montant_ttc}
        st.session_state["ligne_factures"].append(ligne)
        st.success("✅ Ligne ajoutée avec succès !")

    # Affichage des lignes ajoutées
    st.subheader("📄 Lignes de factures")
    if st.session_state["ligne_factures"]:
        df_lignes = pd.DataFrame(st.session_state["ligne_factures"])
        st.table(df_lignes)

        # Calcul du total
        total_ht = sum(l["Quantité"] * l["Montant Unitaire"] for l in st.session_state["ligne_factures"])
        total_tva = sum((l["Quantité"] * l["Montant Unitaire"]) * (l["TVA"] / 100) for l in st.session_state["ligne_factures"])
        total_ttc = total_ht + total_tva

        st.write(f"**Total HT :** {total_ht:.2f} €")
        st.write(f"**Total TVA :** {total_tva:.2f} €")
        st.write(f"**Total TTC :** {total_ttc:.2f} €")

        if st.button("Enregistrer Facture"):
            client = db_service.get_client_by_name(client_selection)[0]
            entreprise = db_service.get_entreprise_by_name(entreprise_selection)[0]
            new_id = len(st.session_state["factures_data"]) + 1
            new_facture = {"ID": new_id, "Date": date_facture,"Entreprise": entreprise_selection ,"Client": client_selection, "Total HT": total_ht, "TVA": total_tva, "Total TTC": total_ttc}
            st.session_state["factures_data"] = pd.concat([st.session_state["factures_data"], pd.DataFrame([new_facture])], ignore_index=True)

            db_service.add_facture(entreprise["id"], client["id"] , date_facture, total_ht, total_tva, total_ttc)
            st.success("✅ Facture enregistrée avec succès !")

        if st.button("Exporter en PDF", key="export_pdf_one"):
            entreprise = db_service.get_entreprise_by_name(entreprise_selection)[0]
            client = db_service.get_client_by_name(client_selection)[0]
            generate_pdf(entreprise, client, date_facture, st.session_state["ligne_factures"], total_ht, total_tva, total_ttc, facture_num)
            st.success("📄 Facture exportée en PDF avec succès !")




def search_factures():
    st.header("🔍 Recherche de Factures")

    # Récupération des données depuis la base de données
    factures = db_service.get_factures()

    # Vérifier si des factures existent
    if not factures:
        st.warning("⚠️ Aucune facture trouvée.")
        return

    # Sélection du client pour filtrer
    clients = list(set(facture["nom"] for facture in factures))
    client_filter = st.selectbox("Sélectionner un client", ["Tous"] + clients)

    # Sélection de la date pour filtrer
    date_filter = st.date_input("📅 Filtrer par date (optionnel)")

    # Application des filtres
    filtered_factures = factures
    if client_filter != "Tous":
        filtered_factures = [facture for facture in filtered_factures if facture["nom"] == client_filter]
    if date_filter:
        filtered_factures = [facture for facture in filtered_factures if facture["date"] == date_filter.strftime("%Y-%m-%d")]

    # Affichage des factures filtrées
    st.subheader("📝 Résultats de recherche")
    if filtered_factures:
        df_factures = pd.DataFrame(filtered_factures)
        st.table(df_factures)
    else:
        st.warning("⚠️ Aucune facture trouvée pour ce filtre.")

    # Export PDF de la facture sélectionnée
    facture_selection = st.selectbox("📄 Sélectionner une facture à exporter", [f"{facture['id']} - {facture['nom']} ({facture['date']})" for facture in filtered_factures])
    if st.button("Exporter en PDF", key="export_pdf_all"):
        facture_id = int(facture_selection.split(" - ")[0])  # Récupérer l'ID de la facture
        facture_details = next(facture for facture in factures if facture["id"] == facture_id)
        generate_pdf(facture_details["nom"], facture_details["date"], [], facture_details["total_ht"], facture_details["total_tva"], facture_details["total_ttc"], facture_id)
        st.success("✅ Facture exportée en PDF avec succès !")

