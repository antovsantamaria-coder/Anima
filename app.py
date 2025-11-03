# ==============================
# ANIMA - WebApp Chat Emocional (UDD)
# ==============================
# Requisitos:
# pip install streamlit openai pandas python-dotenv

import streamlit as st
import pandas as pd
import datetime
import os
from dotenv import load_dotenv
from openai import OpenAI

# ==============================
# CONFIGURACIÓN INICIAL
# ==============================
st.set_page_config(page_title="ANIMA - Apoyo Emocional UDD", page_icon="💬", layout="centered")

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ==============================
# FUNCIONES AUXILIARES
# ==============================
def responder_ia(mensaje_usuario):
    """Genera una respuesta empática y breve desde la IA"""
    prompt = f"""
    Eres ANIMA, una IA empática creada para acompañar emocionalmente a estudiantes de la UDD.
    Tu tono es cercano, profesional y cálido.
    Clasifica la necesidad del estudiante como: 
    - Emocional
    - Académica
    - Social
    Luego da una respuesta breve y útil.
    Mensaje del estudiante: {mensaje_usuario}
    """
    try:
        respuesta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}]
        )
        return respuesta.choices[0].message.content
    except Exception as e:
        return "⚠️ No pude procesar tu mensaje en este momento. Intenta de nuevo más tarde."

def guardar_historial(usuario, mensaje, respuesta):
    """Guarda las conversaciones en sesión"""
    nuevo = {
        "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "usuario": usuario,
        "mensaje": mensaje,
        "respuesta": respuesta
    }
    st.session_state.historial = st.session_state.historial.append(nuevo, ignore_index=True)

# ==============================
# INICIO DE SESIÓN
# ==============================
st.title("💬 ANIMA - Apoyo Emocional UDD")

if "logueado" not in st.session_state:
    st.session_state.logueado = False
if "historial" not in st.session_state:
    st.session_state.historial = pd.DataFrame(columns=["fecha", "usuario", "mensaje", "respuesta"])

if not st.session_state.logueado:
    st.subheader("Inicia sesión con tu correo UDD")
    correo = st.text_input("Correo institucional", placeholder="nombre.apellido@udd.cl")
    if st.button("Ingresar"):
        if correo.endswith("@udd.cl"):
            st.session_state.logueado = True
            st.session_state.usuario = correo
            st.success(f"Bienvenido/a {correo}")
        else:
            st.error("Solo se permiten correos institucionales UDD.")
    st.stop()

# ==============================
# INTERFAZ PRINCIPAL DEL CHAT
# ==============================
st.markdown("### 🤖 Chat de acompañamiento ANIMA")
st.write("ANIMA te escucha y te acompaña. Cuéntame cómo te sientes hoy 💛")

mensaje = st.text_input("Escribe tu mensaje aquí...")

if st.button("Enviar"):
    if mensaje.strip():
        respuesta = responder_ia(mensaje)
        guardar_historial(st.session_state.usuario, mensaje, respuesta)
        st.chat_message("user").write(mensaje)
        st.chat_message("assistant").write(respuesta)
    else:
        st.warning("Por favor escribe algo antes de enviar.")

# ==============================
# HISTORIAL Y DERIVACIÓN
# ==============================
with st.expander("📜 Ver historial de conversaciones"):
    if len(st.session_state.historial) > 0:
        st.dataframe(st.session_state.historial)
    else:
        st.info("Aún no tienes historial de conversación.")

st.markdown("---")
st.markdown("### ☎️ Derivación a apoyo humano")
st.write("Si prefieres hablar con un profesional del área de bienestar UDD, haz clic abajo:")
whatsapp_link = "https://wa.me/56912345678?text=Hola%20necesito%20apoyo%20emocional%20desde%20ANIMA"
st.link_button("Hablar con un profesional en WhatsApp", whatsapp_link)

st.markdown("---")
st.caption("© 2025 ANIMA UDD — Plataforma de apoyo emocional y académico")

