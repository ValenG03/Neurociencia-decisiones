import base64
import json
import mimetypes
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st
from PIL import Image


# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="🧠 Tu cerebro elige",
    page_icon="🧠",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent


# =========================================================
# DISEÑO
# =========================================================

st.html("""
<style>
.stApp {
    background:
        radial-gradient(ellipse at 90% 0%, #dff4ff, transparent 45%),
        #f5f8fd;
    color: #17233b;
    color-scheme: light;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1120px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #17233b !important;
    letter-spacing: -.035em;
}

.stApp [data-testid="stMarkdownContainer"],
.stApp label {
    color: #17233b;
}

.hero {
    text-align: center;
    position: relative;
    overflow: hidden;
    background: linear-gradient(
        120deg,
        #102a48,
        #125681 65%,
        #087aa0
    );
    padding: 42px;
    border-radius: 28px;
    color: white;
    margin-bottom: 26px;
    box-shadow: 0 18px 50px #1a6c9c24;
    animation: reveal .65s ease-out;
}

.hero:after {
    content: "";
    position: absolute;
    width: 280px;
    height: 280px;
    border: 1px solid #7dd3fc50;
    border-radius: 50%;
    right: -65px;
    top: -120px;
    box-shadow:
        0 0 0 35px #7dd3fc12,
        0 0 0 75px #7dd3fc09;
    pointer-events: none;
}

.hero h1 {
    color: white !important;
    text-align: center;
    font-size: clamp(2rem, 5vw, 3.5rem);
    margin: 14px 0;
    line-height: 1.15;
    position: relative;
    z-index: 1;
}

.hero p {
    color: #e0f2fe !important;
    text-align: center;
    font-size: 1.12rem;
    line-height: 1.65;
    max-width: 730px;
    margin: 18px auto;
    position: relative;
    z-index: 1;
}

.eyebrow {
    text-align: center;
    font-size: 11px;
    letter-spacing: 2.6px;
    font-weight: 700;
    color: #a5e6ff;
    position: relative;
    z-index: 1;
}

.hero-tags {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 20px;
    position: relative;
    z-index: 1;
}

.pill {
    display: inline-block;
    border: 1px solid #a5e6ff55;
    background: #ffffff10;
    border-radius: 30px;
    padding: 6px 13px;
    font-size: 12px;
    color: #e0f2fe;
    text-align: center;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 18px;
}

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #fff, #e9f5ff);
    border: 1px solid #d8e9f6;
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0 5px 20px #102a4808;
    transition: transform .2s, box-shadow .2s;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 9px 22px #102a4812;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricValue"] {
    color: #17233b;
}

div.stButton > button,
div.stDownloadButton > button {
    border-radius: 12px;
    min-height: 46px;
    transition: transform .18s, box-shadow .18s;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(100deg, #087db0, #2463bb);
    border: 0;
    color: white;
    box-shadow: 0 5px 16px #168dc326;
}

div.stButton > button:not(:disabled):hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px #168dc32b;
}

button:focus-visible,
a:focus-visible {
    outline: 3px solid #38bdf8 !important;
    outline-offset: 3px;
}

[data-baseweb="tab-list"] {
    gap: 10px;
    flex-wrap: wrap;
    height: auto;
}

[data-baseweb="tab"] {
    background: #e9f3fc;
    border-radius: 12px;
    padding: 10px 15px;
    color: #245779;
}

[data-baseweb="tab"][aria-selected="true"] {
    background: #ccecff;
    color: #064d78;
    font-weight: 700;
}

[data-testid="stExpander"] {
    background: #ffffff;
    border-radius: 16px;
}

[data-testid="stRadio"] {
    background: #ffffff;
    padding: 14px;
    border-radius: 14px;
    border: 1px solid #d8e9f6;
}

.recap {
    background: #eef7ff;
    border-left: 4px solid #38bdf8;
    padding: 18px 22px;
    border-radius: 0 16px 16px 0;
    margin: 12px 0 20px;
    color: #17233b;
    line-height: 1.75;
}

.edu-banner {
    background: linear-gradient(100deg, #dff3ff, #edf0ff);
    padding: 24px;
    border-radius: 18px;
    margin-bottom: 20px;
    color: #17395b;
}

.edu-banner h2 {
    margin-top: 0;
}

.repo-image {
    display: flex;
    justify-content: center;
    width: 100%;
    margin: 24px 0 30px;
}

.repo-image img {
    display: block;
    max-width: 100%;
    height: auto;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(23, 35, 59, .10);
}

@keyframes reveal {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *:before, *:after {
        animation: none !important;
        transition: none !important;
        transform: none !important;
    }
}

@media (max-width: 640px) {
    .hero {
        padding: 25px 20px;
    }

    .block-container {
        padding-top: 1rem;
    }

    .pill {
        font-size: 11px;
    }

    [data-baseweb="tab"] {
        padding: 8px 10px;
    }
}
</style>
""")


