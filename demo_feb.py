import streamlit as st
from openai import OpenAI
import time

st.set_page_config(page_title='Milton', layout="wide")

if 'messages' not in st.session_state:
    st.session_state.messages = []
# =============================================================================
# FUNCTIONS
# =============================================================================
contexto = ("Eres un empleado del hotel Virtual Plaza y trabajas como atención al cliente respondiendo reseñas de clientes."
            "Tus respuestas a reseñas de clientes son cortas, concisas. Eres amable y positivo. Contesta en modo chat."
            "Solo respondes a los temas que tengan relación con tu hotel, y a nada más. Si la reseña no tiene que ver con el hotel, limitate a responder algo como: Esto no es una reseña del hotel Virtual Plaza.")

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
# MAIN
# =============================================================================
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
                     "Variedad de panes. Faltaría algo más de fiambre que no sea de cerdo, hubo pechuga de pavo pero no tenía buen sabor.")
    
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