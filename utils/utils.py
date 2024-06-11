import streamlit as st
from sqlalchemy import create_engine,text

"""Raccoglie le principali funzioni condivise dalle varie pagine"""
#connessione al db
def connect_db(dialect, username, password, host, dbname):
    try:
        engine=create_engine(f'{dialect}://{username}:{password}@{host}/{dbname}')
        conn = engine.connect()
        return conn
    except:
        return False
    

def check_connection():
    if "connection" not in st.session_state.keys():
        st.session_state["connection"] = False

    if st.sidebar.button("Connetti al db"):
        myconnection = connect_db("mysql+pymysql", "root", "mypassword", "localhost", "palestra")
        if myconnection is not False:
            st.session_state["connection"] = myconnection
        else:
            st.session_state["connection"] = False
            st.sidebar.error("Errore connessione")

    if st.session_state["connection"]:
        st.sidebar.success("Connesso al db")
        return True
    

def execute_query(conn, query):
    return conn.execute(text(query))


def compact_format(num):
    num = float(num)
    if (abs(num) >= 1e9):
        return "{:.2f}B".format(num / 1e9)
    elif abs(num) >= 1e6:
        return "{:.2f}M".format(num / 1e6)
    elif abs(num) >= 1e3:
        return "{:.2f}K".format(num / 1e3)
    else:
        return "{:.0f}".format(num)