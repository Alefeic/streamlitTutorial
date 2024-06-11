import streamlit as st
from utils.utils import *


def get_list(attributo):
    query = f"select distinct {attributo} from products"
    result = execute_query(st.session_state["connection"], query)
    result_list=[]
    for row in result.mappings():
        result_list.append(row[attributo])
    return result_list


def get_info():
    return get_list("productLine"), get_list("productScale"), get_list("productVendor")


def check_info(prod_dict):
    for value in prod_dict.values():
        if value=='':
            return False
    return True


def insert(prod_dict):
    if check_info(prod_dict):
        attributi = ", ".join(prod_dict.keys())
        valori = tuple(prod_dict.values())
        query = f"insert into products ({attributi}) values {valori};"
        #try_except per verificare che l'operazione MySQL abbia avuto successo, generare un errore altrimenti
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
    with st.form("Nuovo prodotto"):
        st.header("Aggiungi prodotto")
        categorie, scale, venditori = get_info()
        categoria = st.selectbox("Categoria", categorie)
        scala = st.selectbox("Scala", scale)
        venditore = st.selectbox("Venditore", venditori)

        code = st.text_input("Codice prodotto", placeholder = "S**_****")
        nome = st.text_input("Nome prodotto", placeholder = "Inserisci nome prodotto")
        description = st.text_input("Descrizione", placeholder = "Inserisci descrizione prodotto")
        qta = st.slider("Quantità", 0, 10000)
        price = st.number_input("Prezzo", 1.00)
        msrp = st.number_input("MSRP")

        submitted = st.form_submit_button("Salva", type = 'primary')
        product_dict = {"productCode": code, "productName": nome, "productLine": categoria, "productScale": scala, "productVendor": venditore, "productDescription": description, "quantityInStock": qta, "buyPrice": price, "MSRP": msrp}

        if submitted:
            if insert(product_dict):
                st.success("Hai inserito un nuovo prodotto")
            else:
                st.error("Errore di inserimento")


if __name__ == "__main__":
    st.title("🖊 Aggiungi")
    if check_connection():
        create_form()
