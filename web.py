import streamlit as st
import pandas as pd
import psycopg2
import warnings

warnings.filterwarnings('ignore')

# Configuración de la base de datos
db_config = {
    "host": "135.125.107.175",
    "port": "5432",
    "user": "admin_miguel",
    "password": "@Neurona12",
    "database": "milton_project",
    "schema": "general_1"
}

# Consulta SQL para obtener emails y respuestas generadas
email_query = """
SELECT
    email_body,
    generated_response
FROM
    general_1.emails
WHERE
    hotel_id = %s;
"""

def query_database(config, query, hotel_id):
    conn = psycopg2.connect(
        host=config["host"],
        port=config["port"],
        user=config["user"],
        password=config["password"],
        dbname=config["database"]
    )

    # Ejecutar la consulta con parámetros para prevenir inyección SQL
    df = pd.read_sql(query, conn, params=(hotel_id,))

    conn.close()
    return df

st.set_page_config(page_title="Milton", layout="wide", page_icon="🤵🏻‍♂️")

# CSS
st.markdown(
    """
    <style>
    .email_body {
        height: 300px;
        overflow-y: auto;
        background-color: #FDFDFD;
        padding: 20px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .generated_response {
        height: 300px;
        overflow-y: auto;
        background-color: #F9FAF9;
        padding: 20px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


col1, col2 = st.columns([1, 3.5])

with col1:
    st.image("milton_logo.png", width=120)
    
with col2: 
    st.text("")
    st.markdown("<h1 style='text-align: left; color: #172427; font-size: 40px;'>Milton</h1>", unsafe_allow_html=True)

st.divider()

hotel_id = 1

if hotel_id:
    df = query_database(db_config, email_query, hotel_id)

    if not df.empty:
        # Sección donde se muestran los emails
        for index, row in df.iterrows():
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**🦰 Email {}**".format(index + 1))
                email_body = row["email_body"]
                st.markdown(f'<div class="email_body">{email_body}</div>', unsafe_allow_html=True)

            with col2:
                st.markdown("**🤵🏻‍♂️ Respuesta {}**".format(index + 1))
                generated_response = row["generated_response"]
                st.markdown(f'<div class="generated_response">{generated_response}</div>', unsafe_allow_html=True)
            st.divider()
    else:
        st.warning("No hay correos electrónicos para mostrar para el hotel ID especificado.")
else:
    st.warning("Por favor, ingrese un ID de hotel para buscar correos electrónicos.")
