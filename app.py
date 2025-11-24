# app.py - ANIMA con Calendario Inteligente (vista mensual, recordatorios, persistencia por usuario)
import streamlit as st
from groq import Groq
import os, json
from datetime import date, datetime, timedelta
import calendar

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="ANIMA - Apoyo Emocional UDD", layout="wide", page_icon="💙")

# ---------------- FORCE LIGHT THEME + STYLES ----------------
st.markdown("""
<style>
:root { color-scheme: light !important; }
[data-testid="stAppViewContainer"], body { background-color: #FFF8E7 !important; }
[data-testid="stSidebar"] { background-color: #CBE4F9 !important; color: #333333 !important; }
/* Buttons */
.stButton>button { background-color: #AED9E0; color: #333333; border-radius:10px; padding:8px 18px; font-weight:600; border:none; }
.stButton>button:hover { background-color:#BEE3ED; }
/* Inputs */
.stTextInput>div>div>input, .stTextArea>div>textarea { background:#FFFFFF; color:#333333; border:1px solid #EADFCB; border-radius:8px; }
/* Chat input area */
[data-baseweb="textarea"] textarea { background-color:#FFFFFF !important; color:#333333 !important; border:1px solid #EADFCB !important; border-radius:20px !important; padding:10px 14px !important; }
/* Chat messages neutral */
[data-testid="stChatMessageUser"], [data-testid="stChatMessageAssistant"] { background-color: transparent !important; color:#333333 !important; border:none !important; padding:0 !important; }
/* Calendar cells */
.calendar-cell { padding:8px; vertical-align: top; }
.calendar-day-num { font-weight:600; color:#333333; margin-bottom:6px; }
.event-pill { display:inline-block; padding:4px 8px; border-radius:8px; font-size:12px; margin:2px 0; color:#222; }
/* Keep text color readable and avoid forcing uppercase */
h1,h2,h3,h4,h5,h6,p,div,span,label { color:#333333 !important; text-transform: none !important; font-family: "Helvetica Neue", "Open Sans", sans-serif; }
/* Remove heavy shadows / borders */
* { box-shadow: none !important; }
/* Floating menu button */
#menu-btn { position: fixed; top: 18px; left: 18px; z-index: 999; background:#AED9E0; color:#333333; border:none; padding:6px 10px; border-radius:10px; font-weight:700; cursor:pointer; }
/* Scrollbar pastel */
::-webkit-scrollbar { width:8px; }
::-webkit-scrollbar-thumb { background-color:#EBDDC9; border-radius:4px; }
</style>
""", unsafe_allow_html=True)

# Floating menu button (toggles the sidebar)
if "menu_open" not in st.session_state:
    st.session_state.menu_open = False

def toggle_menu():
    st.session_state.menu_open = not st.session_state.menu_open

if st.button("☰", key="menu_button"):
    toggle_menu()

# show/hide sidebar
if st.session_state.menu_open:
    with st.sidebar:
        st.title("☰ Menú ANIMA")
        choice = st.radio("Ir a:", ["Chat de ayuda", "Historial", "Grupos de apoyo", "Calendario ANIMA", "Cerrar sesión"])
        st.session_state.menu_choice = choice
        st.markdown("---")
        st.caption("ANIMA · Apoyo Emocional UDD 💙")

# ---------------- GROQ CLIENT (if not available, app still runs but IA responses will show error) ----------------
client = None
try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except Exception:
    client = None

def ai_reply(prompt):
    """Llamada segura a Groq; si falla, devuelve texto por defecto."""
    if client is None:
        return "ANIMA no puede conectarse al servicio de IA en este momento. Igual puedo ayudarte con tu calendario."
    try:
        # Instrucción de sistema con enlace a WhatsApp en caso de riesgo
        system_instruction = (
            "Eres ANIMA, un asistente empático de la UDD que ayuda a planificar y cuidar el bienestar. "
            "Si detectas que el usuario expresa angustia severa, pensamientos de riesgo o solicita ayuda profesional explícita, "
            "DEBES finalizar tu respuesta sugiriendo contactar a los especialistas y proporcionar este enlace de WhatsApp: "
            "https://wa.me/569XXXXXXXX (Indícalo amablemente)."
        )
        
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role":"system", "content": system_instruction},
                {"role":"user", "content": prompt}
            ]
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"ANIMA no pudo generar respuesta automática ({e})."