# =========================================================
# FUENTES
# =========================================================

SOURCES = {
    "frame": (
        "De Martino et al. (2006) · Encuadre y decisión",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC2631940/",
    ),
    "time": (
        "Kable y Glimcher (2007) · Valor subjetivo y espera",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC2845395/",
    ),
    "social": (
        "Sanfey et al. (2003) · Juego del ultimátum",
        "https://pubmed.ncbi.nlm.nih.gov/12805551/",
    ),
    "loss": (
        "Tom et al. (2007) · Ganancias y pérdidas",
        "https://pubmed.ncbi.nlm.nih.gov/17255512/",
    ),
}


# =========================================================
# ESCENARIOS
# =========================================================

TASKS = [
    {
        "title": "Un regalo con dos caminos",
        "tag": "01 · Elegir",
        "text": (
            "Recibís 100 fichas. Elegí cómo terminar esta "
            "ronda independiente."
        ),
        "options": [
            "Conservar 40 fichas con certeza.",
            "40% de terminar con 100 fichas; 60% de terminar con 0.",
        ],
        "lesson": (
            "Ambas opciones tienen valor esperado de 40 fichas. "
            "Igual promedio no significa igual riesgo ni igual "
            "atractivo personal."
        ),
        "neuro": (
            "En una tarea de encuadre monetario, De Martino y "
            "colegas observaron una asociación entre actividad "
            "de la amígdala y elecciones sensibles al encuadre."
        ),
        "regions": ["AMY"],
        "source": "frame",
    },
    {
        "title": "Ahora o después",
        "tag": "02 · Esperar",
        "text": (
            "Podés recibir un premio hoy o dentro de 30 días. "
            "Suponé que el pago está garantizado, que el poder "
            "de compra no cambia y que no hay intereses ni costos."
        ),
        "options": [
            "Recibir 100 unidades hoy.",
            "Recibir 140 unidades en 30 días.",
        ],
        "lesson": (
            "Una elección aislada no estima tu impulsividad "
            "ni tu tasa de descuento. Necesitaríamos muchas "
            "combinaciones de montos y plazos."
        ),
        "neuro": (
            "Kable y Glimcher encontraron correlaciones entre "
            "valor subjetivo y señal de fMRI en corteza "
            "prefrontal medial, estriado ventral y corteza "
            "cingulada posterior."
        ),
        "regions": ["MPFC", "VS", "PCC"],
        "source": "time",
    },
    {
        "title": "Un reparto desigual",
        "tag": "03 · Negociar",
        "text": (
            "Una persona desconocida reparte 10 fichas: se queda "
            "con 8 y te ofrece 2. Es una única interacción, sin "
            "reputación ni negociaciones futuras. Si rechazás, "
            "ambos reciben 0."
        ),
        "options": [
            "Aceptar: recibo 2 y la otra persona recibe 8.",
            "Rechazar: ambos recibimos 0.",
        ],
        "lesson": (
            "Aceptar maximiza tu pago en esta ronda; rechazar "
            "puede expresar rechazo a la desigualdad. La "
            "elección no mide tu moralidad."
        ),
        "neuro": (
            "Sanfey y colegas observaron respuestas a ofertas "
            "injustas en ínsula anterior y corteza prefrontal "
            "dorsolateral. Es una asociación grupal, no un "
            "detector de injusticia individual."
        ),
        "regions": ["AI", "DLPFC"],
        "source": "social",
    },
    {
        "title": "Evitar una pérdida",
        "tag": "04 · Resolver",
        "text": (
            "En una nueva ronda tenés 100 fichas. Debés "
            "elegir entre estas alternativas."
        ),
        "options": [
            "Perder 60 fichas con certeza.",
            "40% de no perder ninguna; 60% de perder las 100.",
        ],
        "lesson": (
            "Los resultados posibles son idénticos a los del "
            "escenario 1: 40 seguras o 40% de obtener 100. "
            "Cambió la manera de describirlos."
        ),
        "neuro": (
            "La evidencia sobre encuadre vincula contexto "
            "y valoración. No permite afirmar que una región "
            "controló tu elección ni dividir tu cerebro "
            "en racional y emocional."
        ),
        "regions": ["AMY"],
        "source": "frame",
    },
    {
        "title": "¿Aceptarías la apuesta?",
        "tag": "05 · Arriesgar",
        "text": (
            "Esta apuesta es independiente de las rondas "
            "anteriores. Podés afrontar la pérdida y no "
            "hay costos adicionales."
        ),
        "options": [
            "Aceptar: 50% de ganar 150 fichas y 50% de perder 100.",
            "Rechazar: no gano ni pierdo fichas.",
        ],
        "lesson": (
            "El valor esperado es +25 fichas. Rechazar no "
            "demuestra por sí solo aversión a las pérdidas: "
            "también puede influir la aversión al riesgo."
        ),
        "neuro": (
            "Tom y colegas relacionaron diferencias en "
            "sensibilidad a ganancias y pérdidas con respuestas "
            "en estriado ventral y corteza prefrontal durante "
            "apuestas monetarias."
        ),
        "regions": ["VS", "PFC"],
        "source": "loss",
    },
]


