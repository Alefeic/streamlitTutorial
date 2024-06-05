import streamlit as st
from utils.utils import *
import pandas as pd

#ogni tab ha una funzione separata


def create_tab_prodotti(tab_prodotti):
    col1, col2, col3 = tab_prodotti.columns(3)
    payment_info = execute_query(st.session_state["connection"], "SELECT SUM(amount) as 'TotalAmount', MAX(amount) as 'MaxAmount', AVG(amount) as 'AvgAmount' FROM `payments`;")
    payment_info_dict = [dict(zip(payment_info.keys(), result)) for result in payment_info]
    print(payment_info_dict)
    col1.metric("Importo totale", f"$ {compact_format(payment_info_dict[0]['TotalAmount'])}")
    col2.metric("Importo massimo", f"$ {compact_format(payment_info_dict[0]['MaxAmount'])}")
    col3.metric("Importo medio", f"$ {compact_format(payment_info_dict[0]['AvgAmount'])}")

    with tab_prodotti.expander("Panoramica prodotti", True):
        query = "SELECT productCode as 'code', productName AS 'name', quantityInStock AS 'quantity', buyPrice AS 'price', MSRP FROM products"
        prod_col1, prod_col2 = st.columns([3, 3])
        sort_param = prod_col1.radio("Ordina per: ", ['code', 'name', 'quantity', 'price'])
        sort_choice = prod_col2.selectbox("Ordine: ", ['crescente', 'decrescente'])
        sort_dict={'crescente': 'ASC', 'decrescente': 'DESC'}
        query += f" ORDER BY {sort_param} {sort_dict[sort_choice]}"
        prodotti = execute_query(st.session_state["connection"], query)
        df_prodotti = pd.DataFrame(prodotti)
        st.dataframe(df_prodotti, use_container_width=True)

    with tab_prodotti.expander("Panoramica pagamenti", True):
        query = "SELECT MIN(paymentDate), MAX(paymentDate) from payments"
        data = execute_query(st.session_state["connection"], query)
        min_max = [dict(zip(data.keys(), result)) for result in data]
        min_value = min_max[0]['MIN(paymentDate)']
        max_value = min_max[0]['MAX(paymentDate)']

        data_range = st.date_input("Selezionare il range di date:", value=(min_value, max_value), min_value=min_value, max_value=max_value)

        query = f"SELECT paymentDate, SUM(amount) as 'Total Amount' from payments where paymentDate >'{data_range[0]}' and paymentDate <'{data_range[1]}' group by paymentDate"
        paymentDate = execute_query(st.session_state["connection"], query)

        df_paymentDate = pd.DataFrame(paymentDate)
        if (df_paymentDate.empty):
            st.warning("Nessun dato disponibile.")
        else:
            df_paymentDate['Total Amount'] = df_paymentDate['Total Amount'].astype(float)
            df_paymentDate['paymentDate'] = pd.to_datetime(df_paymentDate['paymentDate'])

            st.line_chart(df_paymentDate, x="paymentDate", y="Total Amount")


#def create_tab_staff(tab_staff):
    #al minuto 1:41:00


if __name__ == "__main__":
    st.title("📈 Analisi")

    #creazione dei tab distinti
    tab_prodotti,tab_staff,tab_clienti=st.tabs(["Prodotti","Staff","Clienti"])
    if check_connection():
        create_tab_prodotti(tab_prodotti)