import streamlit as st

col1, col2 = st.columns([1.3, 2])

with col1:
    st.image("milton_logo.png", width=220)
    
with col2: 
    st.write("")
    st.write("")
    st.write("")
    st.markdown("<h1 style='text-align: left; color: #172427; font-size: 70px;'>Milton</h1>", unsafe_allow_html=True)

# Sección donde se muestran los emails
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Email original")
    original_email = st.text_area("")

with col2:
    st.markdown("#### Respuesta generada")
    generated_response = st.text_area("Escribe aquí la respuesta generada")