INTERPRETATIONS = [
    [
        (
            "Al conservar 40 fichas, priorizaste la certeza "
            "frente a la posibilidad de obtener una recompensa "
            "mayor. En esta situación aceptaste renunciar a "
            "la oportunidad de llegar a 100 para evitar terminar "
            "en cero. Eso describe una preferencia por la opción "
            "segura en esta ronda, no una personalidad "
            "necesariamente conservadora."
        ),
        (
            "Al elegir la alternativa incierta, aceptaste "
            "la posibilidad de terminar en cero a cambio de "
            "una oportunidad de obtener 100 fichas. En esta "
            "ronda preferiste esa distribución de resultados "
            "a recibir 40 con certeza. No podemos saber si "
            "te atrajo la ganancia máxima, la experiencia "
            "de apostar u otro aspecto."
        ),
    ],
    [
        (
            "Al elegir 100 hoy, le diste más peso a disponer "
            "de la recompensa inmediatamente que al aumento "
            "de 40 unidades por esperar. Ese intercambio puede "
            "entenderse mediante el descuento temporal: una "
            "recompensa futura puede valer subjetivamente menos "
            "por la demora. No significa que el futuro no te "
            "importe; el costo de esperar depende también "
            "de tus necesidades."
        ),
        (
            "Al elegir 140 en 30 días, priorizaste el monto "
            "mayor frente a la disponibilidad inmediata de "
            "100. Bajo los supuestos de pago garantizado "
            "y poder de compra estable, aceptaste el costo "
            "de esperar por un beneficio adicional. Esto no "
            "permite afirmar que siempre seas paciente: "
            "otra demora u otro monto podrían cambiar "
            "tu elección."
        ),
    ],
    [
        (
            "Al aceptar el reparto, priorizaste obtener las "
            "2 fichas disponibles frente a rechazar la propuesta "
            "y recibir cero. Esto no implica que la desigualdad "
            "te resulte indiferente: podés considerarla injusta "
            "y, aun así, preferir conservar el beneficio "
            "económico en una interacción sin consecuencias "
            "futuras."
        ),
        (
            "Al rechazar, renunciaste a 2 fichas e impediste "
            "que la otra persona recibiera 8. Una interpretación "
            "posible es que evitar ese reparto desigual tuvo "
            "más peso que tu beneficio inmediato. Sin embargo, "
            "la respuesta por sí sola no distingue entre una "
            "norma de justicia, enojo u otros motivos."
        ),
    ],
    [
        (
            "Al aceptar perder 60 fichas, aseguraste conservar "
            "40 y descartaste el riesgo de perderlas todas. "
            "En esta ronda preferiste limitar la incertidumbre, "
            "aun renunciando a la posibilidad de conservar "
            "las 100. Lo interesante aparece al comparar "
            "esta elección con la primera pregunta."
        ),
        (
            "Al elegir la apuesta, aceptaste el riesgo "
            "de perder las 100 fichas para mantener la "
            "posibilidad de no perder ninguna. Describir "
            "el problema como una pérdida puede cambiar "
            "su atractivo, aunque el resultado económico "
            "sea equivalente al de una formulación como "
            "ganancia. Tu respuesta aislada no demuestra "
            "que el encuadre haya sido la causa."
        ),
    ],
    [
        (
            "Al aceptar, consideraste suficientemente "
            "atractiva la posibilidad de ganar 150 como "
            "para afrontar una pérdida posible de 100. "
            "El promedio matemático es favorable, pero "
            "no garantiza una ganancia en una única ronda. "
            "Tu decisión es compatible con aceptar este "
            "riesgo concreto; no implica que ignores "
            "las pérdidas."
        ),
        (
            "Al rechazar, priorizaste mantener tu saldo "
            "frente a una apuesta que podía aumentarlo "
            "o reducirlo. Aunque el promedio matemático "
            "es positivo, puede que evitar la pérdida "
            "potencial o la incertidumbre haya pesado "
            "más para vos. No podemos separar esos "
            "motivos con una sola respuesta."
        ),
    ],
]


