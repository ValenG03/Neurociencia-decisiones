import json
import math
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="DECIDIR · Laboratorio", page_icon="🧠", layout="wide")

st.markdown("""
<style>
.stApp {background:#f5f7fb; color:#17233b;}
[data-testid="stHeader"] {background:transparent;}
.block-container {max-width:1100px; padding-top:2rem;}
h1,h2,h3 {color:#17233b !important; letter-spacing:-.025em;}
[data-testid="stVerticalBlockBorderWrapper"] {border-radius:18px;}
.hero {background:linear-gradient(120deg,#152846,#244d69);padding:32px;
 border-radius:24px;color:#fff;margin-bottom:24px;}
.hero h1 {color:#fff !important;font-size:2.7rem;margin:8px 0;}
.hero p {color:#dbe8f5;max-width:680px;}
.eyebrow {font-size:12px;letter-spacing:3px;font-weight:700;color:#87e3d3;}
div.stButton>button {border-radius:12px;min-height:46px;}
div.stButton>button[kind="primary"] {background:#166b63;border:0;color:white;}
[data-testid="stMetric"] {background:#e9eef6;padding:16px;border-radius:16px;}
</style>
""", unsafe_allow_html=True)

SOURCES = {
    "frame": ("De Martino et al. (2006) · Encuadre y decisión",
              "https://pmc.ncbi.nlm.nih.gov/articles/PMC2631940/"),
    "time": ("Kable y Glimcher (2007) · Valor subjetivo y espera",
             "https://pmc.ncbi.nlm.nih.gov/articles/PMC2845395/"),
    "social": ("Sanfey et al. (2003) · Juego del ultimátum",
               "https://pubmed.ncbi.nlm.nih.gov/12805551/"),
    "loss": ("Tom et al. (2007) · Ganancias y pérdidas",
             "https://pubmed.ncbi.nlm.nih.gov/17255512/"),
}

# Adaptaciones educativas: no son réplicas de los protocolos originales.
TASKS = [
    dict(title="Un regalo con dos caminos", tag="01 · Elegir",
         text="Recibís 100 fichas. Elegí cómo terminar esta ronda independiente.",
         options=["Conservar 40 fichas con certeza.",
                  "40% de terminar con 100 fichas; 60% de terminar con 0."],
         readings=["Elegiste asegurar 40 fichas en esta ronda.",
                   "Elegiste una alternativa incierta con promedio de 40 fichas."],
         lesson="Ambas opciones tienen valor esperado de 40 fichas. Igual promedio no significa igual riesgo ni igual atractivo personal.",
         neuro="En una tarea de encuadre monetario, De Martino y colegas observaron una asociación entre actividad de la amígdala y elecciones sensibles al encuadre.",
         regions=["AMY"], source="frame"),
    dict(title="Ahora o después", tag="02 · Esperar",
         text="Podés recibir un premio hoy o dentro de 30 días. Suponé que el pago está garantizado, que el poder de compra no cambia y que no hay intereses ni costos.",
         options=["Recibir 100 unidades hoy.", "Recibir 140 unidades en 30 días."],
         readings=["Elegiste la recompensa inmediata; eso puede reflejar el costo que tiene esperar para vos.",
                   "Elegiste esperar 30 días a cambio de 40 unidades adicionales."],
         lesson="Una elección aislada no estima tu impulsividad ni tu tasa de descuento. Necesitaríamos muchas combinaciones de montos y plazos.",
         neuro="Kable y Glimcher encontraron correlaciones entre valor subjetivo y señal de fMRI en corteza prefrontal medial, estriado ventral y corteza cingulada posterior.",
         regions=["MPFC", "VS", "PCC"], source="time"),
    dict(title="Un reparto desigual", tag="03 · Negociar",
         text="Una persona desconocida reparte 10 fichas: se queda con 8 y te ofrece 2. Es una única interacción, sin reputación ni negociaciones futuras. Si rechazás, ambos reciben 0.",
         options=["Aceptar: recibo 2 y la otra persona recibe 8.",
                  "Rechazar: ambos recibimos 0."],
         readings=["Aceptaste el reparto y obtuviste 2 fichas pese a la desigualdad.",
                   "Rechazaste el reparto y renunciaste a 2 fichas; la otra persona tampoco cobra."],
         lesson="Aceptar maximiza tu pago en esta ronda; rechazar puede expresar rechazo a la desigualdad. La elección no mide tu moralidad.",
         neuro="Sanfey y colegas observaron respuestas a ofertas injustas en ínsula anterior y corteza prefrontal dorsolateral. Es una asociación grupal, no un detector de injusticia individual.",
         regions=["AI", "DLPFC"], source="social"),
    dict(title="Evitar una pérdida", tag="04 · Resolver",
         text="En una nueva ronda tenés 100 fichas. Debés elegir entre estas alternativas.",
         options=["Perder 60 fichas con certeza.",
                  "40% de no perder ninguna; 60% de perder las 100."],
         readings=["Elegiste la pérdida cierta y terminás con 40 fichas.",
                   "Elegiste arriesgarte para tener una posibilidad de no perder fichas."],
         lesson="Los resultados posibles son idénticos a los del escenario 1: 40 seguras o 40% de obtener 100. Cambió la manera de describirlos.",
         neuro="La evidencia sobre encuadre vincula contexto y valoración. No permite afirmar que una región controló tu elección ni dividir tu cerebro en racional y emocional.",
         regions=["AMY"], source="frame"),
    dict(title="¿Aceptarías la apuesta?", tag="05 · Arriesgar",
         text="Esta apuesta es independiente de las rondas anteriores. Podés afrontar la pérdida y no hay costos adicionales.",
         options=["Aceptar: 50% de ganar 150 fichas y 50% de perder 100.",
                  "Rechazar: no gano ni pierdo fichas."],
         readings=["Aceptaste una apuesta de valor esperado positivo, con posibilidad real de perder 100 fichas.",
                   "Rechazaste la apuesta y evitaste una posible pérdida de 100 fichas."],
         lesson="El valor esperado es +25 fichas. Rechazar no demuestra por sí solo aversión a las pérdidas: también puede influir la aversión al riesgo.",
         neuro="Tom y colegas relacionaron diferencias en sensibilidad a ganancias y pérdidas con respuestas en estriado ventral y corteza prefrontal durante apuestas monetarias.",
         regions=["VS", "PFC"], source="loss"),
]

