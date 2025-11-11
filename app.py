import streamlit as st
from groq import Groq
import os

# ---------------- CONFIGURACIÓN GENERAL ----------------
st.set_page_config(page_title="ANIMA - Apoyo Emocional UDD", layout="centered", page_icon="💙")

# --- ESTILOS PERSONALIZADOS (fondo crema + azul pastel) ---
st.markdown("""
<style>

/* Fondo principal */
[data-testid="stAppViewContainer"] {
    background-color: #FFF8F0;
}

/* Barra lateral */
[data-testid="stSidebar"] {
    background-color: #D7E8F7;
    color: #3A3A3A;
    border: none;
}

/* Botones */
.stButton>button {
    background-color: #B8E0D2;
    color: #3A3A3A;
    border: none;
    border-radius: 10px;
    font-weight: 600;
}
.stButton>button:hover {
    background-color: #A3D9C9;
}

/* Entradas de texto */
.stTextInput>div>div>input, .stTextArea>div>textarea {
    background-color: #FFFFFF;
    border: 1px solid #EBDDC9;
    color: #3A3A3A;
    border-radius: 10px;
}

/* --- CHAT --- */
[data-testid="stChatInput"] {
    background-color: #FFF8F0 !important; /* crema */
    border-top: 1px solid #EBDDC9 !important;
}

/* Caja de texto donde se escribe (parte negra antes) */
[data-baseweb="textarea"] textarea {
    background-color: #FFFFFF !important;
    color: #3A3A3A !important;
    border: 1px solid #EAD8C5 !important;
    border-radius: 20px !important;
    padding: 10px 16px !important;
}

/* Botón de enviar (flecha) */
[data-testid="stChatInputSubmitButton"] {
    background-color: #B8E0D2 !important;
    border-radius: 50% !important;
}
[data-testid="stChatInputSubmitButton"]:hover {
    background-color: #A3D9C9 !important;
}

/* Mensajes del usuario y asistente */
[data-testid="stChatMessageUser"] {
    background-color: #FFF2E1 !important; /* crema pastel */
    color: #3A3A3A !important;
    border-radius: 12px;
}
[data-testid="stChatMessageAssistant"] {
    background-color: #E9F7F2 !important; /* verde menta suave */
    color: #3A3A3A !important;
    border-radius: 12px;
}

/* Enlaces */
a {
    color: #6AAED6 !important;
}
a:hover {
    text-decoration: underline;
}

/* Tipografía */
h1, h2, h3, h4, h5 {
    color: #2B2B2B;
    font-family: "Poppins", sans-serif;
}
p, span, div, label {
    color: #3A3A3A !important;
    font-family: "Poppins", sans-serif;
}

/* Scroll suave */
::-webkit-scrollbar-thumb {
    background-color: #EBDDC9;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)





# --- Inicializar cliente Groq ---
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- FUNCIÓN PARA OBTENER RESPUESTA DE LA IA ---
def obtener_respuesta(mensaje):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Eres ANIMA, una IA empática y amable de apoyo emocional para estudiantes de la Universidad del Desarrollo (UDD)."},
                {"role": "user", "content": mensaje}
            ]
        )
        texto = response.choices[0].message.content

        # Sugerir ayuda psicológica si detecta emociones negativas
        if any(p in mensaje.lower() for p in ["ansiosa", "estresada", "triste", "deprimida", "mal", "colapsada"]):
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
            st.info("💙 Estás en un punto intermedio. ANIMA te acompañará para mejorar tu bienestar.")
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

# --- BOTÓN MENÚ HAMBURGUESA FLOTANTE ---
if "mostrar_menu" not in st.session_state:
    st.session_state.mostrar_menu = False

def toggle_menu():
    st.session_state.mostrar_menu = not st.session_state.mostrar_menu

if st.button("☰", key="menu_btn"):
    toggle_menu()

if st.session_state.mostrar_menu:
    mostrar_menu()

# --- INICIO DE SESIÓN ---
if "logged_in" not in st.session_state:
    st.markdown("<h2 style='text-align:center;'>💙 ANIMA - Apoyo Emocional UDD</h2>", unsafe_allow_html=True)
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
st.title("💬 Chat de apoyo emocional ANIMA")

# Mostrar encuesta si aún no se ha respondido
if "encuesta_respondida" not in st.session_state or not st.session_state.encuesta_respondida:
    encuesta_bienestar()
    st.stop()

# Saludo inicial personalizado
if "saludo_inicial" not in st.session_state:
    nombre_usuario = st.session_state.usuario.split('@')[0].capitalize()
    st.session_state.saludo_inicial = f"Hola {nombre_usuario} 👋, soy **ANIMA**, tu asistente emocional UDD. ¿Cómo te sientes hoy?"
    st.session_state.historial.append({"user": "Inicio de conversación", "bot": st.session_state.saludo_inicial})

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






