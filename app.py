import streamlit as st
from groq import Groq
import json
import os
from datetime import date, datetime

# ---------------- CONFIGURACIÓN GENERAL ----------------
st.set_page_config(page_title="ANIMA - Apoyo Emocional UDD", layout="centered", page_icon="💙")

# --- ESTILOS PERSONALIZADOS (mismo esquema que ya usas) ---
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #FFF8F0;
    background-image: linear-gradient(180deg, #FFFDF8 0%, #FFF5E6 100%);
}
[data-testid="stSidebar"] {
    background-color: #CBE4F9;
}
.stButton>button {
    background-color: #AED9E0;
    color: #2E2E2E;
    border-radius: 10px;
    border: none;
    font-weight: bold;
    padding: 8px 20px;
}
.stButton>button:hover {
    background-color: #BEE3ED;
    color: #000;
}
.stTextInput>div>div>input, .stTextArea>div>textarea {
    background-color: #FFFFFF;
    border: 1px solid #B0BEC5;
    border-radius: 8px;
    color: #2E2E2E;
}
[data-testid="stChatMessageUser"] {
    background-color: #FFF3E0;
    border-radius: 10px;
}
[data-testid="stChatMessageAssistant"] {
    background-color: #E3F2FD;
    border-radius: 10px;
}
h1, h2, h3, h4, h5, h6 {
    color: #2E2E2E;
    font-family: "Helvetica Neue", sans-serif;
}
body, p, label, span, div {
    color: #2E2E2E !important;
}
</style>
""", unsafe_allow_html=True)

# --- Inicializar cliente Groq ---
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- FUNCIONES AUXILIARES ---
def guardar_calendario(usuario, data):
    archivo = f"calendario_{usuario}.json"
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def cargar_calendario(usuario):
    archivo = f"calendario_{usuario}.json"
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# --- FUNCIÓN DE RESPUESTA DE IA ---
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
        if any(p in mensaje.lower() for p in ["estresada", "triste", "mal", "colapsada", "ansiosa"]):
            texto += "\n\n💬 Si necesitas apoyo inmediato, puedes escribir a nuestro equipo en [WhatsApp de Bienestar UDD](https://wa.me/56912345678)."
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
            st.warning("💛 Tus respuestas indican que podrías beneficiarte del apoyo de un profesional.")
        elif promedio < 7:
            st.info("💙 Estás en un punto intermedio. ANIMA te acompañará para mejorar tu bienestar.")
        else:
            st.success("🌸 ¡Excelente! Tu bienestar general parece estar bien equilibrado.")
        st.session_state.encuesta_respondida = True

# --- CALENDARIO INTELIGENTE ---
def calendario_inteligente(usuario):
    st.title("🗓️ Calendario Inteligente ANIMA")
    st.markdown("Organiza tu tiempo y recibe recordatorios personalizados 💙")

    data = cargar_calendario(usuario)
    color_eventos = st.color_picker("🎨 Elige el color para tus eventos:", "#AED9E0")

    with st.expander("➕ Agregar nuevo evento"):
        titulo = st.text_input("Título del evento")
        fecha = st.date_input("Fecha", value=date.today())
        descripcion = st.text_area("Descripción o detalle")
        if st.button("Agregar evento"):
            nuevo = {"titulo": titulo, "fecha": str(fecha), "descripcion": descripcion, "color": color_eventos}
            data.append(nuevo)
            guardar_calendario(usuario, data)
            st.success("✅ Evento agregado correctamente.")

    st.markdown("---")
    st.subheader("📅 Tus eventos:")

    if data:
        for evento in data:
            st.markdown(f"""
            <div style='background-color:{evento["color"]};padding:10px;border-radius:10px;margin-bottom:10px;'>
                <b>{evento["titulo"]}</b><br>
                📅 {evento["fecha"]}<br>
                📝 {evento["descripcion"]}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Aún no tienes eventos en tu calendario.")

    # --- ANÁLISIS INTELIGENTE DE EVENTOS ---
    if data:
        hoy = str(date.today())
        eventos_hoy = [e for e in data if e["fecha"] == hoy]
        total = len(data)

        st.markdown("---")
        st.subheader("💡 Recomendaciones de ANIMA:")

        if len(eventos_hoy) > 3:
            st.warning("🌙 Tienes muchos eventos hoy. Recuerda hacer pausas breves y cuidar tu energía.")
        elif len(eventos_hoy) == 0:
            st.info("📖 No tienes eventos para hoy. Puedes aprovechar para descansar o planificar la semana.")
        elif any("prueba" in e["titulo"].lower() or "certamen" in e["titulo"].lower() for e in data):
            st.warning("🧠 Veo evaluaciones en tu agenda. Intenta dormir bien y preparar pausas cortas antes del estudio.")
        elif total > 10:
            st.info("📅 Tienes una agenda muy activa. ANIMA te recomienda agendar momentos de autocuidado.")

# --- MENÚ LATERAL ---
def mostrar_menu():
    with st.sidebar:
        st.title("☰ Menú ANIMA")
        opcion = st.radio("Selecciona una opción:", ["Chat de ayuda", "Historial", "Grupos de apoyo", "Calendario inteligente", "Cerrar sesión"])

        if opcion == "Chat de ayuda":
            st.session_state.vista = "chat"
        elif opcion == "Historial":
            st.session_state.vista = "historial"
        elif opcion == "Grupos de apoyo":
            st.session_state.vista = "foros"
        elif opcion == "Calendario inteligente":
            st.session_state.vista = "calendario"
        elif opcion == "Cerrar sesión":
            st.session_state.clear()
            st.rerun()

# --- INICIO DE SESIÓN ---
if "logged_in" not in st.session_state:
    st.markdown("<h2 style='text-align:center;'>💙 ANIMA - Apoyo Emocional UDD</h2>", unsafe_allow_html=True)
    st.subheader("Inicio de sesión")
    correo = st.text_input("Correo institucional UDD", placeholder="nombre.apellido@udd.cl")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar sesión"):
        if correo.endswith("@udd.cl") and len(password) > 3:
            st.session_state.logged_in = True
            st.session_state.usuario = correo.split("@")[0]
            st.session_state.historial = []
            st.session_state.encuesta_respondida = False
            st.success("Inicio de sesión exitoso 💫")
            st.rerun()
        else:
            st.error("Por favor, usa tu correo institucional UDD y una contraseña válida.")
    st.stop()

# --- INTERFAZ PRINCIPAL ---
mostrar_menu()
vista = st.session_state.get("vista", "chat")

if vista == "chat":
    st.title("💬 Chat de apoyo emocional ANIMA")
    if not st.session_state.encuesta_respondida:
        encuesta_bienestar()
        st.stop()

    st.write(f"Hola 👋 {st.session_state.usuario}, soy **ANIMA**. ¿Cómo te sientes hoy?")
    mensaje_usuario = st.chat_input("Escribe aquí tu mensaje...")
    if mensaje_usuario:
        respuesta = obtener_respuesta(mensaje_usuario)
        st.session_state.historial.append({"user": mensaje_usuario, "bot": respuesta})
    for msg in st.session_state.historial:
        with st.chat_message("user"):
            st.write(msg["user"])
        with st.chat_message("assistant"):
            st.write(msg["bot"])

elif vista == "calendario":
    calendario_inteligente(st.session_state.usuario)

st.markdown("---")
st.caption("WebApp ANIMA - Apoyo Emocional UDD 💙 Desarrollado con Streamlit + Groq")







