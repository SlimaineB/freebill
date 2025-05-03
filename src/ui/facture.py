import streamlit as st
import pandas as pd

def show():
    st.header("Gestion des Notes de Frais")

    if "frais_data" not in st.session_state:
        st.session_state["frais_data"] = pd.DataFrame(columns=["ID", "Date", "Montant", "Description"])

    date_frais = st.date_input("Date", key="date_frais")
    montant_frais = st.number_input("Montant", min_value=0.0, format="%.2f", key="montant_frais")
    description_frais = st.text_area("Description", key="description_frais")

    if st.button("Ajouter Note de Frais"):
        new_id = len(st.session_state["frais_data"]) + 1
        new_frais = {"ID": new_id, "Date": date_frais, "Montant": montant_frais, "Description": description_frais}
        st.session_state["frais_data"] = pd.concat([st.session_state["frais_data"], pd.DataFrame([new_frais])], ignore_index=True)
        st.success("✅ Note de frais ajoutée avec succès !")

    st.dataframe(st.session_state["frais_data"])