BRIDGES = [
    (
        "El estudio comparó elecciones monetarias bajo "
        "descripciones de ganancia y de pérdida, junto "
        "con registros de fMRI."
    ),
    (
        "Los autores estudiaron elecciones entre recompensas "
        "inmediatas y demoradas, relacionando su valor "
        "subjetivo con señales cerebrales."
    ),
    (
        "Los autores utilizaron el juego del ultimátum: "
        "aceptar una oferta permite cobrarla; rechazarla "
        "deja a ambas partes sin pago."
    ),
    (
        "La manipulación central fue cambiar la descripción "
        "manteniendo equivalentes los resultados económicos "
        "de las opciones."
    ),
    (
        "El estudio presentó apuestas con probabilidades "
        "iguales de ganar o perder y distintos montos, "
        "en lugar de inferir una característica a partir "
        "de una única apuesta."
    ),
]


# =========================================================
# EDUCACIÓN
# =========================================================

CHAPTERS = {
    "🧠 Los 6 lóbulos cerebrales": """
Aquí usamos una **descripción de seis lóbulos** que incluye la ínsula y el lóbulo límbico. Es una organización anatómica útil, pero el número puede variar según el criterio del manual; no es una lista universal de seis compartimentos funcionales independientes.

**Frontal.** Está en la parte anterior. Sus regiones intervienen en movimiento voluntario, planificación, control de la conducta y lenguaje. La corteza prefrontal participa en decisiones junto con otras estructuras.

**Parietal.** En la zona superior y posterior al frontal, integra información corporal y espacial. Ayuda a localizar sensaciones y orientar la atención y la acción.

**Temporal.** Se extiende por los laterales inferiores. Participa en audición, lenguaje, reconocimiento y memoria; en su región medial se encuentra la formación hipocampal.

**Occipital.** Situado atrás, está especializado principalmente en procesamiento visual. La visión implica múltiples operaciones y conexiones con otros lóbulos.

**Ínsula.** Está oculta en profundidad dentro del surco lateral. Participa en gusto, percepción del estado corporal y procesamiento de señales relevantes, entre otras funciones.

**Límbico.** Comprende regiones de la cara medial, como los giros cingulado y parahipocampal, vinculadas con memoria, motivación y emoción. No equivale a todo el sistema límbico, que también incluye estructuras profundas.

[Anatomía de la corteza · NCBI Bookshelf](https://www.ncbi.nlm.nih.gov/books/NBK575742/)
""",

    "🌐 Áreas funcionales principales": """
Una distinción introductoria agrupa áreas **motoras, sensitivas y de asociación**. Estas áreas trabajan de manera coordinada.

Las **áreas motoras** participan en preparar y ejecutar movimientos; la corteza motora primaria es una de ellas.

Las **áreas sensitivas** procesan información visual, auditiva y corporal, entre otras modalidades.

Las **áreas de asociación** integran información con recuerdos, metas y contexto para guiar la conducta.

En una decisión, estas operaciones se combinan: percibís las opciones, interpretás su significado, valorás consecuencias y ejecutás una respuesta. No existe un único “botón cerebral” para decidir.

[Organización y funciones del encéfalo · National Academies](https://www.ncbi.nlm.nih.gov/books/NBK234157/)
""",

    "🏛️ Grandes estructuras del encéfalo": """
El **encéfalo** es el conjunto de estructuras dentro del cráneo. El sistema nervioso central incluye también la médula espinal. Podemos distinguir cuatro grandes conjuntos anatómicos.

El **telencéfalo** comprende los hemisferios, su corteza, la sustancia blanca y núcleos profundos.

El **diencéfalo** incluye el tálamo y el hipotálamo. Junto con el telencéfalo forma parte del prosencéfalo.

El **cerebelo**, situado detrás del tronco y debajo de regiones posteriores de los hemisferios, participa en coordinación, equilibrio y aprendizaje motor, además de contribuir a funciones cognitivas. No es sinónimo de cerebro posterior: el rombencéfalo incluye también el puente y el bulbo.

El **tronco encefálico** comprende mesencéfalo, puente y bulbo. Comunica distintas partes del sistema nervioso y participa en vigilia, movimientos y regulación de funciones vitales.

[Introducción al encéfalo · NINDS](https://www.ninds.nih.gov/health-information/public-education/brain-basics)
""",

    "🔎 Estructuras internas profundas": """
**Amígdala.** Hay un complejo amigdalino en cada hemisferio, en el temporal medial. Interviene en aprendizaje y valoración de estímulos relevantes, incluidas amenazas y recompensas; no es exclusivamente un centro del miedo.

**Hipocampo.** Participa en formar y consolidar recuerdos declarativos y en navegación espacial. No almacena por sí solo toda la memoria a largo plazo.

**Ganglios basales.** Son un conjunto de núcleos que incluye caudado, putamen y globo pálido. Sus circuitos participan en selección de acciones, movimiento, aprendizaje y hábitos.

**Tálamo.** Interviene en circuitos sensoriales, motores y cognitivos. Gran parte de la información sensorial hace relevo allí antes de llegar a corteza; la vía olfatoria inicial es una excepción, aunque existen conexiones olfativas posteriores con el tálamo.

**Hipotálamo.** Participa en regulación hormonal, temperatura, hambre, sed y ritmos de sueño y vigilia.

**Mesencéfalo.** Participa en movimientos oculares, orientación a estímulos y circuitos motores y de vigilia.

**Puente o protuberancia.** Conecta circuitos corticales y cerebelosos e interviene en sueño y respiración.

**Bulbo raquídeo.** Contiene circuitos importantes para regulación respiratoria y cardiovascular, además de reflejos como la deglución. Estas funciones se coordinan con otras regiones.

[Grandes estructuras y funciones · National Academies](https://www.ncbi.nlm.nih.gov/books/NBK234157/) · [Circuitos talamocorticales · NCBI](https://www.ncbi.nlm.nih.gov/books/NBK546699/)
""",

    "🗣️ Lenguaje y áreas corticales": """
Las denominaciones **Broca** y **Wernicke** son referencias históricas útiles, pero el lenguaje depende de una red distribuida.

El **área de Broca**, generalmente en el frontal inferior izquierdo, participa en operaciones de producción y procesamiento del lenguaje.

La **región clásica de Wernicke** se ubica en el temporal superior posterior del hemisferio dominante; comprender lenguaje requiere también otras regiones temporales, parietales y frontales.

La **corteza prefrontal** contribuye a mantener metas, planificar, evaluar opciones y regular la conducta. El caso de Phineas Gage es históricamente importante, pero no demuestra que la personalidad resida en un solo punto.

La **corteza motora primaria**, en el giro precentral del frontal, contribuye al control del movimiento voluntario. Su representación corporal suele ilustrarse con el homúnculo motor: no es un mapa literal ni inmutable.

La **corteza somatosensorial primaria**, en el giro postcentral del parietal, procesa especialmente tacto y posición corporal. Dolor y temperatura dependen de circuitos distribuidos que incluyen otras áreas.

La **corteza visual primaria o V1**, alrededor del surco calcarino en el occipital, recibe información a través del relevo talámico y participa en el análisis visual inicial. Su daño puede producir pérdida de visión en sectores del campo visual; lesiones extensas bilaterales pueden causar ceguera cortical.

La **corteza auditiva primaria**, en la superficie temporal superior, procesa propiedades del sonido, como su frecuencia. La audición depende también de vías subcorticales y otras áreas.

[Red del lenguaje · Li et al.](https://arxiv.org/abs/1906.07546) · [Corteza auditiva · Neuroscience](https://www.ncbi.nlm.nih.gov/books/NBK10900/) · [Vías visuales · Neuroscience](https://www.ncbi.nlm.nih.gov/books/NBK10909/)
""",

    "🧩 Conexiones y regiones especializadas": """
El **cuerpo calloso** es un gran haz de sustancia blanca que comunica los hemisferios. No es corteza ni la única conexión entre ambos, y la transmisión neural lleva tiempo: no es instantánea.

La **corteza cingulada**, alrededor del cuerpo calloso, contiene subregiones con funciones distintas. Algunas participan en monitoreo de la conducta y procesamiento afectivo; otras se relacionan con memoria y cognición interna.

La **corteza orbitofrontal**, sobre las órbitas, participa en representar y actualizar el valor de posibles resultados. Colabora con otros circuitos para adaptar decisiones; no es un centro único de riesgo, recompensa o inhibición social.

Las **regiones fusiformes selectivas para caras**, en la superficie ventral occipitotemporal, participan en percepción de rostros dentro de una red más amplia. La selectividad no implica exclusividad absoluta. Lesiones de esa red pueden causar prosopagnosia; no toda lesión fusiforme produce necesariamente ese cuadro.

[Estimulación fusiforme y percepción de caras · Parvizi et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC3517886/) · [Valoración y redes cerebrales · Kable y Glimcher](https://pmc.ncbi.nlm.nih.gov/articles/PMC2845395/)
""",

    "🗺️ Resumen General de Divisiones": """
Con esto, los mapas cerebrales cubren las siguientes divisiones:

1. Los **6 Lóbulos** externos e internos.
2. Las **8 Estructuras Internas Profundas** (amígdala, hipocampo, ganglios basales y estructuras del diencéfalo y del tronco encefálico).
3. Las **7 Áreas Corticales Famosas** (Broca, Wernicke, prefrontal, motoras y sensoriales).
4. El **Cuerpo Calloso** y los giros de asociación especializada.
""",
}


