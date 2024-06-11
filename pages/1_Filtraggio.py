import streamlit as st
from utils.utils import *
import pandas as pd

def get_list(attributo):
    query = f"select distinct {attributo} from Corsi"
    result = execute_query(st.session_state["connection"], query)
    result_list=[]
    for row in result.mappings():
        result_list.append(row[attributo])
    return result_list


def get_info():
    return get_list("CodC"), get_list("Nome"), get_list("Tipo"), get_list("Livello")


st.title("Visualizzazione :red[corsi]")
st.subheader("Puoi :blue[filtrare] per varie categorie, sulla :green[destra] vedrai il programma con relativo istruttore dei corsi selezionati.")

if "connection" not in st.session_state.keys():
        st.session_state["connection"] = False

if check_connection():
    col1, col2 = st.columns(2, gap="large")
    num_corsi = execute_query(st.session_state["connection"], "SELECT DISTINCT COUNT(*) as 'Numero di corsi' FROM Corsi")
    corsi_info_dict = [dict(zip(num_corsi.keys(), result)) for result in num_corsi]
    col1.metric("Numero di :blue[corsi] totale", f"{compact_format(corsi_info_dict[0]['Numero di corsi'])}")
    
    tipi = execute_query(st.session_state["connection"], "SELECT COUNT(DISTINCT Tipo) as 'Numero di tipi' FROM Corsi; ")
    tipi_info_dict = [dict(zip(tipi.keys(), result)) for result in tipi]
    col2.metric("Numero di :green[tipi] totale", f"{compact_format(tipi_info_dict[0]['Numero di tipi'])}")


    with col1.expander("Visualizza corsi", True):
        query = "SELECT CodC as 'Codice', Nome AS 'Nome', Tipo AS 'Tipo', Livello AS 'Livello' FROM Corsi"
        corsi_col1, corsi_col2 = st.columns([3, 3])
        sort_param = corsi_col1.radio("Ordina per: ", ['Codice', 'Nome', 'Tipo', 'Livello'])
        sort_choice = corsi_col2.selectbox("Ordine: ", ['Crescente', 'Decrescente'])
        sort_dict={'Crescente': 'ASC', 'Decrescente': 'DESC'}
        filter = corsi_col1.multiselect("Filtra per:", ['Codice', 'Nome', 'Tipo', 'Livello'])

        query += " WHERE 1=1"
        Codice, Nome, Tipo, Livello = get_info()
        if ("Codice" in filter):
            CodC = st.selectbox("Categoria", Codice)
            query += f" AND CodC='{CodC}'"
        if ("Nome" in filter):
            name = st.selectbox("Nome", Nome)
            query += f" AND Nome='{name}'"
        if ("Tipo" in filter):
            type = st.selectbox("Tipo", Tipo)
            query += f" AND Tipo='{type}'"
        if ("Livello" in filter):
            level = st.selectbox("Livello", Livello)
            query += f" AND Livello='{level}'"
  
        query += f" ORDER BY {sort_param} {sort_dict[sort_choice]}"
        corsi = execute_query(st.session_state["connection"], query)
        df_corsi = pd.DataFrame(corsi)
        if df_corsi.empty:
            st.error("Corso inesistente")
        else:
            st.dataframe(df_corsi, use_container_width=True)


    with col2.expander("Dettagli:", True):
        if not df_corsi.empty:
            codc_list = df_corsi['Codice'].tolist()
            codc_str = ','.join([f"'{codc}'" for codc in codc_list])
            query2 = f"SELECT CodC as 'Codice', Giorno AS 'Giorno', OraInizio AS 'Ora di inizio', Durata AS 'Durata', Sala AS 'Sala', Nome AS 'Nome', Cognome AS 'Cognome' FROM Programma, Istruttore WHERE Programma.CodFisc=Istruttore.CodFisc AND CodC IN ({codc_str})"
            vedi = execute_query(st.session_state["connection"], query2)
            df_vedi = pd.DataFrame(vedi)
            if df_vedi.empty:
                st.error("Programma assente")
            else:
                st.dataframe(df_vedi, use_container_width=True)
        else:
            st.error("Corso inesistente")