# Posiciones didácticas, NO coordenadas de un atlas o focos de activación.
REGIONS = {
    "AMY": (43, 32, "Amígdala", "Región profunda; asociación con encuadre en el estudio citado."),
    "MPFC": (22, 51, "Prefrontal medial", "Cara medial; asociación con valor subjetivo."),
    "VS": (38, 43, "Estriado ventral", "Región profunda; valoración de recompensas y pérdidas."),
    "PCC": (65, 61, "Cingulada posterior", "Cara medial; asociación con valor subjetivo."),
    "AI": (34, 48, "Ínsula anterior", "Oculta bajo la corteza lateral; respuesta a ofertas injustas."),
    "DLPFC": (28, 73, "Prefrontal dorsolateral", "Superficie lateral; respuesta en la tarea de ultimátum."),
    "PFC": (16, 60, "Corteza prefrontal", "Etiqueta amplia; incluye subregiones, no un foco específico."),
}

def chart(fig, key):
    fig.update_layout(template="plotly_white", font=dict(color="#17233b"),
                      paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=20,r=20,t=35,b=25))
    st.plotly_chart(fig, width="stretch", key=key,
                    config={"displayModeBar": False})

def brain(selected):
    fig = go.Figure()
    fig.add_shape(type="path", path=(
        "M 10,42 C 0,57 10,77 25,82 C 37,95 65,93 80,82 "
        "C 100,80 109,58 99,42 C 94,29 75,23 60,28 C 42,15 23,25 10,42 Z"
    ), fillcolor="#e2e8f2", line=dict(color="#9faec5", width=2))
    # Contorno inferior independiente para una silueta cerrada más legible.
    for path in ["M 24,73 Q 42,82 58,72", "M 58,72 Q 82,80 94,61",
                 "M 18,56 Q 37,65 48,54", "M 55,54 Q 78,63 94,49"]:
        fig.add_shape(type="path", path=path, line=dict(color="#bfcbdd",width=2))
    for code, (x,y,name,detail) in REGIONS.items():
        active = code in selected
        fig.add_trace(go.Scatter(x=[x],y=[y],mode="markers+text",text=[code],
            textposition="top center",textfont=dict(size=11),
            marker=dict(size=19 if active else 10,color="#158675" if active else "#a8b3c5"),
            hovertemplate=f"<b>{name}</b><br>{detail}<extra></extra>",showlegend=False))
    fig.update_layout(height=330, xaxis=dict(visible=False,range=[-5,115]),
                      yaxis=dict(visible=False,range=[10,100],scaleanchor="x"))
    return fig