# =========================================================
# REGIONES DEL MAPA ESQUEMÁTICO
# =========================================================

REGIONS = {
    "AMY": (
        43, 32,
        "Amígdala",
        "Región profunda; asociación con encuadre en el estudio citado.",
    ),
    "MPFC": (
        22, 51,
        "Prefrontal medial",
        "Cara medial; asociación con valor subjetivo.",
    ),
    "VS": (
        38, 43,
        "Estriado ventral",
        "Región profunda; valoración de recompensas y pérdidas.",
    ),
    "PCC": (
        65, 61,
        "Cingulada posterior",
        "Cara medial; asociación con valor subjetivo.",
    ),
    "AI": (
        34, 48,
        "Ínsula anterior",
        "Oculta bajo la corteza lateral; respuesta a ofertas injustas.",
    ),
    "DLPFC": (
        28, 73,
        "Prefrontal dorsolateral",
        "Superficie lateral; respuesta en la tarea de ultimátum.",
    ),
    "PFC": (
        16, 60,
        "Corteza prefrontal",
        "Etiqueta amplia; incluye subregiones, no un foco específico.",
    ),
}


# =========================================================
# FUNCIONES
# =========================================================

def show_repo_image(filename):
    image_path = BASE_DIR / filename

    if not image_path.is_file():
        st.warning(
            f"No se encontró la imagen {filename}. "
            "Agregala en la misma carpeta que app.py."
        )
        return

    max_width = (
        440 if "brodmann" in filename.lower() else 760
    )

    try:
        # Se leen las dimensiones sin modificar la imagen.
        with Image.open(image_path) as original:
            native_width = original.width
            detected_mime = Image.MIME.get(original.format)

        # No amplía imágenes por encima de su ancho original.
        display_width = min(max_width, native_width)

        mime_type = (
            detected_mime
            or mimetypes.guess_type(image_path.name)[0]
            or "image/jpeg"
        )

        # Conserva los bytes originales sin compresión adicional.
        encoded_image = base64.b64encode(
            image_path.read_bytes()
        ).decode("ascii")

        alt_text = (
            "Mapa de áreas de Brodmann"
            if "brodmann" in filename.lower()
            else "Ilustración anatómica del cerebro"
        )

        st.html(f"""
        <div class="repo-image">
            <img
                src="data:{mime_type};base64,{encoded_image}"
                alt="{alt_text}"
                style="width:{display_width}px;"
            >
        </div>
        """)

    except (OSError, ValueError):
        st.warning(
            f"No se pudo abrir {filename}. "
            "Comprobá que sea un archivo de imagen válido."
        )