# ---------------- Persistence utils ----------------
def user_file(username):
    safe = username.replace(" ", "_")
    return f"calendar_{safe}.json"

def load_user_data(username):
    f = user_file(username)
    if os.path.exists(f):
        try:
            with open(f,"r",encoding="utf-8") as fh:
                return json.load(fh)
        except Exception:
            return {"events": [], "prefs": {}}
    else:
        return {"events": [], "prefs": {}}

def save_user_data(username, data):
    f = user_file(username)
    with open(f,"w",encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=4)

# ---------------- Login & Session init ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "menu_choice" not in st.session_state:
    st.session_state.menu_choice = "Chat de ayuda"
if "survey_done" not in st.session_state:
    st.session_state.survey_done = False
if "risk_detected" not in st.session_state:
    st.session_state.risk_detected = False

def login_block():
    st.markdown("<h2 style='text-align:center;'>💙 ANIMA - Apoyo Emocional UDD</h2>", unsafe_allow_html=True)
    st.subheader("Inicio de sesión")
    correo = st.text_input("Correo institucional UDD", placeholder="nombre.apellido@udd.cl")
    password = st.text_input("Contraseña", type="password")
    if st.button("Iniciar sesión"):
        if correo and correo.endswith("@udd.cl") and len(password) > 3:
            st.session_state.logged_in = True
            st.session_state.user = correo.split("@")[0]
            st.success("Inicio de sesión exitoso 💫")
            st.rerun()

        else:
            st.error("Usa un correo institucional válido (@udd.cl) y una contraseña de al menos 4 caracteres.")
    st.stop()

# if not logged in, show login
if not st.session_state.logged_in:
    login_block()

# load user data
user = st.session_state.user
user_data = load_user_data(user)  # {"events":[...], "prefs": {...}}

# ensure structure
if "events" not in user_data:
    user_data["events"] = []
if "prefs" not in user_data:
    user_data["prefs"] = {}

# default color preference
if "color_event" not in user_data["prefs"]:
    user_data["prefs"]["color_event"] = "#AED9E0"
if "calendar_view" not in user_data["prefs"]:
    user_data["prefs"]["calendar_view"] = "Mensual"

# ---------------- Survey (encuesta previa) ----------------
def survey_block():
    st.subheader("💭 Encuesta breve de bienestar")
    energia = st.slider("Nivel de energía (0-10)", 0, 10, 5, key="s_energia")
    animo = st.slider("Ánimo (0-10)", 0, 10, 5, key="s_animo")
    concentracion = st.slider("Concentración (0-10)", 0, 10, 5, key="s_conc")
    motivacion = st.slider("Motivación (0-10)", 0, 10, 5, key="s_motiv")
    if st.button("Enviar encuesta"):
        prom = (energia + animo + concentracion + motivacion)/4
        st.session_state.survey_done = True
        # Keep summary in session for suggestions later
        st.session_state.survey_summary = {"energia":energia,"animo":animo,"conc":concentracion,"motiv":motivacion,"prom":prom}
        
        # --- MODIFICACIÓN: Detectar riesgo automáticamente ---
        # Si el promedio es bajo (< 4), activamos la alerta
        if prom < 4.0:
            st.session_state.risk_detected = True
        else:
            st.session_state.risk_detected = False
            
        st.success("Gracias. ANIMA usará esto para sugerir una planificación equilibrada.")
        st.rerun()
    st.stop()

# If not done survey, show it on first visit to calendar or chat
if not st.session_state.survey_done:
    survey_block()

