import streamlit as st
from groq import Groq
import os
from datetime import datetime

# --- CONFIGURACIÓN GENERAL ---
st.set_page_config(page_title="ANIMA - Apoyo Emocional UDD", layout="centered", page_icon="💙")

# --- Inicializar cliente Groq ---
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- FUNCIÓN PARA OBTENER RESPUESTA DE LA IA ---
def obtener_respuesta(mensaje):
    """Genera una respuesta de la IA usando Groq"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Eres ANIMA, un asistente empático y comprensivo de apoyo emocional de la Universidad del Desarrollo (UDD). Usa un tono cálido, comprensivo y profesional."},
                {"role": "user", "content": mensaje}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error al conectar con la IA: {e}"


# --- SIMULADOR DE BASE DE DATOS DE FOROS ---
if "foros" not in st.session_state:
    st.session_state.foros = {
        "Bienestar y salud mental": [],
        "Apoyo entre compañeros": [],
        "Motivación y energía": []
    }

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

            grupo = st.selectbox(
                "Selecciona un grupo para unirte al foro:",
                ["Bienestar y salud mental", "Apoyo entre compañeros", "Motivación y energía"]
            )

            st.markdown(f"### 💬 Foro: {grupo}")

            # Mostrar mensajes previos
            if st.session_state.foros[grupo]:
                for mensaje in st.session_state.foros[grupo]:
                    st.markdown(f"**{mensaje['autor']} ({mensaje['hora']}):** {mensaje['texto']}")
                    st.markdown("---")
            else:
                st.info("Aún no hay mensajes en este grupo. Sé el primero en compartir algo 💙")

            # Enviar nuevo mensaje
            nuevo_msg = st.text_area("Escribe tu mensaje en este grupo")
            if st.button("Publicar mensaje"):
                if nuevo_msg.strip():
                    st.session_state.foros[grupo].append({
                        "autor": st.session_state.usuario.split("@")[0],
                        "texto": nuevo_msg.strip(),
                        "hora": datetime.now().strftime("%H:%M")
                    })
                    st.success("Mensaje publicado 💬")
                    st.rerun()

        elif opcion == "Cerrar sesión":
            st.session_state.clear()
            st.rerun()


# --- INICIO DE SESIÓN ---
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
            st.session_state.encuesta_realizada = False
            st.success("Inicio de sesión exitoso 💫")
            st.rerun()
        else:
            st.error("Por favor, usa tu correo institucional UDD y una contraseña válida.")
    st.stop()


# --- MOSTRAR MENÚ LATERAL ---
mostrar_menu()

# --- ENCUESTA DE BIENESTAR ---
if not st.session_state.get("encuesta_realizada", False):
    st.title("💬 Bienvenida/o a ANIMA 💙")
    st.markdown("""
    Antes de comenzar el chat, te invitamos a responder una breve **encuesta de bienestar emocional**.  
    Nos ayudará a orientarte mejor y saber si podrías necesitar apoyo psicológico o psicopedagógico.
    """)

    estado_animo = st.selectbox(
        "¿Cómo te sientes hoy?",
        ["😊 Bien", "😐 Cansado/a", "😔 Triste", "😰 Ansioso/a", "😴 Sin energía"]
    )
    energia = st.slider("¿Cómo evaluarías tu nivel de energía esta semana?", 0, 10, 5)
    concentracion = st.radio("¿Has tenido problemas para concentrarte o dormir?", ["Sí", "No"])
    apoyo = st.radio("¿Sientes que necesitas hablar con alguien sobre cómo te sientes?", ["Sí", "No", "No estoy seguro/a"])

    if st.button("Enviar respuestas"):
        puntaje = 0
        if estado_animo in ["😔 Triste", "😰 Ansioso/a", "😴 Sin energía"]:
            puntaje += 2
        if energia < 4:
            puntaje += 2
        if concentracion == "Sí":
            puntaje += 1
        if apoyo != "No":
            puntaje += 1

        if puntaje >= 4:
            st.session_state.recomendacion = "Parece que podrías beneficiarte de una conversación con nuestro equipo de apoyo psicológico 💙"
        elif puntaje == 3:
            st.session_state.recomendacion = "Podría ser útil conversar con un tutor psicopedagógico para apoyarte en la gestión académica 💬"
        else:
            st.session_state.recomendacion = "Parece que te encuentras estable emocionalmente 💪, pero siempre puedes contar con ANIMA para conversar cuando lo necesites."

        st.session_state.encuesta_realizada = True
        st.success("Gracias por responder 💙")
        st.rerun()
    st.stop()

# --- RESULTADO DE ENCUESTA ---
if "recomendacion" in st.session_state:
    st.info(f"**Sugerencia ANIMA:** {st.session_state.recomendacion}")

    # Enlace directo a WhatsApp UDD
    whatsapp_url = "https://wa.me/56912345678?text=Hola,%20soy%20estudiante%20UDD%20y%20necesito%20apoyo%20emocional"
    st.markdown(f"[💬 Hablar con apoyo psicológico en WhatsApp]({whatsapp_url})")

    st.markdown("---")

# --- INTERFAZ PRINCIPAL DEL CHAT ---
st.title("💬 Chat de apoyo emocional ANIMA")
st.write("Hola 👋 Soy **ANIMA**, tu asistente emocional UDD. Puedes contarme cómo te sientes o pedir ayuda cuando lo necesites.")

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