def chart(fig, key):
    fig.update_layout(
        template="plotly_white",
        font=dict(color="#17233b"),
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=35, b=25),
    )

    st.plotly_chart(
        fig,
        width="stretch",
        key=key,
        config={"displayModeBar": False},
    )


def brain(selected):
    fig = go.Figure()

    fig.add_shape(
        type="path",
        path=(
            "M 10,42 "
            "C 0,57 10,77 25,82 "
            "C 37,95 65,93 80,82 "
            "C 100,80 109,58 99,42 "
            "C 94,29 75,23 60,28 "
            "C 42,15 23,25 10,42 Z"
        ),
        fillcolor="#e2e8f2",
        line=dict(color="#9faec5", width=2),
    )

    for path in [
        "M 24,73 Q 42,82 58,72",
        "M 58,72 Q 82,80 94,61",
        "M 18,56 Q 37,65 48,54",
        "M 55,54 Q 78,63 94,49",
    ]:
        fig.add_shape(
            type="path",
            path=path,
            line=dict(color="#bfcbdd", width=2),
        )

    for code, (x, y, name, detail) in REGIONS.items():
        active = code in selected

        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode="markers+text",
            text=[code],
            textposition="top center",
            textfont=dict(size=11),
            marker=dict(
                size=19 if active else 10,
                color="#158675" if active else "#a8b3c5",
            ),
            hovertemplate=(
                f"<b>{name}</b><br>{detail}<extra></extra>"
            ),
            showlegend=False,
        ))

    fig.update_layout(
        height=330,
        xaxis=dict(
            visible=False,
            range=[-5, 115],
        ),
        yaxis=dict(
            visible=False,
            range=[10, 100],
            scaleanchor="x",
        ),
    )

    return fig


def reset():
    for key in list(st.session_state):
        if key.startswith("nd_"):
            del st.session_state[key]


# =========================================================
# ESTADO DE LA SESIÓN
# =========================================================

st.session_state.setdefault("nd_answers", [])
st.session_state.setdefault("nd_started", False)

answers = st.session_state.nd_answers


# =========================================================
# ENCABEZADO: HTML DIRECTO, SIN INTERPRETACIÓN MARKDOWN
# =========================================================

st.html("""
<div class="hero">
    <div class="eyebrow">
        LABORATORIO DE DECISIONES
    </div>

    <h1>🧠 Tu cerebro elige</h1>

    <p>
        ¿Por qué elegís lo que elegís? Entrá al laboratorio y
        explorá cómo el riesgo, el tiempo y el contexto influyen
        en tus decisiones.
    </p>

    <div class="hero-tags">
        <span class="pill">5 escenarios</span>
        <span class="pill">Ciencia + interacción</span>
        <span class="pill">Una nueva mirada sobre tus elecciones</span>
    </div>
</div>
""")


