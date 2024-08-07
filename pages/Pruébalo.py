import streamlit as st
from demo_emails import run_demo_emails

st.set_page_config(page_title="Milton", page_icon="🛎️", layout="wide", initial_sidebar_state="collapsed" )
st.logo(image='milton_logo.png', link='https://milton.gluon.es/')

col1, col2, col3 = st.columns(3)
with col2:
    st.image("milton.svg", width=100)

with col3:
    st.page_link("pages/Acceso_clientes.py", label="Acceso clientes", icon="👤")

run_demo_emails()

st.divider()
st.page_link("Milton.py", label="Volver a la página principal", icon="🛎️")