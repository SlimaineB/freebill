import streamlit as st
import pandas as pd
import datetime

def show():
    st.header("🧾 Gestion des Notes de Frais")

    if "frais_data" not in st.session_state:
        st.session_state["frais_data"] = pd.DataFrame(columns=["ID", "Date", "Type", "Montant TTC", "TVA (%)", "Montant HT", "Description", "Mode de paiement", "Justificatif"])

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

    # Ajout du mode de paiement
    mode_paiement = st.selectbox("💳 Mode de paiement", ["Personnel", "Professionnel"], key="mode_paiement")

    # Ajout d'un justificatif (téléchargement de fichier)
    justificatif = st.file_uploader("📎 Ajouter un justificatif (PDF, JPG, PNG)", type=["pdf", "jpg", "png"], key="justificatif")

    if st.button("➕ Ajouter Note de Frais"):
        new_id = len(st.session_state["frais_data"]) + 1
        new_frais = {
            "ID": new_id, "Date": date_frais, "Type": type_frais, "Montant TTC": montant_ttc,
            "TVA (%)": taux_tva, "Montant HT": round(montant_ht, 2), "Description": description_frais,
            "Mode de paiement": mode_paiement, "Justificatif": justificatif.name if justificatif else "Aucun"
        }

        st.session_state["frais_data"] = pd.concat([st.session_state["frais_data"], pd.DataFrame([new_frais])], ignore_index=True)
        st.success("✅ Note de frais ajoutée avec succès !")

    st.subheader("🖊 Édition des Notes de Frais")

    # Ajout des listes déroulantes dans `st.data_editor()`
    st.session_state["frais_data"] = dynamic_input_data_editor(
        st.session_state["frais_data"],
        key="frais_data_editor",
        num_rows="dynamic",
        column_config={
            "Date": st.column_config.DateColumn(format="DD/MM/YYYY", step=1),
            "Type": st.column_config.SelectboxColumn(options=list(type_frais_options.keys())),
            "TVA (%)": st.column_config.NumberColumn(format="%.1f"),
            "Mode de paiement": st.column_config.SelectboxColumn(options=["Personnel", "Professionnel"]),
            "Justificatif": st.column_config.TextColumn()
        }
    )


def dynamic_input_data_editor(data, key, **_kwargs):
    """
    Like streamlit's data_editor but which allows you to initialize the data editor with input arguments that can
    change between consecutive runs. Fixes the problem described here: https://discuss.streamlit.io/t/data-editor-not-changing-cell-the-1st-time-but-only-after-the-second-time/64894/13?u=ranyahalom
    :param data: The `data` argument you normally pass to `st.data_editor()`.
    :param key: The `key` argument you normally pass to `st.data_editor()`.
    :param _kwargs: All other named arguments you normally pass to `st.data_editor()`.
    :return: Same result returned by calling `st.data_editor()`
    """
    changed_key = f'{key}_khkhkkhkkhkhkihsdhsaskskhhfgiolwmxkahs'
    initial_data_key = f'{key}_khkhkkhkkhkhkihsdhsaskskhhfgiolwmxkahs__initial_data'

    def on_data_editor_changed():
        if 'on_change' in _kwargs:
            args = _kwargs['args'] if 'args' in _kwargs else ()
            kwargs = _kwargs['kwargs'] if 'kwargs' in _kwargs else  {}
            _kwargs['on_change'](*args, **kwargs)
        st.session_state[changed_key] = True

    if changed_key in st.session_state and st.session_state[changed_key]:
        data = st.session_state[initial_data_key]
        st.session_state[changed_key] = False
    else:
        st.session_state[initial_data_key] = data
    __kwargs = _kwargs.copy()
    __kwargs.update({'data': data, 'key': key, 'on_change': on_data_editor_changed})
    return st.data_editor(**__kwargs)