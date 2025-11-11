import streamlit as st
from groq import Groq
import os

# Título y configuración de la app
st.set_page_config(page_title="ANIMA - Apoyo Emocional UDD", layout="centered", page_icon="💙")

# --- Inicializar cliente Groq ---
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- FUNCIONES AUXILIARES ---

def obtener_respuesta(mensaje):
    """Genera una respuesta de la IA usando Groq"""
    try:
        response = client.chat.completions.create(
             model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Eres un asistente empático y comprensivo de apoyo emocional de la Universidad del Desarrollo (UDD)."},
                {"role": "user", "content": mensaje}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error al conectar con la IA: {e}"

def mostrar_menu():
    """Menú lateral con opciones adicionales"""
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
            st.markdown("""
            - **Bienestar y salud mental** 🧠  
              Grupo para conversar sobre estrés académico, ansiedad y autocuidado.

            - **Apoyo entre compañeros** 🤝  
              Espacio para compartir experiencias universitarias y apoyarse mutuamente.

            - **Motivación y energía** ☀️  
              Grupo para quienes buscan mejorar su ánimo o reencontrar motivación.
            """)

        elif opcion == "Cerrar sesión":
            st.session_state.clear()
            st.rerun()  # ✅ reemplazamos experimental_rerun()


# --- SECCIÓN DE INICIO DE SESIÓN ---
if "logged_in" not in st.session_state:
    st.title("💙 ANIMA - Apoyo Emocional UDD")
    st.subheader("Inicio de sesión")
    correo = st.text_input("Correo institucional UDD", placeholder="nombre.apellido@udd.cl")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar sesión"):
        if correo.endswith("@udd.cl") and len(password) > 3:
            st.session_state.logged_in = True
            st.session_state.usuario = correo
            st.session_state.historial = []
            st.success("Inicio de sesión exitoso 💫")
            st.rerun()  # ✅ reemplazamos experimental_rerun()
        else:
            st.error("Por favor, usa tu correo institucional UDD y una contraseña válida.")
    st.stop()


# --- INTERFAZ PRINCIPAL DEL CHAT ---
mostrar_menu()

st.title("💬 Chat de apoyo emocional ANIMA")
st.write("Hola 👋 Soy **ANIMA**, tu asistente emocional UDD. ¿Cómo te sientes hoy?")

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