# =========================================================
# PANTALLA INICIAL
# =========================================================

if not st.session_state.nd_started:
    a, b, c = st.columns(3)

    a.metric("Escenarios", "5")
    b.metric("Duración orientativa", "3–5 min")
    c.metric("Respuestas correctas", "Sin puntaje")

    st.write(
        "Elegí primero; al final descubrirás las conexiones "
        "con la investigación, un mapa cerebral y una sección "
        "para aprender sobre sus partes."
    )

    st.info(
        "Experiencia educativa. No mide actividad cerebral, "
        "no diagnostica ni construye un perfil psicológico "
        "validado. Las fichas y los pagos son hipotéticos."
    )

    st.caption(
        "La app mantiene las respuestas en la sesión; "
        "no implementa una base de datos ni un registro "
        "de participantes."
    )

    if st.button(
        "Comenzar la experiencia →",
        type="primary",
    ):
        st.session_state.nd_started = True
        st.rerun()

    st.stop()


# =========================================================
# CINCO PREGUNTAS
# =========================================================

if len(answers) < len(TASKS):
    i = len(answers)
    task = TASKS[i]

    st.progress(
        i / len(TASKS),
        text=f"Escenario {i + 1} de 5",
    )

    with st.container(border=True):
        st.caption(task["tag"])
        st.header(task["title"])
        st.write(task["text"])

        choice = st.radio(
            "¿Qué elegís?",
            task["options"],
            index=None,
            key=f"nd_q{i}",
        )

        button_text = (
            "Ver mis resultados →"
            if i == len(TASKS) - 1
            else "Confirmar y continuar →"
        )

        if st.button(
            button_text,
            type="primary",
            disabled=choice is None,
        ):
            answers.append(
                task["options"].index(choice)
            )
            st.rerun()

    st.button(
        "Reiniciar",
        on_click=reset,
    )

    st.stop()


# =========================================================
# RESUMEN DE RESULTADOS
# =========================================================

st.header("Tus decisiones, bajo la lupa")

st.caption(
    "Descripciones de esta sesión. No son rasgos de "
    "personalidad ni mediciones neuronales."
)

changed = answers[0] != answers[3]

a, b, c = st.columns(3)

a.metric(
    "Recorrido",
    "5 / 5",
)

b.metric(
    "Elección ante el encuadre",
    "Cambió" if changed else "Se mantuvo",
)

c.metric(
    "Recompensa elegida",
    "Hoy" if answers[1] == 0 else "En 30 días",
)

if changed:
    st.info(
        "Cambiaste entre las rondas 1 y 4, aunque ofrecían "
        "los mismos resultados. Es compatible con sensibilidad "
        "al encuadre, pero dos respuestas no establecen "
        "la causa del cambio."
    )
else:
    st.info(
        "Mantuviste la elección entre las rondas 1 y 4. "
        "Eso describe este par de respuestas; no prueba "
        "que seas inmune al encuadre."
    )

show_repo_image("cerebro 2.jpg")


# =========================================================
# SECCIONES: SIN SIMULADOR
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "Tu recorrido",
    "Datos del estudio",
    "Mapa cerebral",
    "📚 Educación",
])


# =========================================================
# TU RECORRIDO
# =========================================================

with tab1:
    for i, task in enumerate(TASKS):
        with st.expander(
            f"{i + 1}. {task['title']}",
            expanded=i == 0,
        ):
            st.write(
                f"En la pregunta {i + 1}, la situación era "
                f"la siguiente: {task['text']}"
            )

            selected_letter = "AB"[answers[i]]
            selected_option = task["options"][answers[i]]

            st.html(
                '<div class="recap">'
                '<strong>Estas eran tus alternativas</strong><br>'
                f'<strong>Opción A:</strong> {task["options"][0]}<br>'
                f'<strong>Opción B:</strong> {task["options"][1]}'
                '<br><br>'
                f'<strong>Elegiste la opción {selected_letter}:</strong> '
                f'{selected_option}'
                '</div>'
            )

            st.write(
                INTERPRETATIONS[i][answers[i]]
            )

            st.write(
                task["lesson"]
            )

            label, url = SOURCES[task["source"]]

            st.markdown(
                "Para entender este tipo de decisión, "
                "podemos mirar la investigación de "
                f"**[{label}]({url})**. "
                f"{BRIDGES[i]} {task['neuro']}"
            )

            st.caption(
                "Esta interpretación se limita a la situación "
                "planteada: no identifica tus motivos con certeza "
                "ni mide qué regiones se activaron en vos."
            )


# =========================================================
# DATOS DEL ESTUDIO
# =========================================================

