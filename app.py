import streamlit as st
import requests

st.set_page_config(page_title="ANIMA - Apoyo Emocional UDD", layout="wide")

# 🌈 --- Estilos personalizados ---
st.markdown("""
    <style>
        body {
            background-color: #FFF8E7; /* Fondo crema */
            color: #2B2B2B; /* Texto oscuro para contraste */
            font-family: 'Helvetica', sans-serif;
        }
        section[data-testid="stSidebar"] {
            background-color: #A7C7E7; /* Azul pastel */
            color: #2B2B2B;
        }
        h1, h2, h3, h4, h5 {
            color: #2B2B2B;
        }
        .stTextInput>div>div>input {
            background-color: #FFFFFF;
            color: #2B2B2B;
            border: 1px solid #D8CFC4;
            border-radius: 8px;
        }
        .stButton>button {
            background-color: #A7C7E7;
            color: #2B2B2B;
            border-radius: 10px;
            font-weight: 600;
            border: none;
            padding: 8px 16px;
        }
        .stButton>button:hover {
            background-color: #91B9D9;
            color: #1A1A1A;
        }
        .chat-bubble-user {
            background-color: #DCEBF8;
            color: #2B2B2B;
            border-radius: 12px;
            padding: 10px 15px;
            margin-bottom: 6px;
        }
        .chat-bubble-ai {
            background-color: #F9EFE3;
            color: #2B2B2B;
            border-radius: 12px;
            padding: 10px 15px;
            margin-bottom: 6px;
            border: 1px solid #E2D7C3;
        }
        .forum-card {
            background-color: #FAF3E0;
            color: #2B2B2B;
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 10px;
            border: 1px solid #E2D7C3;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        /* Fondo del contenedor principal */
        [data-testid="stAppViewContainer"] {
            background-color: #FFF8E7;
        }
    </style>
""", unsafe_allow_html=True)

# --- Estados de sesión ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "survey_done" not in st.session_state:
    st.session_state.survey_done = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "menu_visible" not in st.session_state:
    st.session_state.menu_visible = False

# --- Función para alternar menú ---
def toggle_menu():
    st.session_state.menu_visible = not st.session_state.menu_visible

# --- Botón de menú hamburguesa ---
col1, col2 = st.columns([0.1, 0.9])
with col1:
    if st.button("☰", key="menu_button"):
        toggle_menu()

# --- Menú lateral (se puede ocultar) ---
if st.session_state.menu_visible:
    with st.sidebar:
        st.header("📘 Menú")
        if st.button("🏠 Cerrar menú"):
            st.session_state.menu_visible = False
            st.experimental_rerun()
        st.markdown("### 🕓 Historial")
        st.markdown("Aquí verás tus conversaciones previas con ANIMA.")
        st.markdown("### 🤝 Grupos de apoyo UDD")
        grupos = ["Ansiedad y Estrés", "Motivación y Hábitos", "Dificultades Académicas", "Autoestima y Confianza"]
        for g in grupos:
            st.markdown(f"<div class='forum-card'><b>{g}</b><br><i>Espacio para compartir experiencias con otros estudiantes UDD.</i></div>", unsafe_allow_html=True)

# --- Inicio de sesión ---
if not st.session_state.logged_in:
    st.title("💙 Bienvenida/o a ANIMA - Apoyo Emocional UDD")
    user = st.text_input("Correo UDD:")
    password = st.text_input("Contraseña:", type="password")

    if st.button("Iniciar sesión"):
        if user.endswith("@udd.cl") and password:
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.error("Debes ingresar un correo institucional válido (terminado en @udd.cl).")
    st.stop()

# --- Encuesta inicial ---
if not st.session_state.survey_done:
    st.title("🧠 Evaluación inicial de bienestar")
    mood = st.selectbox("¿Cómo te sientes hoy?", ["Feliz", "Triste", "Ansioso/a", "Cansado/a", "Motivado/a"])
    energy = st.slider("¿Cómo evaluarías tu nivel de energía hoy?", 1, 10, 5)
    focus = st.slider("¿Qué tan concentrado/a te has sentido últimamente?", 1, 10, 5)
    sleep = st.selectbox("¿Has dormido bien esta semana?", ["Sí", "No"])
    
    if st.button("Enviar respuestas"):
        st.session_state.survey_done = True
        st.success("Gracias por responder. ANIMA usará esta información para personalizar tu apoyo 💬")
        st.experimental_rerun()
    st.stop()

# --- Chat principal ---
st.title("💬 Chat de apoyo ANIMA")

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-bubble-user'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-ai'>{msg['content']}</div>", unsafe_allow_html=True)

user_input = st.text_input("Escribe tu mensaje...")

if st.button("Enviar"):
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        # --- IA simulada (puedes reemplazar con Groq u OpenAI) ---
        ai_response = (
            "Gracias por compartir cómo te sientes 💬. "
            "Si necesitas ayuda inmediata, contacta a nuestro equipo en "
            "[WhatsApp](https://wa.me/56912345678). 💙"
        )
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        st.experimental_rerun()

st.markdown("---")
st.caption("WebApp ANIMA - Apoyo Emocional UDD 💙 Desarrollado con Streamlit + Groq")






