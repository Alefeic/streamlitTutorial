import streamlit as st
import numpy as np
import pandas as pd
from utils.utils import *
import pymysql,cryptography

if __name__ == "__main__":
    st.set_page_config(
        page_title="Laboratorio 4",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://dbdmg.polito.it/',
            'Report a bug': "https://dbdmg.polito.it/",
            'About': "# Corso di *Basi di Dati*, laboratorio 4 di :red[Tortoroglio Alessio]"
        }
    )

    if "connection" not in st.session_state.keys():
        st.session_state["connection"] = False

    col1,col2=st.columns([3,2])
    with col1:
        st.title("Laboratorio :red[4]")
        st.markdown("## Costruito da :blue[Tortoroglio Alessio]")
        st.markdown("#### In questo laboratorio l'obiettivo è di")
        st.write("Per iniziare connettiti al database premendo sul pulsante qui sul lato :violet[sinistro]")

    if check_connection():
        

        with col2:
            st.image("images/gym.gif")


        with st.expander("Numero di lezioni per slot di tempo", True):
            query = "SELECT OraInizio as 'Ora di Inizio', COUNT(*) AS 'Numero di Lezioni' FROM Programma GROUP BY OraInizio"
            orari = execute_query(st.session_state["connection"], query)
            df_orari = pd.DataFrame(orari)
            st.bar_chart(df_orari, x="Ora di Inizio", y="Numero di Lezioni", use_container_width=True)

        with st.expander("Numero di lezioni programmate per giorno della settimana", False):
            query = "SELECT Giorno, COUNT(*) as 'Numero di Lezioni' FROM Programma group by Giorno"
            data = execute_query(st.session_state["connection"], query)
            df_giorno = pd.DataFrame(data)
            if (df_giorno.empty):
                st.warning("Nessun dato disponibile.")
            else:
                st.area_chart(df_giorno, x="Giorno", y="Numero di Lezioni")


    