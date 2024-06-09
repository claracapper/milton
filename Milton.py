import streamlit as st

st.set_page_config(page_title="Milton", page_icon="🤵", layout="wide", initial_sidebar_state="collapsed" )
st.logo(image='milton_logo.png', link='https://milton.gluon.es/')

st.title("Milton")
st.write("")

col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/Registro.py", label="Regístrate", icon="✍️")
with col2:
    st.page_link("pages/Acceso_clientes.py", label="Acceso clientes", icon="👤")

st.divider()
st.write("Aquí puedes encontrar información sobre cómo usar esta aplicación.")
