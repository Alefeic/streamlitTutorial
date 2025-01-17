import streamlit as st
from utils.utils import *
import pandas as pd
import datetime


def check_info(ist_dict):
    i=-1
    for value in ist_dict.values():
        i=i+1
        if value=='' and i!=5:
            return False
    return True


def insert(ist_dict):
    if check_info(ist_dict):
        attributi = ", ".join(ist_dict.keys())
        valori = tuple(ist_dict.values())
        query = f"insert into Istruttore ({attributi}) values {valori};"
        try:
            execute_query(st.session_state["connection"], query)
            st.session_state["connection"].commit()
        except Exception as e:
            st.error(e)
            return False
        return True
    else:
        return False


def create_form():
    with st.form("Nuovo istruttore"):
        st.header("Aggiungi :violet[istruttore]:")

        code = st.text_input("Codice fiscale", placeholder = "Inserisci codice fiscale")
        nome = st.text_input("Nome", placeholder = "Inserisci nome istruttore")
        cognome = st.text_input("Cognome", placeholder = "Inserisci cognome istruttore")
        valore = datetime.date(2019, 7, 6)
        mindate = datetime.date(1900, 1, 1)
        maxdate = datetime.datetime.today()
        datanascita = st.date_input("Data di nascita :date:", valore, min_value=mindate, max_value=maxdate)
        email = st.text_input("Email", placeholder="mario.rossi@gmail.com")
        telefono = st.text_input("Numero di telefono :phone:", placeholder="Inserisci numero di telefono (opzionale)") 

        submitted = st.form_submit_button("Salva", type = 'primary')
        ist_dict = {"CodFisc": code, "Nome": nome, "Cognome": cognome, "DataNascita": datanascita.strftime("%Y-%m-%D"), "Email": email, "Telefono": telefono}

        if submitted:
            if insert(ist_dict):
                st.success("Hai inserito un nuovo prodotto :white_check_mark:")
            else:
                st.error("Errore di inserimento :x:")


if __name__ == "__main__":
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
    st.title("Inserimento :blue[istruttori]")
    st.subheader("Puoi :blue[inserire] istruttori completando ciascuna richiesta nel :violet[form] :arrow_down:")
    if check_connection():
        create_form()
