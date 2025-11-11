import streamlit as st
from groq import Groq
import datetime

# =========================
# CONFIGURACIÓN BÁSICA
# =========================
st.set_page_config(page_title="Anima UDD", layout="wide")

# Inicializar cliente Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# =========================
# SESIONES
# =========================
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

if "usuario" not in st.session_state:
    st.session_state.usuario = None

if "historial" not in st.session_state:
    st.session_state.historial = []

# =========================
# BARRA LATERAL (MENÚ)
# =========================
with st.sidebar:
    st.markdown("### ☰ Menú Principal")

    menu = st.radio(
        "Navegación",
        ["💬 Chat", "👤 Inicio de sesión", "🕒 Historial", "🤝 Grupos de ayuda"],
        label_visibility="collapsed"
    )

    st.divider()
    if st.button("🧹 Reiniciar chat"):
        usuario = st.session_state.usuario
        st.session_state.clear()
        st.session_state.usuario = usuario
        st.rerun()

# =========================
# 1️⃣ INICIO DE SESIÓN
# =========================
if menu == "👤 Inicio de sesión":
    st.title("👤 Iniciar sesión en Anima UDD")

    correo = st.text_input("Correo UDD", placeholder="nombre.apellido@udd.cl")
    if st.button("Iniciar sesión"):
        if correo.endswith("@udd.cl"):
            st.session_state.usuario = correo
            st.success(f"Bienvenida/o, {correo.split('@')[0]} 💙")
        else:
            st.error("Por favor usa tu correo institucional (@udd.cl)")

    st.markdown("---")
    st.caption("WebApp ANIMA - Apoyo Emocional UDD 💙 Desarrollado con Streamlit + Groq")

# =========================
# 2️⃣ HISTORIAL DE CHAT
# =========================
elif menu == "🕒 Historial":
    st.title("🕒 Historial de conversaciones")
    if len(st.session_state.historial) == 0:
        st.info("No hay conversaciones guardadas aún.")
    else:
        for i, registro in enumerate(reversed(st.session_state.historial), 1):
            st.markdown(f"**Chat {i} - {registro['fecha']}**")
            st.write(registro['resumen'])
            st.divider()

    st.markdown("---")
    st.caption("WebApp ANIMA - Apoyo Emocional UDD 💙 Desarrollado con Streamlit + Groq")

# =========================
# 3️⃣ GRUPOS DE AYUDA
# =========================
elif menu == "🤝 Grupos de ayuda":
    st.title("🤝 Grupos de ayuda UDD")
    st.markdown("""
    Aquí puedes encontrar apoyo entre estudiantes de la universidad:

    - 💬 **Salud Mental:** Conversatorios y acompañamiento entre pares.  
    - 📚 **Apoyo Académico:** Tutorías entre estudiantes de distintas carreras.  
    - 🌱 **Bienestar Estudiantil:** Actividades recreativas y grupos de autoayuda.  

    👉 Próximamente podrás unirte directamente desde Anima.
    """)

    st.markdown("---")
    st.caption("WebApp ANIMA - Apoyo Emocional UDD 💙 Desarrollado con Streamlit + Groq")

# =========================
# 4️⃣ CHAT PRINCIPAL
# =========================
else:
    st.title("💬 Anima UDD")
    st.markdown("Tu espacio de acompañamiento emocional 🌿")

    # Mostrar mensajes del chat
    for msg in st.session_state.mensajes:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Entrada de usuario
    entrada = st.chat_input("¿Cómo te sientes hoy?")

    if entrada:
        st.session_state.mensajes.append({"role": "user", "content": entrada})
        with st.chat_message("user"):
            st.markdown(entrada)

        try:
            respuesta = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.mensajes
            )
            contenido = respuesta.choices[0].message.content
        except Exception as e:
            contenido = f"⚠️ Error al conectar con la IA: {e}"

        with st.chat_message("assistant"):
            st.markdown(contenido)

        st.session_state.mensajes.append({"role": "assistant", "content": contenido})

        # Guardar resumen en historial
        if len(st.session_state.mensajes) > 4:
            resumen = st.session_state.mensajes[-1]["content"][:150] + "..."
            st.session_state.historial.append({
                "fecha": datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
                "resumen": resumen
            })

    # 👇 Pie de página institucional
    st.markdown("---")
    st.caption("WebApp ANIMA - Apoyo Emocional UDD 💙 Desarrollado con Streamlit + Groq")


