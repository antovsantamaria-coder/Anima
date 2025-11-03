import streamlit as st
import os
from openai import OpenAI

# Configuración inicial
st.set_page_config(page_title="💬 ANIMA - Apoyo Emocional UDD", page_icon="💙", layout="centered")

# Cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Inicialización de variables en session_state ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "historial" not in st.session_state:
    st.session_state.historial = []
if "usuario" not in st.session_state:
    st.session_state.usuario = "Invitado"

# --- Función para guardar historial ---
def guardar_historial(usuario, mensaje, respuesta):
    nuevo = {"usuario": usuario, "mensaje": mensaje, "respuesta": respuesta}
    st.session_state.historial.append(nuevo)

# --- Interfaz principal ---
st.title("💙 ANIMA - Apoyo Emocional UDD")
st.write("ANIMA te escucha y te acompaña. Cuéntame cómo te sientes hoy 💛")

# Mostrar historial de chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- Llamada a la IA ---
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres ANIMA, un asistente emocional de la Universidad del Desarrollo. Escucha con empatía, haz preguntas suaves y deriva a un profesional si es necesario."},
                    *st.session_state.messages,
                ],
                stream=True,
            )

            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        except Exception as e:
            full_response = "No pude conectarme en este momento 😔"
            st.error(f"Error al conectar con la IA: {e}")

        # Guardar respuesta
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        # Guardar historial del chat
        guardar_historial(st.session_state.usuario, prompt, full_response)

# --- Mostrar historial si el usuario lo desea ---
with st.expander("📋 Ver historial de conversación"):
    for item in st.session_state.historial:
        st.markdown(f"**Tú:** {item['mensaje']}")
        st.markdown(f"**ANIMA:** {item['respuesta']}")
        st.markdown("---")

# --- Botón para limpiar chat ---
if st.button("🧹 Reiniciar chat"):
    usuario = st.session_state.usuario
    st.session_state.clear()
    st.session_state.usuario = usuario
    st.rerun()


st.markdown("---")
st.caption("WebApp ANIMA - Apoyo Emocional UDD 💙 Desarrollado con Streamlit + OpenAI")
