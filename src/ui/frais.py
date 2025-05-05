import streamlit as st
import pandas as pd
import datetime

def show():
    st.header("🧾 Gestion des Notes de Frais")

    if "frais_data" not in st.session_state:
        st.session_state["frais_data"] = pd.DataFrame(columns=["ID", "Date", "Type", "Montant TTC", "TVA (%)", "Montant HT", "Description"])

    # Pré-remplir la date avec aujourd’hui
    date_frais = st.date_input("📅 Date", value=datetime.date.today(), key="date_frais")

    # Liste déroulante pour le type de frais
    type_frais_options = {
        "Repas": 10,
        "Transport": 5.5,
        "Poste": 20,
        "Hébergement": 10,
        "Divers": 20
    }
    type_frais = st.selectbox("🛠 Type de Note de Frais", list(type_frais_options.keys()), key="type_frais")

    # Calcul automatique du taux de TVA selon le type
    taux_tva = st.number_input("📊 Taux de TVA (%)", min_value=0.0, value=float(type_frais_options[type_frais]), format="%.1f", key="taux_tva")

    montant_ttc = st.number_input("💰 Montant TTC (€)", min_value=0.0, format="%.2f", key="montant_ttc")

    montant_ht = montant_ttc / (1 + (taux_tva / 100))  # ✅ Calcul automatique

    description_frais = st.text_area("📝 Description", key="description_frais")

    if st.button("➕ Ajouter Note de Frais"):
        new_id = len(st.session_state["frais_data"]) + 1
        new_frais = {"ID": new_id, "Date": date_frais, "Type": type_frais, "Montant TTC": montant_ttc, 
                     "TVA (%)": taux_tva, "Montant HT": round(montant_ht, 2), "Description": description_frais}
        
        st.session_state["frais_data"] = pd.concat([st.session_state["frais_data"], pd.DataFrame([new_frais])], ignore_index=True)
        st.success("✅ Note de frais ajoutée avec succès !")

    st.subheader("🖊 Édition des Notes de Frais")
    
    # Ajout des listes déroulantes dans `st.data_editor()`
    st.session_state["frais_data"] = st.data_editor(
        st.session_state["frais_data"],
        num_rows="dynamic",
        column_config={
            "Date": st.column_config.DateColumn(format="DD/MM/YYYY",step=1),
            "Type": st.column_config.SelectboxColumn(options=list(type_frais_options.keys())),
            "TVA (%)": st.column_config.NumberColumn(format="%.1f")
        }
    )
