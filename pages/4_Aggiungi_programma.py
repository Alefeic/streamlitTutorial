import streamlit as st
from utils.utils import *
import datetime


def check_info(lesson_dict):
    for value in lesson_dict.values():
        if value=='':
            return False
    return True

def get_instructors():
    query = "SELECT CodFisc FROM Istruttore"
    result = execute_query(st.session_state["connection"], query)
    return [row['CodFisc'] for row in result.mappings()]

def get_courses():
    query = "SELECT CodC FROM Corsi"
    result = execute_query(st.session_state["connection"], query)
    return [row['CodC'] for row in result.mappings()]

def insert_lesson(lesson_dict):
    if check_info(lesson_dict):
        attributi = ", ".join(lesson_dict.keys())
        valori = tuple(lesson_dict.values())
        query = f"insert into Programma ({attributi}) values {valori};"
        try:
            execute_query(st.session_state["connection"], query)
            st.session_state["connection"].commit()
        except Exception as e:
            st.error(e)
            return False
        return True
    else:
        return False

def check_lesson_exists(CodC, Giorno):
    query = f"SELECT * FROM Programma WHERE CodC='{CodC}' AND Giorno='{Giorno}'"
    result = execute_query(st.session_state["connection"], query)
    return len(result.fetchall()) > 0

def create_lesson_form():
    with st.form("Nuova lezione settimanale"):
        st.header("Aggiungi :red[nuova] lezione :date:")

        CodFisc = st.selectbox("Codice fiscale istruttore", get_instructors())
        Giorno = st.selectbox("Giorno", ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"])
        OraInizio = st.slider("Ora di inizio :clock1:", 0, 23, 0)
        MinutiInizio = st.slider("Minuti di inizio :clock10:", 0, 59, 0)
        Durata = st.slider("Durata (minuti) :alarm_clock:", 0, 60, 0)
        CodC = st.selectbox("Codice corso", get_courses())
        Sala = st.text_input("Sala", placeholder="Inserisci sala")

        submitted = st.form_submit_button("Salva", type='primary')
        lesson_dict = {
            "CodFisc": CodFisc,
            "Giorno": Giorno,
            "OraInizio": f"{OraInizio:02}:{MinutiInizio:02}",
            "Durata": Durata,
            "CodC": CodC,
            "Sala": Sala
        }

        if submitted:
            if Durata > 60:
                st.error("La durata della lezione non può superare i 60 minuti.")
            elif Giorno not in ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]:
                st.error("Il giorno deve essere compreso tra Lunedì e Venerdì.")
            elif check_lesson_exists(CodC, Giorno):
                st.error(f"Esiste già una lezione per il corso {CodC} il giorno {Giorno} :x:")
            else:
                if insert_lesson(lesson_dict):
                    st.success("Lezione inserita correttamente :white_check_mark:")
                else:
                    st.error("Errore durante l'inserimento della lezione :x:")

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
    st.title("Inserimento :blue[Lezione]")
    st.subheader("Puoi :blue[inserire] lezioni completando ciascuna richiesta del :red[form] :smile:")
    if check_connection():
        create_lesson_form()