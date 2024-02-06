import streamlit as st
from openai import OpenAI
import time

st.set_page_config(page_title='Milton')

if 'messages' not in st.session_state:
    st.session_state.messages = []
# =============================================================================
# FUNCTIONS
# =============================================================================
contexto = "Eres un empleado del hotel Virtual Plaza y trabajas como atención al cliente respondiendo reseñas de clientes. Tus respuestas a reseñas de clientes son cortas, concisas. Eres amable y positivo."
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

# =============================================================================
# MAIN
# =============================================================================
st.title('Reseñas')
st.divider()

# Nombre del usuario
st.header('👨‍🦱 Manuel')

# Campo de texto para escribir la reseña
st.subheader('Tu reseña')
review_text = st.text_area('Comparte detalles de tu experiencia en este lugar:')

if st.button('Publicar'):
    st.divider()
    # Añade el mensaje del usuario a la sesión para mantener el historial
    st.session_state.messages.append({"role": "user", "content": review_text})

    # Muestra inmediatamente el mensaje del usuario
    with st.chat_message("user"):
        st.markdown(review_text)
    
    # Prepara un contenedor para el mensaje "Escribiendo..." que pueda ser actualizado
    writing_placeholder = st.empty()
    
    with writing_placeholder.container():
        with st.chat_message("assistant"):
            st.text("Leyendo la reseña...")

    # Simula un retardo para representar el tiempo de procesamiento
    time.sleep(0.2)  # Ajusta este tiempo según sea necesario

    # Obtiene la respuesta del asistente
    respuesta = gpt_model(contexto, review_text, model="gpt-4-1106-preview")
    
    # Reemplaza el mensaje "Escribiendo..." con la respuesta del asistente
    writing_placeholder.empty()  # Elimina el mensaje "Escribiendo..."
    with st.chat_message("assistant"):
        st.markdown(respuesta)

    # Añade la respuesta del asistente al estado de la sesión
    st.session_state.messages.append({"role": "assistant", "content": respuesta})
