import streamlit as st
from groq import Groq
import os

# ---------------- CONFIGURACIÓN GENERAL ----------------
st.set_page_config(page_title="ANIMA - Apoyo Emocional UDD", layout="centered", page_icon="💙")

# --- Estilos Pasteles Personalizados ---
st.markdown("""
<style>
/* Fondo general */
[data-testid="stAppViewContainer"] {
    background-color: #F9FAFB;
    background-image: linear-gradient(180deg, #FDFBFB 0%, #EBEDEE 100%);
}

/* Panel lateral */
[data-testid="stSidebar"] {
    background-color: #F3E5F5;
}

/* Botones */
.stButton>button {
    background-color: #A5D8FF;
    color: #1A1A1A;
    border-radius: 10px;
    border: none;
    font-weight: bold;
    padding: 8px 20px;
}
.stButton>button:hover {
    background-color: #C8E7FF;
    color: #000;
}

/* Inputs */
.stTextInput>div>div>input, .stTextArea>div>textarea {
    background-color: #FFFFFF;
    border: 1px solid #D1C4E9;
    border-radius: 8px;
}

/* Mensajes del chat */
[data-testid="stChatMessageUser"] {
    background-color: #FFF8E1;
}
[data-testid="stChatMessageAssistant"] {
    background-color: #E1F5FE;
}

/* Texto general */
body {
    color: #3E3E3E;
}
</style>
""", unsafe_allow_html=True)

# --- Inicializar cliente Groq ---
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- FUNCIÓN PARA OBTENER RESPUESTA DE LA IA ---
def obtener_respuesta(mensaje):
    """Genera una respuesta de la IA usando Groq"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Eres ANIMA, una IA empática y amable de apoyo emocional para estudiantes de la Universidad del Desarrollo (UDD)."},
                {"role": "user", "content": mensaje}
            ]
        )
        texto = response.choices[0].message.content

        # Si detecta emociones fuertes o señales de estrés, muestra WhatsApp
        if any(palabra in mensaje.lower() for palabra in ["ansiosa", "estresada", "triste", "deprimida", "mal", "colapsada"]):
            texto += "\n\n💬 Parece que estás pasando por un momento difícil. Si necesitas apoyo inmediato, puedes escribir a nuestro equipo en [WhatsApp de Bienestar UDD](https://wa.me/56912345678)."
        return texto

    except Exception as e:
        return f"⚠️ Error al conectar con la IA: {e}"

# --- ENCUESTA DE BIENESTAR ---
def encuesta_bienestar():
    st.subheader("💭 Antes de comenzar, responde esta breve encuesta:")
    energia = st.slider("¿Cómo evaluarías tu nivel de energía hoy?", 0, 10, 5)
    animo = st.slider("¿Qué tan animado/a te sientes?", 0, 10, 5)
    concentracion = st.slider("¿Qué tan concentrado/a te has sentido últimamente?", 0, 10, 5)
    motivacion = st.slider("¿Qué tan motivado/a te sientes con tus estudios?", 0, 10, 5)

    if st.button("Enviar respuestas"):
        promedio = (energia + animo + concentracion + motivacion) / 4
        if promedio < 4:
            st.warning("💛 Tus respuestas indican que podrías beneficiarte del apoyo de un profesional. ANIMA te recomienda contactar a psicología o psicopedagogía UDD.")
        elif promedio < 7:
            st.info("💙 Parece que estás en un punto intermedio. ANIMA te acompañará para mejorar tu bienestar.")
        else:
            st.success("🌸 ¡Excelente! Tu bienestar general parece estar bien equilibrado.")
        st.session_state.encuesta_respondida = True


# --- MENÚ LATERAL ---
def mostrar_menu():
    with st.sidebar:
        st.title("☰ Menú ANIMA")
        opcion = st.radio("Selecciona una opción:", ["Chat de ayuda", "Historial", "Grupos de apoyo", "Cerrar sesión"])

        if opcion == "Historial":
            st.subheader("🗂️ Historial de conversaciones")
            if "historial" in st.session_state and st.session_state.historial:
                for msg in st.session_state.historial:
                    st.markdown(f"**Tú:** {msg['user']}")
                    st.markdown(f"**ANIMA:** {msg['bot']}")
                    st.markdown("---")
            else:
                st.info("No hay conversaciones previas aún.")

        elif opcion == "Grupos de apoyo":
            st.subheader("👥 Grupos de ayuda entre estudiantes UDD")
            grupo = st.selectbox("Selecciona un grupo para unirte:", [
                "Bienestar y salud mental 🧠",
                "Apoyo entre compañeros 🤝",
                "Motivación y energía ☀️"
            ])
            st.markdown(f"### Foro del grupo: {grupo}")
            comentario = st.text_area("Escribe un mensaje para el grupo:")
            if st.button("Publicar"):
                st.success("✅ Tu mensaje fue publicado en el foro.")
            st.info("💬 Aquí podrás ver y responder a otros mensajes del grupo próximamente.")

        elif opcion == "Cerrar sesión":
            st.session_state.clear()
            st.rerun()

# --- INICIO DE SESIÓN ---
if "logged_in" not in st.session_state:
    st.markdown("<div class='titulo'><h2>💙 ANIMA - Apoyo Emocional UDD</h2></div>", unsafe_allow_html=True)
    st.subheader("Inicio de sesión")
    correo = st.text_input("Correo institucional UDD", placeholder="nombre.apellido@udd.cl")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar sesión"):
        if correo.endswith("@udd.cl") and len(password) > 3:
            st.session_state.logged_in = True
            st.session_state.usuario = correo
            st.session_state.historial = []
            st.session_state.encuesta_respondida = False
            st.success("Inicio de sesión exitoso 💫")
            st.rerun()
        else:
            st.error("Por favor, usa tu correo institucional UDD y una contraseña válida.")
    st.stop()

# --- INTERFAZ PRINCIPAL DEL CHAT ---
mostrar_menu()

st.title("💬 Chat de apoyo emocional ANIMA")

# Mostrar encuesta si aún no se ha respondido
if "encuesta_respondida" not in st.session_state or not st.session_state.encuesta_respondida:
    encuesta_bienestar()
    st.stop()

# Saludo inicial
st.write(f"Hola 👋 {st.session_state.usuario.split('@')[0]}, soy **ANIMA**, tu asistente emocional UDD. ¿Cómo te sientes hoy?")

# Inicializar historial
if "historial" not in st.session_state:
    st.session_state.historial = []

# Entrada del usuario
mensaje_usuario = st.chat_input("Escribe aquí tu mensaje...")

if mensaje_usuario:
    respuesta = obtener_respuesta(mensaje_usuario)
    st.session_state.historial.append({"user": mensaje_usuario, "bot": respuesta})

# Mostrar historial
for msg in st.session_state.historial:
    with st.chat_message("user"):
        st.write(msg["user"])
    with st.chat_message("assistant"):
        st.write(msg["bot"])

st.markdown("---")
st.caption("WebApp ANIMA - Apoyo Emocional UDD 💙 Desarrollado con Streamlit + Groq")





