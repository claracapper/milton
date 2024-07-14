import streamlit as st

st.set_page_config(page_title="Milton", page_icon="🤵", layout="wide", initial_sidebar_state="collapsed" )
st.logo(image='milton_logo.png', link='https://milton.gluon.es/')

st.title("Milton")
st.write("")

video_file = open('milton1080hd.mp4', 'rb')
video_bytes = video_file.read()
st.video(video_bytes)

st.divider()

st.page_link("pages/Acceso_clientes.py", label="Acceso clientes", icon="👤")