# --- MODIFICACIÓN: MOSTRAR ALERTA AUTOMÁTICA SI HAY RIESGO ---
# Esto aparece en CUALQUIER pantalla si la encuesta fue negativa
if st.session_state.get("risk_detected", False):
    st.error("⚠️ ANIMA ha detectado que tus niveles de energía o ánimo están bajos.")
    st.markdown("""
    <div style="background-color: #f8d7da; padding: 15px; border-radius: 10px; border: 1px solid #f5c6cb; color: #721c24; margin-bottom: 20px;">
        <h3 style="margin-top:0; color: #721c24;">🆘 Apoyo Profesional UDD</h3>
        <p>No tienes que pasar por esto solo/a. El equipo de bienestar está disponible para escucharte.</p>
        <a href="https://wa.me/569XXXXXXXX" target="_blank" style="text-decoration: none;">
            <button style="background-color: #25D366; color: white; border: none; padding: 10px 20px; border-radius: 5px; font-weight: bold; font-size: 16px; cursor: pointer;">
                💬 Contactar por WhatsApp ahora
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

# ---------------- Helpers for calendar ----------------
def parse_date(d):
    if isinstance(d, str):
        return datetime.fromisoformat(d).date()
    if isinstance(d, date):
        return d
    return None

def events_on_day(events, d):
    dstr = str(d)
    return [e for e in events if e.get("date")==dstr]

def upcoming_events(events, days=3):
    today = date.today()
    out = []
    for e in events:
        ed = parse_date(e.get("date"))
        if ed is None:
            continue
        delta = (ed - today).days
        if 0 <= delta <= days:
            out.append((delta,e))
    out.sort(key=lambda x: x[0])
    return out

def month_matrix(year, month):
    cal = calendar.Calendar(firstweekday=0)  # Monday=0? here Sunday=6; but we'll use default
    weeks = cal.monthdayscalendar(year, month)
    return weeks

# ---------------- Calendar UI render (monthly grid) ----------------
def render_month_view(events, year, month, prefs):
    # Build mapping of date -> list events
    events_map = {}
    for e in events:
        ed = e.get("date")
        if ed:
            events_map.setdefault(ed, []).append(e)

    weeks = month_matrix(year, month)
    month_name = calendar.month_name[month]
    html = f"<div style='width:100%'><h3 style='margin-bottom:6px'>{month_name} {year}</h3>"
    html += "<table style='width:100%; border-collapse:collapse;'>"
    # header weekdays
    html += "<tr>"
    for wd in ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]:
        html += f"<th style='text-align:left;padding:8px;color:#2B2B2B'>{wd}</th>"
    html += "</tr>"
    # weeks
    for wk in weeks:
        html += "<tr>"
        for day in wk:
            if day == 0:
                html += "<td class='calendar-cell' style='height:90px;background:transparent'></td>"
            else:
                ddate = date(year, month, day)
                key = str(ddate)
                pills_html = ""
                if key in events_map:
                    # show up to 2 event pills
                    for ev in events_map[key][:2]:
                        title_short = ev.get("title","").replace("<","").replace(">","")
                        color = ev.get("color", prefs.get("color_event","#AED9E0"))
                        pills_html += f"<div class='event-pill' style='background:{color};color:#222;margin-top:4px;'>{title_short[:18]}</div>"
                    if len(events_map[key])>2:
                        pills_html += f"<div style='font-size:12px;color:#6b6b6b;margin-top:4px;'>+{len(events_map[key])-2} more</div>"
                html += f"<td class='calendar-cell' style='vertical-align:top; padding:8px; height:90px;'>"
                html += f"<div class='calendar-day-num'>{day}</div>{pills_html}</td>"
        html += "</tr>"
    html += "</table></div>"
    st.markdown(html, unsafe_allow_html=True)

# ---------------- Smart recommendations ----------------
def smart_recommendations(events, survey):
    recs = []
    today = date.today()
    # upcoming 3 days
    up = upcoming_events(events, days=3)
    if up:
        for delta, e in up:
            d = parse_date(e["date"])
            when = "hoy" if delta==0 else f"en {delta} día(s)"
            recs.append(f"🔔 {when}: {e['title']}. {('Hora: ' + e.get('time')) if e.get('time') else ''}")
    # overloaded days
    # compute counts per day for coming week
    counts = {}
    for e in events:
        ed = parse_date(e.get("date"))
        if ed:
            if 0 <= (ed - today).days <= 7:
                counts.setdefault(str(ed),0)
                counts[str(ed)] += 1
    overloaded = [d for d,c in counts.items() if c >= 3]
    if overloaded:
        recs.append("⚠️ Noté días muy cargados esta semana. ANIMA sugiere incluir pausas de 10-15 minutos cada 90 minutos de estudio.")
    # based on survey avg (if present)
    if survey:
        prom = survey.get("prom", None)
        if prom is not None and prom < 4:
            recs.append("💛 Tu encuesta indica baja energía. ANIMA recomienda planificar bloques más cortos de estudio y más descansos.")
    # suggestions based on keywords
    keywords = ["prueba","certamen","examen","entrega","control"]
    if any(any(k in e.get("title","").lower() for k in keywords) for e in events):
        recs.append("🧠 Tienes evaluaciones próximas: intenta programar repasos cortos y sueño reparador la noche anterior.")
    return recs

# ---------------- Calendar Editor UI ----------------
def calendar_editor(user_data):
    st.subheader("Configuración y eventos")
    prefs = user_data.get("prefs", {})
    # color preference
    col = st.color_picker("Color por defecto para nuevos eventos", prefs.get("color_event","#AED9E0"))
    prefs["color_event"] = col
    user_data["prefs"] = prefs

    st.markdown("### Agregar evento")
    c1, c2 = st.columns(2)
    with c1:
        title = st.text_input("Título", key="evt_title")
        ev_date = st.date_input("Fecha", value=date.today(), key="evt_date")
    with c2:
        ev_time = st.text_input("Hora (opcional, ej. 14:30)", key="evt_time")
        desc = st.text_area("Descripción (opcional)", key="evt_desc")

    add_clicked = st.button("Agregar evento")
    if add_clicked:
        if not title.strip():
            st.error("El evento necesita un título.")
        else:
            new = {"title": title.strip(), "date": str(ev_date), "time": ev_time.strip(), "desc": desc.strip(), "color": prefs.get("color_event","#AED9E0")}
            user_data.setdefault("events", []).append(new)
            save_user_data(user, user_data)
            st.success("Evento agregado correctamente.")
            st.rerun()

    st.markdown("---")
    st.subheader("Tus eventos (editar / eliminar)")
    events = user_data.get("events", [])
    if not events:
        st.info("No tienes eventos todavía.")
    else:
        # list with delete buttons
        for idx, e in enumerate(events):
            st.markdown(f"**{e.get('title')}** — {e.get('date')} {(' - ' + e['time']) if e.get('time') else ''}")
            st.write(e.get("desc",""))
            col1, col2 = st.columns([0.1,0.9])
            with col1:
                if st.button("Eliminar", key=f"del_{idx}"):
                    events.pop(idx)
                    user_data["events"] = events
                    save_user_data(user, user_data)
                    st.success("Evento eliminado.")
                    st.experimental_rerun()
            with col2:
                if st.button("Editar", key=f"edit_{idx}"):
                    # bring up edit form
                    new_title = st.text_input("Nuevo título", value=e.get("title"), key=f"nt_{idx}")
                    new_date = st.date_input("Nueva fecha", value=parse_date(e.get("date")), key=f"nd_{idx}")
                    new_time = st.text_input("Nueva hora", value=e.get("time",""), key=f"ntm_{idx}")
                    new_desc = st.text_area("Nueva descripción", value=e.get("desc",""), key=f"ndesc_{idx}")
                    if st.button("Guardar cambios", key=f"save_{idx}"):
                        events[idx] = {"title": new_title, "date": str(new_date), "time": new_time, "desc": new_desc, "color": e.get("color", prefs.get("color_event"))}
                        user_data["events"] = events
                        save_user_data(user, user_data)
                        st.success("Cambios guardados.")
                        st.experimental_rerun()

# ---------------- MAIN VIEWS ----------------
# Sidebar fallback (when menu_open False)
if not st.session_state.menu_open:
    # keep a small sidebar to navigate
    with st.sidebar:
        st.title("ANIMA")
        choice = st.radio("Ir a:", ["Chat de ayuda", "Historial", "Grupos de apoyo", "Calendario ANIMA", "Cerrar sesión"])
        st.session_state.menu_choice = choice

choice = st.session_state.get("menu_choice","Chat de ayuda")

if choice == "Cerrar sesión":
    st.session_state.clear()
    st.rerun()


# Chat view
if choice == "Chat de ayuda":
    st.title("💬 Chat de apoyo emocional ANIMA")
    st.write(f"Hola {user}, soy ANIMA. ¿Cómo te sientes hoy?")
    # quick suggestions from calendar when entering chat
    recs = smart_recommendations(user_data.get("events",[]), st.session_state.get("survey_summary", None))
    if recs:
        st.markdown("### Recomendaciones rápidas de ANIMA")
        for r in recs[:5]:
            st.info(r)
    # chat input (simple)
    user_msg = st.chat_input("Escribe aquí tu mensaje...")
    if user_msg:
        reply = ai_reply(user_msg)
        # keep minimal chat history in session
        if "chat_hist" not in st.session_state:
            st.session_state.chat_hist = []
        st.session_state.chat_hist.append({"user":user_msg, "bot":reply})
    # show chat history
    if "chat_hist" in st.session_state:
        for m in st.session_state.chat_hist:
            with st.chat_message("user"):
                st.write(m["user"])
            with st.chat_message("assistant"):
                st.write(m["bot"])

# Calendar view
elif choice == "Calendario ANIMA":
    st.title("🗓️ Calendario ANIMA")
    # top: quick reminders
    reminders = upcoming_events(user_data.get("events",[]), days=3)
    if reminders:
        st.subheader("🔔 Recordatorios próximos")
        for delta, e in reminders:
            when = "Hoy" if delta==0 else f"En {delta} día(s)"
            st.info(f"{when}: {e.get('title')} — {e.get('date')} {('(' + e.get('time') + ')') if e.get('time') else ''}")

    st.markdown("---")
    # settings and editor
    calendar_editor(user_data)

    st.markdown("---")
    # monthly grid
    st.subheader("Vista mensual")
    # navigation
    if "cal_year" not in st.session_state:
        st.session_state.cal_year = date.today().year
    if "cal_month" not in st.session_state:
        st.session_state.cal_month = date.today().month

    nav1, nav2, nav3 = st.columns([1,2,1])
    with nav1:
        if st.button("◀️ Mes anterior"):
            m = st.session_state.cal_month - 1
            y = st.session_state.cal_year
            if m < 1:
                m = 12; y -= 1
            st.session_state.cal_month = m; st.session_state.cal_year = y
    with nav2:
        st.markdown(f"### {calendar.month_name[st.session_state.cal_month]} {st.session_state.cal_year}")
    with nav3:
        if st.button("Mes siguiente ▶️"):
            m = st.session_state.cal_month + 1
            y = st.session_state.cal_year
            if m > 12:
                m = 1; y += 1
            st.session_state.cal_month = m; st.session_state.cal_year = y

    render_month_view(user_data.get("events",[]), st.session_state.cal_year, st.session_state.cal_month, user_data.get("prefs",{}))

    st.markdown("---")
    st.caption("WebApp ANIMA - Apoyo Emocional UDD 💙 Desarrollado con Streamlit + Groq")

# Foros view (simple area)
elif choice == "Grupos de apoyo":
    st.title("🤝 Grupos de apoyo UDD (Anónimo)")
    # simple local forum (session-based)
    if "forums" not in st.session_state:
        st.session_state.forums = {"Bienestar y salud mental": [], "Apoyo entre compañeros": [], "Motivación y energía": []}
    group = st.selectbox("Selecciona grupo", list(st.session_state.forums.keys()))
    st.markdown(f"### Foro: {group}")
    for msg in st.session_state.forums[group]:
        st.markdown(f"**Anónimo ({msg['time']}):** {msg['text']}")
    new_msg = st.text_area("Escribe un comentario")
    if st.button("Publicar comentario"):
        if new_msg.strip():
            # FORO ANONIMO
            st.session_state.forums[group].append({"author":"Anónimo","time":datetime.now().strftime("%H:%M"),"text":new_msg.strip()})
            st.success("Publicado.")
            st.rerun()


# Historial view
elif choice == "Historial":
    st.title("🕒 Historial de conversaciones")
    hist = st.session_state.get("historial", [])
    if not hist:
        st.info("Aún no hay historial.")
    else:
        for h in hist:
            st.markdown(f"**Tú:** {h.get('user')}")
            st.markdown(f"**ANIMA:** {h.get('bot')}")
            st.markdown("---")

# save any changes to user_data at end
save_user_data(user, user_data)







