import streamlit as st
from openai import OpenAI
import time
import psycopg2
import os
import dotenv

def run_demo_emails():
    
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
    contexto = ("Vamos a jugar a un juego de rol. Eres empleado del hotel Virtual Plaza, te llamas Milton. Trabajas respondiendo emails de clientes, [IMPORTANT] respondes en el IDIOMA en el que el cliente te escribe. Te inventas respuestas sobre el hotel para satisfacer las demandas de los clientes. Eres agradable, educado, con un toque amistoso y muy humano. No uses frases tipo 'Me complace informarles', sé más directo. Tus respuestas son comedidas, no eres pelota. Siempre respondes en el idioma del email del cliente.  Asegúrate de que tu respuesta sea clara y concisa. Mantén los párrafos cortos y al punto para facilitar la lectura. El cuerpo de tus mensajes consiste en un saludo, agradecimiento por el mensaje del cliente, respuesta y despedida. La firma debe ser: Milton y debajo el nombre del hotel. Solo respondes a los temas que tengan relación con tu hotel, y a nada más. Tu respuesta es exclusivamente el mensaje de email que estás contestando. En el Hotel Virtual Plaza, el check-in es a partir de las 14:00 y el check-out antes de las 12:00, con posibles cargos adicionales por solicitudes fuera de horario. Admitimos mascotas entrenadas, las cuales deben estar con correa en áreas comunes y no se deben dejar solas en las habitaciones. Respetamos la privacidad de los huéspedes, manejando los datos personales según la ley. La piscina opera de 8:00 a 20:00, requiriendo supervisión adulta para niños menores de 12 años y prohibiendo alimentos y bebidas externos. En el restaurante, servimos desayuno, almuerzo y cena en horarios establecidos, con vestimenta apropiada y sin alimentos externos. Pedimos a los huéspedes limitar el ruido entre las 22:00 y las 8:00 y no fumar en áreas cerradas, designando áreas específicas para fumadores. El spa está disponible para mayores de 16 años, con reserva previa de tratamientos. Ofrecemos estacionamiento gratuito, sujeto a disponibilidad. Para eventos y convenciones, es necesario coordinar con nuestro Departamento de Eventos y seguir las normas establecidas, incluyendo la aprobación de decoraciones.")
    
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
        # Dividir la respuesta en segmentos basados en saltos de línea
        segmentos = respuesta.split('\n')
        
        for segmento in segmentos:
            # Dividir cada segmento en palabras para simular la escritura
            palabras = segmento.split()
            
            # Itera sobre cada palabra, agregando una a una al generador
            for palabra in palabras:
                # Agrega un espacio para simular el tipeo y envía cada palabra como un 'yield'
                yield palabra + " "
                # Pausa entre palabras para simular el efecto de tipeo
                time.sleep(0.05)
            
            # Agrega un salto de línea al final de cada segmento
            yield "\n\n"
            
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
    
    st.title('¡Pruébalo! ✨')
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 2]) 
    
    with col1:
        # Campo de texto para escribir la reseña
        # Texto por defecto para el área de texto de la reseña
        texto_defecto = ("")
        
        # Campo de texto para escribir la reseña, con el texto por defecto incluido
        review_text = st.text_area('Escribe un email al Hotel Virtual Plaza:', value=texto_defecto, height=225)
        publicar = st.button('Enviar 📨 ')
    
    
    if publicar:
        # Añade el mensaje del usuario a la sesión para mantener el historial
        st.session_state.messages.append({"role": "user", "content": review_text})
        
        with col1:
            st.markdown('<div style="height: 25px;"></div>', unsafe_allow_html=True)
            st.info("Email enviado. Milton está leyendo y redactando la respuesta 🤵")
            
        with col2:
            # Muestra inmediatamente el mensaje del usuario
            #with st.chat_message("user"):
            #    st.markdown(review_text)
    
            # Obtiene la respuesta del asistente
            respuesta = gpt_model(contexto, review_text, model="gpt-4-turbo")
            
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