def reset():
    for key in list(st.session_state):
        if key.startswith("nd_"):
            del st.session_state[key]

st.session_state.setdefault("nd_answers", [])
st.session_state.setdefault("nd_started", False)
answers = st.session_state.nd_answers

st.markdown("""<div class="hero"><div class="eyebrow">LABORATORIO DE DECISIONES</div>
<h1>Decidir.</h1><p>Cinco elecciones cotidianas. Explorá cómo el riesgo, el tiempo
y el contexto cambian lo que valoramos.</p></div>""", unsafe_allow_html=True)

if not st.session_state.nd_started:
    a,b,c = st.columns(3)
    a.metric("Escenarios", "5")
    b.metric("Duración orientativa", "3–5 min")
    c.metric("Respuestas correctas", "Sin puntaje")
    st.write("Elegí primero; al final descubrirás las conexiones con la investigación, un mapa cerebral y un simulador de preferencias.")
    st.info("Experiencia educativa. No mide actividad cerebral, no diagnostica ni construye un perfil psicológico validado. Las fichas y los pagos son hipotéticos.")
    st.caption("La app mantiene las respuestas en la sesión; no implementa una base de datos ni un registro de participantes.")
    if st.button("Comenzar la experiencia →", type="primary"):
        st.session_state.nd_started = True
        st.rerun()
    st.stop()

if len(answers) < len(TASKS):
    i = len(answers)
    task = TASKS[i]
    st.progress(i / len(TASKS), text=f"Escenario {i+1} de 5")
    with st.container(border=True):
        st.caption(task["tag"])
        st.header(task["title"])
        st.write(task["text"])
        choice = st.radio("¿Qué elegís?", task["options"], index=None, key=f"nd_q{i}")
        if st.button("Ver mis resultados →" if i == 4 else "Confirmar y continuar →",
                     type="primary", disabled=choice is None):
            answers.append(task["options"].index(choice))
            st.rerun()
    st.button("Reiniciar", on_click=reset)
    st.stop()

st.header("Tus decisiones, bajo la lupa")
st.caption("Descripciones de esta sesión. No son rasgos de personalidad ni mediciones neuronales.")
changed = answers[0] != answers[3]
a,b,c = st.columns(3)
a.metric("Recorrido", "5 / 5")
b.metric("Elección ante el encuadre", "Cambió" if changed else "Se mantuvo")
c.metric("Recompensa elegida", "Hoy" if answers[1] == 0 else "En 30 días")
if changed:
    st.info("Cambiaste entre las rondas 1 y 4, aunque ofrecían los mismos resultados. Es compatible con sensibilidad al encuadre, pero dos respuestas no establecen la causa del cambio.")
else:
    st.info("Mantuviste la elección entre las rondas 1 y 4. Eso describe este par de respuestas; no prueba que seas inmune al encuadre.")
st.caption("El orden fijo, recordar la primera pregunta y usar premios hipotéticos limitan la comparación con un experimento.")

tab1,tab2,tab3,tab4 = st.tabs(["Tu recorrido", "Datos del estudio", "Mapa cerebral", "Simulador"])
with tab1:
    for i, task in enumerate(TASKS):
        with st.expander(f"{i+1}. {task['title']}", expanded=i == 0):
            st.markdown(f"**Tu elección:** {task['options'][answers[i]]}")
            st.write(task["readings"][answers[i]])
            st.info(task["lesson"])
            st.markdown("**¿Qué observó la neurociencia?**")
            st.write(task["neuro"])
            label,url = SOURCES[task["source"]]
            st.markdown(f"Fuente: [{label}]({url})")

with tab2:
    st.subheader("El mismo problema puede sentirse diferente")
    st.write("De Martino et al. (2006): 20 participantes en una tarea monetaria con múltiples ensayos. Porcentaje medio de elecciones de la alternativa arriesgada en cada encuadre:")
    fig = go.Figure(go.Bar(x=["Encuadre de ganancia", "Encuadre de pérdida"],
        y=[42.9,61.6],text=["42,9%","61,6%"],textposition="outside",
        marker_color=["#158675", "#df8e44"],hovertemplate="%{x}: %{y:.1f}%<extra></extra>"))
    fig.update_layout(height=330,yaxis=dict(range=[0,100],title="Elecciones arriesgadas (%)"))
    chart(fig,"empirical")
    st.metric("Diferencia entre condiciones", "+18,7 puntos porcentuales")
    st.caption("Datos publicados, no datos de visitantes. Son promedios de elecciones a través de ensayos, no porcentajes de personas con un rasgo. No representan la probabilidad de tu próxima elección.")
    st.write("Nuestras rondas 1 y 4 son adaptaciones: los porcentajes abarcan las condiciones del estudio, no este único par de preguntas. Para las otras rondas no asignamos porcentajes sin datos comparables.")
    st.markdown(f"[Consultar el estudio original]({SOURCES['frame'][1]})")