with tab2:
    st.subheader(
        "El mismo problema puede sentirse diferente"
    )

    st.write(
        "De Martino et al. (2006): 20 participantes en una "
        "tarea monetaria con múltiples ensayos. Porcentaje "
        "medio de elecciones de la alternativa arriesgada "
        "en cada encuadre:"
    )

    fig = go.Figure(go.Bar(
        x=[
            "Encuadre de ganancia",
            "Encuadre de pérdida",
        ],
        y=[42.9, 61.6],
        text=["42,9%", "61,6%"],
        textposition="outside",
        marker_color=[
            "#158675",
            "#df8e44",
        ],
        hovertemplate=(
            "%{x}: %{y:.1f}%<extra></extra>"
        ),
    ))

    fig.update_layout(
        height=330,
        yaxis=dict(
            range=[0, 100],
            title="Elecciones arriesgadas (%)",
        ),
    )

    chart(
        fig,
        "empirical",
    )

    st.metric(
        "Diferencia entre condiciones",
        "+18,7 puntos porcentuales",
    )

    st.caption(
        "Datos publicados, no datos de visitantes. Son "
        "promedios de elecciones a través de ensayos, "
        "no porcentajes de personas con un rasgo. No "
        "representan la probabilidad de tu próxima elección."
    )

    st.write(
        "Nuestras rondas 1 y 4 son adaptaciones: los porcentajes "
        "abarcan las condiciones del estudio, no este único "
        "par de preguntas. Para las otras rondas no asignamos "
        "porcentajes sin datos comparables."
    )

    st.markdown(
        "[Consultar el estudio original]"
        f"({SOURCES['frame'][1]})"
    )


# =========================================================
# MAPA CEREBRAL
# =========================================================

with tab3:
    st.subheader(
        "Una decisión involucra redes"
    )

    focus = st.selectbox(
        "Explorá un escenario",
        range(len(TASKS)),
        format_func=lambda i: TASKS[i]["title"],
    )

    task = TASKS[focus]

    chart(
        brain(task["regions"]),
        "brain",
    )

    st.caption(
        "Render esquemático original: frente a la izquierda. "
        "Superpone regiones laterales, mediales y profundas. "
        "Ubicaciones aproximadas; no es un atlas, una "
        "resonancia ni un mapa de tu activación. Verde = "
        "regiones comentadas en la investigación seleccionada."
    )

    for code in task["regions"]:
        st.markdown(
            f"**{code} · {REGIONS[code][2]}:** "
            f"{REGIONS[code][3]}"
        )

    st.write(
        task["neuro"]
    )

    st.info(
        "La fMRI registra cambios hemodinámicos asociados "
        "a actividad neural. Una elección en esta app no "
        "permite inferir esa señal. Las regiones participan "
        "en múltiples funciones."
    )

    st.markdown(
        "**Neuroimágenes reales en las publicaciones**"
    )

    st.markdown(
        "[Figuras de fMRI sobre encuadre]"
        "(https://pmc.ncbi.nlm.nih.gov/articles/PMC2631940/#F2)"
        " · "
        "[Figuras de fMRI sobre valor subjetivo]"
        "(https://pmc.ncbi.nlm.nih.gov/articles/PMC2845395/#F3)"
    )


# =========================================================
# EDUCACIÓN
# =========================================================

with tab4:
    st.html("""
    <div class="edu-banner">
        <h2>📚 Educación · Conocé las partes del cerebro</h2>
        <p>
            Un recorrido desde los lóbulos hasta las redes
            que permiten sentir, recordar, actuar y elegir.
        </p>
    </div>
    """)

    # Imagen centrada, de hasta 440 px, antes del selector.
    show_repo_image("areas-brodmann.jfif")

    chapter = st.selectbox(
        "¿Qué querés aprender?",
        list(CHAPTERS),
        key="nd_education",
    )

    with st.container(border=True):
        st.subheader(chapter)
        st.markdown(CHAPTERS[chapter])


# =========================================================
# FUENTES Y DESCARGA
# =========================================================

with st.expander(
    "Fuentes y alcance científico"
):
    for label, url in SOURCES.values():
        st.markdown(
            f"- [{label}]({url})"
        )

    st.write(
        "Las cinco preguntas adaptan paradigmas experimentales. "
        "No forman una escala validada. Las explicaciones "
        "neuronales remiten a asociaciones publicadas, "
        "no a mediciones del visitante."
    )


report = {
    "tipo": "Registro educativo, no evaluación psicológica",
    "respuestas": [
        {
            "escenario": task["title"],
            "eleccion": task["options"][answers[i]],
        }
        for i, task in enumerate(TASKS)
    ],
    "fuentes": {
        label: url
        for label, url in SOURCES.values()
    },
}


st.download_button(
    "Descargar mis elecciones · JSON",
    json.dumps(
        report,
        ensure_ascii=False,
        indent=2,
    ),
    file_name="mis_decisiones.json",
    mime="application/json",
)

st.button(
    "Volver a empezar",
    on_click=reset,
)
