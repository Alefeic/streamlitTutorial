import streamlit as st
from utils.utils import *
import pandas as pd


def get_list(attributo):
    query = f"select distinct {attributo} from Istruttore"
    result = execute_query(st.session_state["connection"], query)
    result_list=[]
    for row in result.mappings():
        result_list.append(row[attributo])
    return result_list


def get_info2():
    return get_list("Cognome"), get_list("DataNascita")

st.set_page_config(
        page_title="Laboratorio 4",
        page_icon=':muscle:',
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://dbdmg.polito.it/',
            'Report a bug': "https://dbdmg.polito.it/",
            'About': "# Corso di *Basi di Dati*, laboratorio 4 di :red[Tortoroglio Alessio]"
        }
    )
st.title("Visualizzazione :blue[istruttori]")
st.subheader("Puoi :blue[filtrare] per varie categorie, :violet[sotto] :arrow_down: vedrai i risultati.")

if "connection" not in st.session_state.keys():
        st.session_state["connection"] = False


if check_connection():

    with st.expander("Filtra per Cognome e data di nascita", True):
        query = "SELECT CodFisc as 'Codice', Nome AS 'Nome', Cognome AS 'Cognome', DataNascita, Email AS 'E-mail', Telefono AS 'Numero di telefono' FROM Istruttore"
        ist_col1, ist_col2 = st.columns([3, 3])
        sort_param = ist_col1.radio("Ordina per: ", ['Codice', 'Nome', 'Cognome', 'DataNascita'])
        sort_choice = ist_col2.selectbox("Ordine: ", ['Crescente', 'Decrescente'])
        sort_dict={'Crescente': 'ASC', 'Decrescente': 'DESC'}
        filter = ist_col1.multiselect("Filtra per:", ['Cognome', 'DataNascita'])

        query2 = "SELECT MIN(DataNascita), MAX(DataNascita) from Istruttore"
        data = execute_query(st.session_state["connection"], query2)
        min_max = [dict(zip(data.keys(), result)) for result in data]
        min_value = min_max[0]['MIN(DataNascita)']
        max_value = min_max[0]['MAX(DataNascita)']

        query += " WHERE 1=1"
        Cognome, Data_nascita = get_info2()
        if ("Cognome" in filter):
            surname = st.selectbox("Cognome", Cognome)
            query += f" AND Cognome='{surname}'"
        if ("DataNascita" in filter):
            birthdate = st.date_input("Selezionare il range di date di nascita", value=(min_value, max_value), min_value=min_value, max_value=max_value)
            query += f" AND DataNascita >= '{birthdate[0]}' AND DataNascita <= '{birthdate[1]}'"


        query += f" ORDER BY {sort_param} {sort_dict[sort_choice]}"
        istruttori = execute_query(st.session_state["connection"], query)
        df_istruttori = pd.DataFrame(istruttori)
        if df_istruttori.empty:
            st.error("Istruttore inesistente :x:")
        else:
            for idx, row in df_istruttori.iterrows():
                st.write(f"### Istruttore :red[{idx + 1}] :white_check_mark:")
                st.markdown(
                    f"""
                    <div style="background-color: #000010; padding: 10px; border-radius: 5px;">
                        <p><b>Codice:</b> {row['Codice']}</p>
                        <p><b>Nome:</b> {row['Nome']}</p>
                        <p><b>Cognome:</b> {row['Cognome']}</p>
                        <p><b>Data di nascita:</b> {row['DataNascita']}</p>
                        <p><b>Email:</b> {row['E-mail']}</p>
                        <p><b>Numero di telefono:</b> {row['Numero di telefono']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                