with tab3:
    st.subheader("Una decisión involucra redes")
    focus = st.selectbox("Explorá un escenario", range(5), format_func=lambda i: TASKS[i]["title"])
    task = TASKS[focus]
    chart(brain(task["regions"]), "brain")
    st.caption("Render esquemático original: frente a la izquierda. Superpone regiones laterales, mediales y profundas. Ubicaciones aproximadas; no es un atlas, una resonancia ni un mapa de tu activación. Verde = regiones comentadas en la investigación seleccionada.")
    for code in task["regions"]:
        st.markdown(f"**{code} · {REGIONS[code][2]}:** {REGIONS[code][3]}")
    st.write(task["neuro"])
    st.info("La fMRI registra cambios hemodinámicos asociados a actividad neural. Una elección en esta app no permite inferir esa señal. Las regiones participan en múltiples funciones.")
    st.markdown("**Neuroimágenes reales en las publicaciones**")
    st.markdown("[Figuras de fMRI sobre encuadre](https://pmc.ncbi.nlm.nih.gov/articles/PMC2631940/#F2) · "
                "[Figuras de fMRI sobre valor subjetivo](https://pmc.ncbi.nlm.nih.gov/articles/PMC2845395/#F3)")

with tab4:
    st.subheader("¿Qué cambia cuando esperar cuesta más?")
    st.write("Modelo educativo de la ronda 2. Mové los parámetros para explorar probabilidades generadas por un modelo, no medidas en participantes.")
    k = st.slider("Descuento por día (k): mayor valor = más costo de esperar", 0.0,0.08,0.015,0.001)
    beta = st.slider("Sensibilidad a la diferencia de valor (β)",0.01,0.30,0.08,0.01)
    days = list(range(91))
    values = [140/(1+k*d) for d in days]
    probs = [100/(1+math.exp(-beta*(v-100))) for v in values]
    fig = go.Figure(go.Scatter(x=days,y=probs,mode="lines",
                              line=dict(color="#158675",width=3)))
    fig.add_vline(x=30,line_dash="dot",line_color="#df8e44")
    fig.update_layout(height=330,xaxis_title="Días de espera por 140 unidades",
                      yaxis=dict(title="P de elegir 140 después · modelo (%)",range=[0,100]))
    chart(fig,"model")
    a,b = st.columns(2)
    a.metric("Modelo: elegir 140 en 30 días", f"{probs[30]:.1f}%")
    b.metric("Modelo: elegir 100 hoy", f"{100-probs[30]:.1f}%")
    st.latex(r"V=\frac{140}{1+kD},\qquad P(\mathrm{esperar})=\frac{1}{1+e^{-\beta(V-100)}}")
    st.caption("D = días; k = descuento temporal; β = sensibilidad en unidades inversas de recompensa. β pequeño aproxima las probabilidades a 50%. Parámetros ilustrativos: no se ajustan a tus respuestas ni reproducen estimaciones de un artículo. Supone pagos garantizados y sin inflación.")

with st.expander("Fuentes y alcance científico"):
    for label,url in SOURCES.values():
        st.markdown(f"- [{label}]({url})")
    st.write("Las cinco preguntas adaptan paradigmas experimentales. No forman una escala validada. Las explicaciones neuronales remiten a asociaciones publicadas, no a mediciones del visitante. La simulación matemática es independiente de los porcentajes empíricos.")

report = {"tipo":"Registro educativo, no evaluación psicológica",
          "respuestas":[{"escenario":t["title"],"eleccion":t["options"][answers[i]]}
                        for i,t in enumerate(TASKS)],
          "fuentes":{label:url for label,url in SOURCES.values()}}
st.download_button("Descargar mis elecciones · JSON", json.dumps(report,ensure_ascii=False,indent=2),
                   file_name="mis_decisiones.json",mime="application/json")
st.button("Volver a empezar",on_click=reset)
