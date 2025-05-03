import streamlit as st
import pandas as pd
from service.export_service import generate_pdf  # Import de la fonction d’export PDF

def show():
    st.header("🧾 Gestion des Factures")

    # Initialisation des données
    if "factures_data" not in st.session_state:
        st.session_state["factures_data"] = pd.DataFrame(columns=["ID", "Date", "Client", "Total HT", "TVA", "Total TTC"])
    
    if "ligne_factures" not in st.session_state:
        st.session_state["ligne_factures"] = []

    date_facture = st.date_input("📅 Date")

    # Sélection du client
    if "config_data" in st.session_state and not st.session_state["config_data"].empty:
        client_selection = st.selectbox("Sélectionner un client", st.session_state["config_data"]["Nom"])
    else:
        st.warning("⚠️ Aucun client enregistré. Ajoutez-en dans l'onglet Configuration.")
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
            new_id = len(st.session_state["factures_data"]) + 1
            new_facture = {"ID": new_id, "Date": date_facture, "Client": client_selection, "Total HT": total_ht, "TVA": total_tva, "Total TTC": total_ttc}
            st.session_state["factures_data"] = pd.concat([st.session_state["factures_data"], pd.DataFrame([new_facture])], ignore_index=True)
            st.success("✅ Facture enregistrée avec succès !")

        if st.button("Exporter en PDF"):
            generate_pdf(client_selection, date_facture, st.session_state["ligne_factures"], total_ht, total_tva, total_ttc, facture_num)
            st.success("📄 Facture exportée en PDF avec succès !")
