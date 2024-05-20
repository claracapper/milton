import streamlit as st
import pandas as pd
import psycopg2
import warnings
from config import db_config
import functions as f

warnings.filterwarnings('ignore')

# Mapeo de códigos a hotelID
code_to_hotel = {
    '1': '1',
    '1011': '11',
    '1012': '12',
    '2013': '13',
    '3014': '14'
}

# Consulta SQL para obtener emails y respuestas generadas
email_query = """
SELECT
    email_body,
    generated_response,
    received_date,
    answered_date
FROM
    general_1.emails
WHERE
    hotel_id = %s
ORDER BY id DESC; 
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

def format_date(date):
    if pd.isna(date):
        return "Fecha no disponible"
    else:
        return pd.to_datetime(date).strftime('%d-%m-%Y %H:%M')

st.set_page_config(
    page_title="Milton",
    page_icon="🤵",
    layout="wide" )

# CSS
st.markdown(
    """
    <style>
    .email_body {
        height: 300px;
        overflow-y: auto;
        background-color: #FDFDFD;
        padding: 20px;
        border-radius: 20px;
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
        border-radius: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("<h1 style='text-align: left; color: #172427; font-size: 40px;'>Milton</h1>", unsafe_allow_html=True)
    
# Página de acceso para el código
code_input = st.sidebar.text_input("Código de acceso", '')

# Verificar el código y mostrar la información correspondiente
if code_input:
    if code_input in code_to_hotel:
        hotel_id = code_to_hotel[code_input]
        hotel_name = f.get_hotel_name(db_config, hotel_id)
        st.title(hotel_name)
        st.divider()
        df = query_database(db_config, email_query, hotel_id)

        if not df.empty:
            total_emails = len(df)
            for index, row in df.iterrows():
                email_number = total_emails - index
                col1, col2 = st.columns(2)
                with col1:
                    received_date = format_date(row["received_date"])
                    st.markdown(f"**🦰 Email {email_number} ({received_date})**")
                    email_body = row["email_body"]
                    st.markdown(f'<div class="email_body">{email_body}</div>', unsafe_allow_html=True)
        
                with col2:
                    answered_date = format_date(row["answered_date"])
                    st.markdown(f"**🤵🏻‍♂️ Respuesta {email_number} ({answered_date})**")
                    generated_response = row["generated_response"]
                    st.markdown(f'<div class="generated_response">{generated_response}</div>', unsafe_allow_html=True)
                st.divider()
        else:
            st.warning("No hay correos electrónicos para el hotel especificado.")
    else:
        st.error("Código de acceso inválido. Por favor, intente de nuevo.")