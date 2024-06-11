import streamlit as st
from utils.utils import *
import pandas as pd

#ogni tab ha una funzione separata


def create_tab_prodotti(tab_prodotti):
    # col1, col2, col3 = tab_prodotti.columns(3)
    # payment_info = execute_query(st.session_state["connection"], "SELECT SUM(amount) as 'TotalAmount', MAX(amount) as 'MaxAmount', AVG(amount) as 'AvgAmount' FROM `payments`;")
    # payment_info_dict = [dict(zip(payment_info.keys(), result)) for result in payment_info]
    # print(payment_info_dict)
    # col1.metric("Importo totale", f"$ {compact_format(payment_info_dict[0]['TotalAmount'])}")
    # col2.metric("Importo massimo", f"$ {compact_format(payment_info_dict[0]['MaxAmount'])}")
    # col3.metric("Importo medio", f"$ {compact_format(payment_info_dict[0]['AvgAmount'])}")

    with tab_prodotti.expander("Numero di lezioni per slot di tempo", True):
        query = "SELECT OraInizio as 'Ora di Inizio', COUNT(*) AS 'Numero di Lezioni' FROM Programma GROUP BY OraInizio"
        orari = execute_query(st.session_state["connection"], query)
        df_orari = pd.DataFrame(orari)
        st.bar_chart(df_orari, x="Ora di Inizio", y="Numero di Lezioni", use_container_width=True)

    with tab_prodotti.expander("Numero di lezioni programmate per giorno della settimana", False):
        query = "SELECT Giorno, COUNT(*) as 'Numero di Lezioni' FROM Programma group by Giorno"
        data = execute_query(st.session_state["connection"], query)
        df_giorno = pd.DataFrame(data)
        if (df_giorno.empty):
            st.warning("Nessun dato disponibile.")
        else:
            st.area_chart(df_giorno, x="Giorno", y="Numero di Lezioni")


def create_tab_staff(tab_staff):
    #si può usare mappings() e first() (aspettandoci una sola tupla) per ottenere i dati desiderati dal risultato della query
    #trovare nome e cognome del presidente e del VP sales
    president_query= "select lastName, firstName from employees where jobTitle='President'"
    president = execute_query(st.session_state["connection"], president_query).mappings().first()
    vp_sales_query = "select lastName, firstName from employees where jobTitle='VP Sales'"
    vp_sales = execute_query(st.session_state["connection"], vp_sales_query).mappings().first()

    col1, col2, col3 = tab_staff.columns(3)
    col1.markdown(f"#### :blue[PRESIDENT:] {president['firstName']} {president['lastName']}")
    col3.markdown(f"#### :orange[VP SALES:] {vp_sales['firstName']} {vp_sales['lastName']}")

    #ordine non presente nel bar chart
    staff_query = "select jobTitle, COUNT(*) as numDipendenti from employees group by jobTitle order by 'numDipendenti' DESC;"
    staff = execute_query(st.session_state["connection"], staff_query)
    df_staff = pd.DataFrame(staff)
    tab_staff.markdown("### Componenti Staff")
    #specificare quali colonne del dataframe devono essere l'asse x o y
    tab_staff.bar_chart(df_staff, x='jobTitle', y='numDipendenti', use_container_width=True)


def create_tab_clienti(tab_clienti):
    col1, col2 = tab_clienti.columns(2)
    query = "select COUNT(*) as 'numeroClienti', country from customers group by country order by 'numeroClienti' DESC;"
    result = execute_query(st.session_state["connection"], query)
    df_clienti = pd.DataFrame(result)
    col1.subheader("Distribuzione clienti nel mondo")
    #impostare un'altezza uguale per i vari elementi può rendere il risultato più curato
    col1.dataframe(df_clienti, use_container_width=True, height=350)

    query = "Select customername, state, creditLimit from customers where country = 'USA' and creditLimit > 100000 order by creditLimit DESC;"
    result = execute_query(st.session_state["connection"], query)
    df = pd.DataFrame(result)
    col2.subheader("Clienti con maggior *credit limit* negli USA")
    col2.dataframe(df, use_container_width=True, height=350)


if __name__ == "__main__":
    st.title("📈 Analisi")

    #creazione dei tab distinti
    tab_prodotti,tab_staff,tab_clienti=st.tabs(["Prodotti","Staff","Clienti"])
    if check_connection():
        create_tab_prodotti(tab_prodotti)
        create_tab_staff(tab_staff)
        create_tab_clienti(tab_clienti)