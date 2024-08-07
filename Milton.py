import streamlit as st
from demo_emails import run_demo_emails

st.set_page_config(page_title="Milton", page_icon="🛎️", layout="wide", initial_sidebar_state="collapsed" )
st.logo(image='milton_logo.png', link='https://milton.gluon.es/')

st.image("milton.svg", width=100)

st.markdown(f'<h1 style="color: #FF8C00;">Milton</h1>', unsafe_allow_html=True)
st.caption("Milton es tu recepcionista digital a medida")
st.write("")

# Botones acceso y demo
col1, col2, col3 = st.columns([1, 0.5, 1])
with col1:
    st.page_link("pages/Pruébalo.py", label="¡Pruébalo!", icon="✨")
with col2:
    st.page_link("pages/Acceso_clientes.py", label="Acceso clientes", icon="👤")
st.divider()

# Texto intro
col1, col2, col3 = st.columns([3, 0.7, 3])
with col1:
    st.header("🤵 Una IA que conoce tu hotel al detalle")
    st.write("Milton aprende todo lo necesario sobre horarios, normas, características, capacidad, etc. y contesta a los clientes de forma precisa y pertinente.")
with col3:
    st.header("🛎️ 24 horas de asistencia. En cualquier idioma.")
    st.write("Milton entiende y responde en cualquier idioma, de forma inmediata, 24h al día. No permitas que los correos de tus clientes se acumulen en la bandeja de entrada.")

# Botón de contacto
st.markdown("""
<a href="https://milton.gluon.es/#Contacto" target="_blank">
    <button style="background-color: #FF8C00; color: white; border: none; padding: 10px 20px; font-size: 16px; cursor: pointer; border-radius: 5px; margin-top: 20px;">
        Contactar →
    </button>
</a>
""", unsafe_allow_html=True)
st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)

# Video
video_file = open('milton1080hd.mp4', 'rb')
video_bytes = video_file.read()
st.video(video_bytes)
st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)

# Pruebalo
run_demo_emails()
st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)

# FAQ
col1, col2, col3 = st.columns([3, 0.7, 3])
with col1:
    st.image("milton_faq.png")
with col3:
    st.title("¿Cómo funciona Milton?")
    st.write("Configura un buzón para Milton o reenvíale los correos que desees. Milton comprende la conversación y elabora una respuesta automáticamente de acuerdo con las normas que le has proporcionado, o deriva el correo al departamento pertinente cuando sea necesario.")
    with st.expander("¿Qué ventajas tiene?"):
        st.write("""
        Gracias a Milton, tu personal tendrá más tiempo para ofrecer atención a tus clientes de forma personalizada y cara a cara, ahorrando mucho tiempo cada día al no tener que atender múltiples correos de escaso valor añadido que inundan la bandeja de entrada.
        """)
    with st.expander("¿A qué sabe contestar?"):
        st.write("""
        Puedes indicar a Milton aquellos correos que debe responder automáticamente, o a quién redirigir aquellos que necesitan tu atención directa. Considera a Milton como uno más de tu equipo e indícale lo que esperas de él.
        """)
    with st.expander("¿Cómo aprende lo que debe decir?"):
        st.write("""
        Puedes entrenar a Milton con la documentación que ya tienes disponible sobre el funcionamiento de tu Hotel o que utilices para formar al personal. Además, Milton puede aprender de preguntas y respuestas antiguas o de las correcciones que hagas en sus respuestas propuestas. ¡Milton mejora cada día!
        """)

st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1.8, 0.2, 3])
with col1:
    st.header("Milton está listo para ayudarte desde hoy mismo.")
    st.caption("Solicita ya tu demo gratuita y comprueba lo que Milton aporta a tu equipo.")
    # Botón de contacto
    st.markdown("""
    <a href="https://milton.gluon.es/#Contacto" target="_blank">
        <button style="background-color: #FF8C00; color: white; border: none; padding: 10px 20px; font-size: 16px; cursor: pointer; border-radius: 5px; margin-top: 20px;">
            Contactar →
        </button>
    </a>
    """, unsafe_allow_html=True)
    st.text("")
with col3:
    st.image("milton_example.png")
    
# Imagen 
st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)
st.image("milton_reto.png")
st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)