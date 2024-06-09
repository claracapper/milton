import streamlit as st

st.set_page_config(page_title="Milton", page_icon="🤵", layout="wide", initial_sidebar_state="collapsed" )
st.logo(image='milton_logo.png')

def app():
    st.title("Solicitar Acceso")
    st.write("Rellene el siguiente formulario para solicitar acceso a la aplicación.")
    with st.form("request_access"):
        name = st.text_input("Nombre")
        email = st.text_input("Email")
        submit_button = st.form_submit_button("Enviar Solicitud")
        if submit_button:
            st.success("Tu solicitud ha sido enviada.")

if __name__ == "__main__":
    app()
    st.divider()
    st.page_link("Milton.py", label="Volver a la página principal", icon="🤵")
