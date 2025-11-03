import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="ANIMA — Lean Canvas Editor", layout="wide")

# --- Default Lean Canvas (texto en español, basado en la versión actualizada) ---
default_canvas = {
    "Proyecto": "ANIMA",
    "Problema": (
        "• Estrés, ansiedad y sobrecarga en estudiantes y jóvenes profesionales (18–30 años).\n"
        "• Dificultades de adaptación universitaria, especialmente en estudiantes con discapacidad o sin redes de apoyo.\n"
        "• Falta de acceso rápido y confiable a apoyo emocional y académico.\n"
        "• Canales institucionales lentos, poco empáticos y fragmentados.\n\n"
        "Datos propuestos:\n"
        "- 62% de los estudiantes declara haber sentido ansiedad o estrés académico severo (Encuesta 2023).\n"
        "- 35% de jóvenes con discapacidad reportan dificultades de integración (SENADIS, 2022)."
    ),
    "Solución": (
        "Chat automatizado con inteligencia artificial empática para detectar necesidades emocionales y académicas.\n"
        "- Derivación inmediata a psicólogos, tutores o redes de apoyo.\n"
        "- Integración con plataformas institucionales (bienestar, orientación, tutorías).\n"
        "- Panel de métricas para instituciones: nivel de estrés, satisfacción, tiempo de respuesta, evolución del bienestar.\n\n"
        "Valor agregado: combina psicología, psicopedagogía, IA y comunidad estudiantil para crear una red integral de apoyo humano y tecnológico."
    ),
    "Propuesta de valor": (
        "Un solo canal para acompañamiento emocional y académico, ágil, empático y confidencial.\n\n"
        "Chat inteligente con respuesta inmediata y derivación profesional. Plataforma accesible e integrada a las necesidades institucionales.\n\n"
        "Diferenciador: enfoque inclusivo que contempla estudiantes con y sin discapacidad, con apoyo especializado."
    ),
    "Ventaja competitiva": (
        "• Integración única de apoyo emocional, académico e inclusivo.\n"
        "• Adaptabilidad a distintos contextos (universidades, institutos, empresas).\n"
        "• Diseño centrado en el usuario, con lenguaje empático.\n"
        "• Basado en datos reales que permiten medir impacto y mejora continua."
    ),
    "Segmento de clientes": (
        "• Estudiantes universitarios y jóvenes profesionales (18–30 años).\n"
        "• Universidades, institutos y organizaciones con programas de bienestar.\n"
        "• Primeros adoptantes: instituciones con áreas de apoyo psicoeducativo e inclusión."
    ),
    "Métricas clave": (
        "• Satisfacción ≥ 80%.\n"
        "• Adopción institucional ≥ 60%.\n"
        "• Reducción del tiempo de espera ≥ 50%.\n"
        "• Retención mensual de usuarios activos ≥ 70%.\n"
        "• Incremento en derivaciones efectivas a profesionales ≥ 30%."
    ),
    "Canales": (
        "• Convenios con instituciones educativas.\n"
        "• Difusión en redes sociales y plataformas universitarias.\n"
        "• Integración en intranets y webs institucionales.\n"
        "• Participación en ferias de bienestar y jornadas de salud mental."
    ),
    "Flujo de ingresos": (
        "• Modelo B2B2C (licencias institucionales).\n"
        "• Servicios complementarios: reportes analíticos, capacitaciones, integraciones.\n"
        "• Versión gratuita limitada para estudiantes individuales."
    ),
    "Estructura de costos": (
        "• Desarrollo tecnológico y mantenimiento.\n"
        "• Honorarios de psicólogos, psicopedagogos y tutores asociados.\n"
        "• Marketing, alianzas y difusión.\n"
        "• Hosting, seguridad y soporte de datos."
    ),
    "Notas": "Creado: " + datetime.now().strftime("%Y-%m-%d %H:%M")
}

# --- UI ---
st.title("🧩 ANIMA — Lean Canvas Editor")
st.write("Edita el Lean Canvas y descarga la versión lista para presentar o compartir.")

# Two-column top: project name + actions
col1, col2 = st.columns([3,1])
with col1:
    project = st.text_input("Nombre del proyecto", default=default_canvas["Proyecto"])
with col2:
    st.markdown("**Acciones**")
    col_actions = st.container()
    st.write("")  # spacing

# hold canvas in session state for persistence while editing
if "canvas" not in st.session_state:
    st.session_state.canvas = default_canvas.copy()
    st.session_state.canvas["Proyecto"] = project

# allow user to reset to defaults
with col2:
    if st.button("Restablecer valores por defecto"):
        st.session_state.canvas = default_canvas.copy()
        st.experimental_rerun()

st.markdown("---")

# Editable areas arranged in a grid similar to a Lean Canvas
areas = [
    ("Problema", 3),
    ("Solución", 3),
    ("Propuesta de valor", 3),
    ("Ventaja competitiva", 3),
    ("Segmento de clientes", 3),
    ("Métricas clave", 3),
    ("Canales", 3),
    ("Flujo de ingresos", 3),
    ("Estructura de costos", 3),
    ("Notas", 1)
]

# Render editable text areas in rows of 3
cols_per_row = 3
for i in range(0, len(areas), cols_per_row):
    cols = st.columns(cols_per_row)
    for j, (area, height) in enumerate(areas[i:i+cols_per_row]):
        with cols[j]:
            st.subheader(area)
            current = st.session_state.canvas.get(area, "")
            new_text = st.text_area("", value=current, height=height*60, key=f"ta_{area}")
            st.session_state.canvas[area] = new_text

st.markdown("---")

# Right side: preview + export buttons
left, right = st.columns([3,1])
with left:
    st.header("Vista previa del Lean Canvas")
    st.markdown(f"### {project}")
    # Simple formatted preview
    for key in ["Problema","Solución","Propuesta de valor","Ventaja competitiva","Segmento de clientes",
                "Métricas clave","Canales","Flujo de ingresos","Estructura de costos","Notas"]:
        st.markdown(f"**{key}**")
        st.markdown(st.session_state.canvas.get(key, ""))
        st.write("")

with right:
    st.header("Exportar / Compartir")
    # JSON export
    canvas_export = st.session_state.canvas.copy()
    canvas_export["Proyecto"] = project
    json_str = json.dumps(canvas_export, ensure_ascii=False, indent=2)
    st.download_button("📥 Descargar JSON", data=json_str, file_name=f"lean_canvas_{project}.json", mime="application/json")

    # Markdown export
    def canvas_to_markdown(canvas_dict):
        lines = [f"# {canvas_dict.get('Proyecto','Proyecto')}\n"]
        for k, v in canvas_dict.items():
            if k == "Proyecto": continue
            lines.append(f"## {k}\n{v}\n")
        return "\n".join(lines)

    md = canvas_to_markdown(canvas_export)
    st.download_button("📥 Descargar Markdown", data=md, file_name=f"lean_canvas_{project}.md", mime="text/markdown")
    st.write("")
    st.markdown("**Copiar Markdown**")
    st.text_area("Markdown (copiar manualmente si quieres)", value=md, height=300)

st.markdown("---")
st.caption("App generada automáticamente para editar y exportar el Lean Canvas de ANIMA. Puedes usar esto como base y ampliar con integración a bases de datos, autenticación o export a PDF/imagen según necesites.")
