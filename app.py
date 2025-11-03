import streamlit as st
import os
from openai import OpenAI

# --- Configuración inicial ---
st.set_page_config(page_title="💬 ANIMA - Apoyo Emocional UDD", page_icon="💙", layout="centered")

# --- Cliente OpenAI ---
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Función para validar correo institucional ---
def validar_correo_udc(correo):
    return correo.lower().endswith("@udd.cl")

# --- Pantalla de inicio de sesión ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "usuario" not in st.session_state:
    st.session_state.usuario = None

if not st.session_state.autenticado:
    st.title("🔐 Inicia sesión en ANIMA - UDD")
    st.write("Por favor, inicia sesión con tu **correo institucional @udd.cl** para continuar.")
    correo = st.text_input("Correo institucional", placeholder="tucorreo@udd.cl")
    if st.button("Ingresar"):
        if validar_correo_udc(correo):
            st.session_state.autenticado = True
            st.session_state.usuario = correo
            st.success("✅ Inicio de sesión exitoso. Bienvenida/o a ANIMA 💙")
            st.rerun()
        else:
            st.error("Solo se permiten correos institucionales @udd.cl")
    st.stop()

# --- Inicialización del chat ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "historial" not in st.session_state:
    st.session_state.historial = []
if "mostrar_whatsapp" not in st.session_state:
    st.session_state.mostrar_whatsapp = False

# --- Función para guardar historial ---
def guardar_historial(usuario, mensaje, respuesta):
    nuevo = {"usuario": usuario, "mensaje": mensaje, "respuesta": respuesta}
    st.session_state.historial.append(nuevo)

# --- Función para detectar si debe derivar ---
def necesita_apoyo(mensaje):
    palabras_clave = [
        "triste", "ansiosa", "estresada", "cansada", "mal", "hablar con alguien",
        "ayuda", "psicólogo", "depresión", "no puedo", "angustia", "preocupada"
    ]
    return any(palabra in mensaje.lower() for palabra in palabras_clave)

# --- Interfaz principal ---
st.title("💙 ANIMA - Apoyo Emocional UDD")
st.caption(f"Sesión iniciada como: **{st.session_state.usuario}**")

st.write("ANIMA te escucha y te acompaña. Cuéntame cómo te sientes hoy 💛")

# Mostrar historial del chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    if necesita_apoyo(prompt):
        st.session_state.mostrar_whatsapp = True

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

        st.session_state.messages.append({"role": "assistant", "content": full_response})
        guardar_historial(st.session_state.usuario, prompt, full_response)

# --- Mostrar botón de WhatsApp ---
if st.session_state.mostrar_whatsapp:
    st.markdown("---")
    st.markdown("💚 Parece que necesitas hablar con alguien. Puedes contactar directamente con apoyo humano de la UDD:")
    whatsapp_url = "https://wa.me/56912345678?text=Hola%20ANIMA,%20necesito%20hablar%20con%20alguien%20de%20apoyo."
    st.markdown(f"[📞 Hablar con apoyo UDD]({whatsapp_url})", unsafe_allow_html=True)

# --- Historial ---
with st.expander("📋 Ver historial de conversación"):
    for item in st.session_state.historial:
        st.markdown(f"**Tú:** {item['mensaje']}")
        st.markdown(f"**ANIMA:** {item['respuesta']}")
        st.markdown("---")

# --- Botones inferiores ---
col1, col2 = st.columns(2)
with col1:
    if st.button("🧹 Reiniciar chat"):
        usuario = st.session_state.usuario
        st.session_state.clear()
        st.session_state.usuario = usuario
        st.session_state.autenticado = True
        st.rerun()

with col2:
    if st.button("🚪 Cerrar sesión"):
        st.session_state.clear()
        st.rerun()

st.markdown("---")
st.caption("WebApp ANIMA - Apoyo Emocional UDD 💙 Desarrollado con Streamlit + OpenAI")
