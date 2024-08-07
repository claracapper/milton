import streamlit as st
from demo_emails import run_demo_emails

st.set_page_config(page_title="Milton", page_icon="🛎️", layout="wide", initial_sidebar_state="collapsed" )
st.logo(image='milton_logo.png', link='https://milton.gluon.es/')

run_demo_emails()
