import streamlit as st
import pandas as pd
import datetime
import service.db_service as db_service

def show():
    st.header("🧾 Gestion des Notes de Frais")

    # 📅 Saisie des informations
    date_frais = st.date_input("📅 Date", value=datetime.date.today(), key="date_frais")

    type_frais_options = {
        "Repas": 10, "Transport": 5.5, "Poste": 20, "Hébergement": 10, "Divers": 20
    }

    type_frais = st.selectbox("🛠 Type de Note de Frais", list(type_frais_options.keys()), key="type_frais")
    taux_tva = st.number_input("📊 Taux de TVA (%)", min_value=0.0, value=float(type_frais_options[type_frais]), format="%.1f", key="taux_tva")
    montant_ttc = st.number_input("💰 Montant TTC (€)", min_value=0.0, format="%.2f", key="montant_ttc")
    montant_ht = montant_ttc / (1 + (taux_tva / 100))  
    description_frais = st.text_area("📝 Description", key="description_frais")
    mode_paiement = st.selectbox("💳 Mode de paiement", ["Personnel", "Professionnel"], key="mode_paiement")
    justificatif = st.file_uploader("📎 Ajouter un justificatif (PDF, JPG, PNG)", type=["pdf", "jpg", "png"], key="justificatif")

    # ✅ Ajouter une nouvelle note de frais en BDD avec une date stockée correctement
    if st.button("➕ Ajouter Note de Frais"):
        db_service.add_frais(date_frais, type_frais, montant_ttc, taux_tva, montant_ht, description_frais, mode_paiement, 
                  justificatif.name if justificatif else "Aucun")
        st.success("✅ Note de frais ajoutée avec succès !")

    st.subheader("🖊 Édition des Notes de Frais")

    # ✅ Charger les frais depuis la BDD sans bidouiller la date
    frais_data = pd.DataFrame(db_service.get_frais())

# Convert the 'date' column to datetime format
    if "date" in frais_data.columns:
        frais_data["date"] = pd.to_datetime(frais_data["date"], format="%Y-%m-%d")


    # ✅ Modifier les données via `st.data_editor()`
    updated_data = st.data_editor(
        frais_data, key="frais_data_editor", num_rows="dynamic",
        column_config={
            "date": st.column_config.DateColumn(format="DD/MM/YYYY", step=1),
            "type": st.column_config.SelectboxColumn(options=list(type_frais_options.keys())),
            "tva": st.column_config.NumberColumn(format="%.1f"),
            "mode_paiement": st.column_config.SelectboxColumn(options=["Personnel", "Professionnel"]),
            "justificatif": st.column_config.TextColumn()
        }
    )

    # ✅ Sauvegarder les modifications en BDD
    if st.button("💾 Enregistrer les modifications"):
        db_service.update_frais(updated_data.to_dict(orient="records"))
        st.success("✅ Modifications enregistrées dans la base de données !")
