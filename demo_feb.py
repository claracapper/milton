import streamlit as st
from openai import OpenAI
import time
import psycopg2
import os
import dotenv

st.set_page_config(page_title='Milton', page_icon="🛎️", layout="wide")

if 'messages' not in st.session_state:
    st.session_state.messages = []
    
# =============================================================================
# Cargar variables de entorno
# =============================================================================
dotenv.load_dotenv()
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = 'milton_project'

# =============================================================================
# FUNCTIONS
# =============================================================================
contexto = ("Eres un empleado del hotel Virtual Plaza y trabajas como atención al cliente respondiendo reseñas de clientes."
            "Tus respuestas a reseñas de clientes son cortas, concisas. Eres amable y positivo. Contesta en modo chat."
            "Solo respondes a los temas que tengan relación con tu hotel, y a nada más. Si la reseña no tiene que ver con el hotel, limitate a responder algo como: Esto no es una reseña del/ hotel Virtual Plaza.")

def gpt_model(contexto,
            mensaje,
            model,
            temperature=0):

    client = OpenAI(api_key="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")  

    context = contexto  + mensaje  
    response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": context}],
            temperature=temperature,
            #max_tokens=100
        )
    
    respuesta = response.choices[0].message.content

    return respuesta

def generar_respuesta_simulada(respuesta):
    # Divide la respuesta en palabras para simular la escritura
    palabras = respuesta.split()
    
    # Itera sobre cada palabra, agregando una a una al generador
    for palabra in palabras:
        # Agrega un espacio para simular el tipeo y envía cada palabra como un 'yield'
        yield palabra + " "
        # Pausa entre palabras para simular el efecto de tipeo
        time.sleep(0.05)
        
# =============================================================================
# connect_database
# =============================================================================
def connect_database(host, port, user, password, database):
    """
    Establece una conexión con una base de datos PostgreSQL utilizando los parámetros proporcionados.
    
    Args:
        host (str): Host donde se encuentra la base de datos.
        port (int): Puerto para la conexión.
        user (str): Usuario para acceder a la base de datos.
        password (str): Contraseña para el usuario.
        database (str): Nombre de la base de datos a conectar.
    
    Returns:
        tuple: Una tupla conteniendo dos elementos. El primero es el objeto de conexión a la base de datos,
               y el segundo es un cursor para realizar operaciones en la base de datos.
               Retorna None, None si la conexión falla.
    """
    # Establecer conexión
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        print("Conexión exitosa a la base de datos.")
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None, None

    # Crear cursor
    cursor = conn.cursor()

    return conn, cursor

# =============================================================================
# insert_data_db
# =============================================================================
def insert_data_db(conn, cursor, query, data):
    """
    Inserta datos en la base de datos utilizando una consulta SQL y los datos proporcionados.
    
    Args:
        conn: Objeto de conexión a la base de datos.
        cursor: Cursor de la base de datos.
        query (str): Consulta SQL para insertar datos.
        data (tuple): Datos que se insertarán en la base de datos.
    
    Returns:
        bool: True si la inserción es exitosa, False en caso contrario.
    """
    try:
        # Ejecutar la consulta
        cursor.execute(query, data)
        conn.commit()
        print("Datos insertados correctamente.")
    except Exception as e:
        conn.rollback()
        print(f"Error al insertar datos: {e}")
        return False
    finally:
        # Cerrar conexión
        cursor.close()
        conn.close()

    return True

# =============================================================================
# save_review
# =============================================================================
def save_review(cursor, conn, review, answer):
    query = """
            INSERT INTO general_1.reviews (review, answer)
            VALUES (%s, %s)
            """
    data = (review, answer)
    cursor.execute(query, data)
    conn.commit()
    
# =============================================================================
# MAIN
# =============================================================================
conn, cursor = connect_database(host, port, user, password, database)

# Nombre del usuario
st.header('👨‍🦱 Manuel')

col1, col2 = st.columns([1.5, 2]) 

with col1:
    # Campo de texto para escribir la reseña
    st.subheader('Tu reseña')
    # Texto por defecto para el área de texto de la reseña
    texto_defecto = ("Es un hotel cómodo por la entrada desde la autovía evitando el tráfico del centro. "
                     "Cerca de casi todo con un paseo de entre 15 y 20 minutos, con líneas de bus urbano muy cerca. "
                     "Habitaciones limpias, camas cómodas, bien de espacio. El baño completo, ducha en muy buen estado. "
                     "Luz del baño algo débil. El desayuno buffet normal, aceptable, tortillas al momento muy ricas. "
                     "Variedad de panes. Faltaría algo más de fiambre que no sea de cerdo, había pechuga de pavo pero no tenía buen sabor.")
    
    # Campo de texto para escribir la reseña, con el texto por defecto incluido
    review_text = st.text_area('Comparte detalles de tu experiencia en este lugar:', value=texto_defecto, height=225)
    publicar = st.button('Publicar')


if publicar:
    # Añade el mensaje del usuario a la sesión para mantener el historial
    st.session_state.messages.append({"role": "user", "content": review_text})
    
    with col1:
        st.success("Reseña publicada con éxito")
    
    with col2:
        # Muestra inmediatamente el mensaje del usuario
        with st.chat_message("user"):
            st.markdown(review_text)
        
        # Obtiene la respuesta del asistente
        respuesta = gpt_model(contexto, review_text, model="gpt-4-1106-preview")
        
        # Reemplaza el contenedor "Escribiendo..." con la respuesta del asistente
        # utilizando st.write_stream para simular la escritura de la respuesta
        with st.chat_message("assistant"):
            # Aquí se utiliza el generador para simular la escritura
            st.write_stream(generar_respuesta_simulada(respuesta))
    
        # Añade la respuesta del asistente al estado de la sesión
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
        # Guarda la reseña y la respuesta a la base de datos
        save_review(cursor, conn, review_text, respuesta)

# Cerrar la conexión a la base de datos al final del script
cursor.close()
conn.close()