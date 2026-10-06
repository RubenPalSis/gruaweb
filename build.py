#!/usr/bin/env python3
"""Genera la web estática de Asistencia 24H Barcelona.

Edita la CONFIGURACIÓN y ejecuta:  python3 build.py
Crea index.html, páginas de zona, páginas legales, 404, sitemap.xml, robots.txt y manifest.
"""
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import quote

# ---------------- CONFIGURACIÓN ----------------
SITE = "https://www.asistencia24hbarcelona.es"  # <- cambia por tu dominio real (sin / final)
NAME = "Asistencia 24H Barcelona"
PHONE_INTL = "+34671448639"
PHONE_TXT = "671 44 86 39"
PHONE_FULL = "+34 671 44 86 39"
WA_MSG = "Hola, necesito una grúa. Estoy en: "
OWNER = "Titular del servicio"  # nombre o razón social para el aviso legal
NIF = "[NIF/CIF]"
EMAIL = "[tu-email@dominio.es]"
GA4_ID = ""  # p.ej. "G-XXXXXXX" para Google Analytics (opcional)
GSC_VERIFY = ""  # código de verificación de Google Search Console (opcional)
# -----------------------------------------------

ROOT = Path(__file__).parent
TODAY = date.today().isoformat()


def wa(extra=""):
    return f"https://wa.me/{PHONE_INTL[1:]}?text={quote(WA_MSG + extra)}"


ICON = {
    "wa": '<svg viewBox="0 0 32 32" fill="currentColor" aria-hidden="true"><path d="M16 3C9 3 3.3 8.7 3.3 15.7c0 2.2.6 4.4 1.7 6.3L3 29l7.2-1.9c1.8 1 3.9 1.5 5.9 1.5 7 0 12.7-5.7 12.7-12.7S23 3 16 3zm0 23.3c-1.9 0-3.8-.5-5.4-1.5l-.4-.2-4.3 1.1 1.1-4.2-.3-.4a10.5 10.5 0 1 1 9.3 5.2zm5.8-7.9c-.3-.2-1.9-.9-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7.1a8.6 8.6 0 0 1-4.3-3.7c-.3-.6.3-.5.9-1.7.1-.2 0-.4 0-.5l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4s-1.2 1.1-1.2 2.8 1.2 3.2 1.4 3.5c.2.2 2.4 3.6 5.7 5 2.1.9 3 1 4 .8.7-.1 1.9-.8 2.2-1.5s.3-1.3.2-1.5c-.1-.1-.3-.2-.6-.4z"/></svg>',
    "tel": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8a15.2 15.2 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>',
}
SV = 'viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
SICON = {
    "grua": f'<svg {SV}><path d="M2 17h2m4 0h7m4 0h3v-5l-3-4h-4v9M15 8V5H9L3 13"/><circle cx="6" cy="17" r="2"/><circle cx="17" cy="17" r="2"/><path d="M9 5v4a1 1 0 1 1-1 1"/></svg>',
    "bat": f'<svg {SV}><rect x="2" y="7" width="18" height="12" rx="2"/><path d="M22 11v4M6 7V5m10 2V5M7 13h4m2 0h4m-2-2v4"/></svg>',
    "rueda": f'<svg {SV}><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/><path d="M12 3v6m0 6v6M3 12h6m6 0h6"/></svg>',
    "acc": f'<svg {SV}><path d="M12 9v4m0 4h.01M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/></svg>',
    "moto": f'<svg {SV}><circle cx="5" cy="17" r="3"/><circle cx="19" cy="17" r="3"/><path d="M8 17h6l3-6h-4l-2-4H8m6 4-3 6"/></svg>',
    "fuel": f'<svg {SV}><path d="M3 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18M3 22h12M6 7h6m3 3h2a2 2 0 0 1 2 2v5a1.5 1.5 0 0 0 3 0V9l-3-3"/></svg>',
    "llave": f'<svg {SV}><path d="M14.7 6.3a4 4 0 0 0 5 5L21 12.6 12.6 21a2.1 2.1 0 0 1-3-3L18 9.6l-1.3-1.3a4 4 0 0 0-2-2z"/><path d="m3 21 6-6"/></svg>',
    "km": f'<svg {SV}><path d="M3 12h18M3 12l4-4m-4 4 4 4M21 12l-4-4m4 4-4 4"/></svg>',
    "baja": f'<svg {SV}><path d="M3 6h18M8 6V4h8v2m-9 0 1 14h8l1-14"/></svg>',
}

SERVICES = [  # (icono, nombre, descripción corta, página propia o None)
    ("grua", "Remolque de coches averiados", "Llevamos tu vehículo al taller, concesionario o domicilio que elijas, con grúa de plataforma y sin dañar el coche.", "remolque-coches-barcelona"),
    ("acc", "Rescate tras accidente", "Retirada rápida de vehículos siniestrados en calles, rondas y autopistas. Te ayudamos a despejar la vía con seguridad.", "grua-accidente-barcelona"),
    ("bat", "Arranque de batería", "¿El coche no arranca? Arrancamos tu batería en el sitio o la sustituimos para que sigas tu camino.", "arranque-bateria-barcelona"),
    ("rueda", "Pinchazo y cambio de rueda", "Cambiamos la rueda pinchada en el momento. Si no tienes repuesto, trasladamos el vehículo al taller más cercano.", "cambio-rueda-pinchazo-barcelona"),
    ("fuel", "Falta de combustible", "Te quedaste sin gasolina o diésel: te llevamos combustible o el coche hasta la gasolinera.", None),
    ("moto", "Traslado de motos", "Transporte de motos y scooters con anclajes específicos, también por avería o accidente.", "grua-motos-barcelona"),
    ("km", "Traslados de larga distancia", "Transporte de vehículos dentro de Cataluña y a cualquier punto de España. Presupuesto cerrado.", "transporte-vehiculos-barcelona"),
    ("llave", "Traslados a ITV y taller", "Movemos coches sin ITV, sin batería o que no pueden circular, con total seguridad y legalidad.", None),
    ("baja", "Retirada para desguace", "Recogemos tu coche viejo o siniestrado y lo llevamos a un centro autorizado para darlo de baja.", "retirada-coches-desguace-barcelona"),
]

BCN_DISTRICTS = ["Ciutat Vella", "Eixample", "Sants-Montjuïc", "Les Corts", "Sarrià-Sant Gervasi", "Gràcia",
                 "Horta-Guinardó", "Nou Barris", "Sant Andreu", "Sant Martí", "Poblenou", "Zona Franca"]

ZONES = [
    dict(slug="grua-hospitalet-de-llobregat", name="L'Hospitalet de Llobregat",
         near="pegada a Barcelona: se llega en pocos minutos por la Gran Via o la Ronda Litoral",
         roads="la Gran Via, la Ronda Litoral, la B-10 y la C-31",
         places="Bellvitge, Collblanc, La Torrassa, Santa Eulàlia, Can Serra y la Fira Gran Via",
         intro="L'Hospitalet está pegada a Barcelona y una de las zonas con más tráfico del área metropolitana. Por eso tenemos grúa disponible para llegar en muy poco tiempo a cualquier barrio."),
    dict(slug="grua-badalona", name="Badalona",
         near="justo al norte de Barcelona, con acceso directo por la C-31 y la Ronda Litoral",
         roads="la C-31, la B-20 (Ronda de Dalt), la Ronda Litoral y la autopista C-32",
         places="el Centre, Llefià, Sant Roc, Montigalà, Pomar, Bufalà y el Port de Badalona",
         intro="Damos servicio de grúa y asistencia en carretera en todo Badalona, desde el puerto hasta los barrios altos, de día y de noche."),
    dict(slug="grua-cornella-de-llobregat", name="Cornellà de Llobregat",
         near="a un paso de Barcelona por la Ronda de Dalt y la B-23",
         roads="la B-23, la A-2, la Ronda de Dalt y la C-245",
         places="Almeda, Sant Ildefons, Fontsanta, Gavarra y la zona del RCDE Stadium",
         intro="En Cornellà atendemos averías y accidentes tanto en el casco urbano como en los accesos a la A-2 y la B-23."),
    dict(slug="grua-el-prat-de-llobregat", name="El Prat de Llobregat",
         near="junto a Barcelona y al aeropuerto, con acceso rápido por la C-31 y la Ronda Litoral",
         roads="la C-31, la autovía de Castelldefels, la B-22 y los accesos al Aeropuerto",
         places="el centro del Prat, Sant Cosme, el polígono Mas Blau y el Aeropuerto Josep Tarradellas Barcelona-El Prat (T1 y T2)",
         intro="¿Tu coche te ha dejado tirado de camino al aeropuerto o en los polígonos del Prat? Llámanos y vamos a por ti."),
    dict(slug="grua-santa-coloma-de-gramenet", name="Santa Coloma de Gramenet",
         near="al otro lado del río Besòs, conectada con Barcelona por la B-20",
         roads="la B-20, la C-31 y la C-58",
         places="Singuerlín, Fondo, Can Mariner, Santa Rosa, Riu Nord y Riu Sud",
         intro="Ofrecemos grúa 24 horas en Santa Coloma de Gramenet con salida inmediata hacia cualquier barrio de la ciudad."),
    dict(slug="grua-sant-adria-de-besos", name="Sant Adrià de Besòs",
         near="en la desembocadura del Besòs, a pocos minutos del Fòrum y de la Ronda Litoral",
         roads="la Ronda Litoral, la C-31 y la B-10",
         places="La Mina, Sant Joan Baptista, Besòs y el Port Fòrum",
         intro="Desde el Fòrum hasta La Mina, recogemos tu vehículo averiado o accidentado en Sant Adrià de Besòs a cualquier hora."),
    dict(slug="grua-esplugues-de-llobregat", name="Esplugues de Llobregat",
         near="al final de la Diagonal, conectada con Barcelona por la Ronda de Dalt",
         roads="la B-23, la Ronda de Dalt y la N-340",
         places="Can Vidalet, La Plana, Ciutat Diagonal y El Gall",
         intro="En Esplugues y Ciutat Diagonal te ofrecemos asistencia en carretera rápida, también en los accesos a la Diagonal y la B-23."),
    dict(slug="grua-sant-cugat-del-valles", name="Sant Cugat del Vallès",
         near="al otro lado de Collserola, a pocos minutos por los túneles de Vallvidrera (C-16)",
         roads="la AP-7, la C-16 (túneles de Vallvidrera) y la B-30",
         places="el centro, Valldoreix, Mira-sol, Les Planes, La Floresta y el Parc Tecnològic del Vallès",
         intro="Cubrimos Sant Cugat y su entorno, incluidos los túneles de Vallvidrera, la AP-7 y las urbanizaciones de la zona."),
    dict(slug="grua-sant-boi-de-llobregat", name="Sant Boi de Llobregat",
         near="en el Baix Llobregat, a pocos minutos de Barcelona por la B-23 y la C-32",
         roads="la C-32, la C-245, la B-23 y la A-2",
         places="Marianao, Casablanca, Camps Blancs, Ciutat Cooperativa, Cooperativa-Molí Nou y los polígonos industriales",
         intro="En Sant Boi atendemos averías y accidentes en el casco urbano, en los polígonos y en la C-32 y la C-245, a cualquier hora."),
    dict(slug="grua-castelldefels", name="Castelldefels",
         near="en la costa del Baix Llobregat, conectada con Barcelona por la C-32 y la autovía de Castelldefels (C-31)",
         roads="la C-32, la C-31 (autovía de Castelldefels) y la C-245",
         places="la Platja, Montmar, Bellamar, Can Bou, el Poal y el Canal Olímpic",
         intro="¿Avería volviendo de la playa o en la C-32? Damos servicio de grúa 24 horas en toda Castelldefels, incluidas las urbanizaciones de montaña."),
    dict(slug="grua-gava", name="Gavà",
         near="entre Viladecans y Castelldefels, con acceso directo por la C-32 y la C-245",
         roads="la C-32, la C-245 y la autovía de Castelldefels",
         places="el centro, Gavà Mar, Can Tries, Bruguers y el polígono de Les Massotes",
         intro="Recogemos tu coche averiado o accidentado en Gavà y Gavà Mar, de día y de noche, y lo llevamos donde nos digas."),
    dict(slug="grua-viladecans", name="Viladecans",
         near="en el Baix Llobregat, junto a la C-32 y a pocos minutos del aeropuerto",
         roads="la C-32, la C-245 y la autovía de Castelldefels",
         places="el centro, Torre-roja, Montserratina, Alba-Rosa, Sales y el polígono Can Calderon",
         intro="Ofrecemos grúa y asistencia en carretera en Viladecans y sus polígonos industriales, con salida inmediata las 24 horas."),
    dict(slug="grua-sant-feliu-de-llobregat", name="Sant Feliu de Llobregat",
         near="junto a la B-23, a pocos minutos de la Diagonal",
         roads="la B-23, la N-340 y la AP-7",
         places="el centro, Mas Lluí, Can Calders, Les Grases y el polígono Eixample Nord",
         intro="En Sant Feliu de Llobregat te ayudamos con averías, pinchazos y accidentes, también en la B-23 y la N-340."),
    dict(slug="grua-sant-joan-despi", name="Sant Joan Despí",
         near="entre Cornellà y Sant Feliu, con salida directa a la B-23 y la Ronda de Dalt",
         roads="la B-23, la N-340 y la Ronda de Dalt",
         places="el centro, Les Planes, Torreblanca, el Pla del Llobregat y la Ciutat Esportiva del FC Barcelona",
         intro="Damos servicio de grúa 24 horas en Sant Joan Despí, tanto en el centro como en los accesos a la B-23."),
    dict(slug="grua-montcada-i-reixac", name="Montcada i Reixac",
         near="al norte de Barcelona, conectada por la C-17, la C-33 y la B-20",
         roads="la C-17, la C-33, la C-58 y la B-30",
         places="Montcada Centre, Can Sant Joan, La Ribera, Terra Nostra, Can Cuiàs y Mas Rampinyo",
         intro="Atendemos averías y accidentes en Montcada i Reixac y en las vías de alta capacidad que la cruzan, como la C-17, la C-33 y la C-58."),
    dict(slug="grua-cerdanyola-del-valles", name="Cerdanyola del Vallès",
         near="en el Vallès Occidental, al otro lado de Collserola, con acceso por la AP-7 y la C-58",
         roads="la AP-7, la C-58, la B-30 y la BV-1414",
         places="el centro, Serraparera, Montflorit, Bellaterra, la UAB y el Parc de l'Alba",
         intro="Cubrimos Cerdanyola del Vallès, Bellaterra y la zona de la UAB con grúa 24 horas, también en la AP-7 y la C-58."),
]

FAQ = [
    ("¿Cuánto tarda en llegar la grúa?",
     "Depende de dónde estés y del tráfico, pero salimos de inmediato en cuanto recibimos tu llamada o tu ubicación por WhatsApp. En Barcelona ciudad y el área metropolitana solemos llegar en muy poco tiempo. Te damos una hora estimada de llegada al hablar contigo."),
    ("¿Cuánto cuesta una grúa en Barcelona?",
     "El precio depende de la distancia, el tipo de vehículo y la hora. Te damos un presupuesto claro y sin compromiso antes de salir, para que no haya sorpresas. Escríbenos por WhatsApp con tu ubicación y el destino y te respondemos al momento."),
    ("¿Trabajáis de noche, fines de semana y festivos?",
     "Sí. Somos un servicio de asistencia 24 horas, los 365 días del año, incluidos noches, fines de semana y festivos."),
    ("¿Qué datos necesito para pedir una grúa?",
     "Tu ubicación (puedes enviarla por WhatsApp), el modelo del vehículo, qué le pasa y a dónde quieres llevarlo. Con eso preparamos la asistencia más adecuada."),
    ("¿Lleváis el coche a mi taller de confianza?",
     "Sí, trasladamos tu vehículo al taller, concesionario, domicilio o lugar que tú nos digas, dentro y fuera de Barcelona."),
    ("¿Podéis recoger coches en parkings subterráneos?",
     "En muchos casos sí. Indícanos la altura del parking y el tipo de vehículo y te confirmamos la mejor manera de sacarlo."),
    ("¿Hacéis traslados fuera de Cataluña?",
     "Sí, realizamos transportes de vehículos a cualquier punto de España con presupuesto cerrado."),
]


SERVICE_PAGES = {
    "remolque-coches-barcelona": dict(
        h1="Remolque de coches en Barcelona",
        title="Remolque de Coches Barcelona 24h",
        desc="Remolque de coches averiados en Barcelona las 24 horas. Grúa de plataforma, traslado al taller o domicilio y presupuesto al momento.",
        intro="¿Tu coche no arranca, hace un ruido raro o se ha parado en plena calle? Lo remolcamos con grúa de plataforma y lo llevamos al taller, concesionario o domicilio que elijas, en Barcelona y su área metropolitana.",
        sections=[
            ("Grúa de plataforma: tu coche no sufre", "Cargamos el vehículo sobre la plataforma, sin arrastrarlo por el suelo. Así protegemos la caja de cambios, la transmisión y los bajos, algo especialmente importante en coches automáticos, eléctricos, híbridos y 4x4."),
            ("Coches, furgonetas, eléctricos y 4x4", "Remolcamos turismos, furgonetas, vehículos eléctricos e híbridos, SUV y todoterrenos. Dinos el modelo al llamar y te confirmamos al momento cómo hacer el traslado."),
            ("A tu taller de confianza o a donde necesites", "Llevamos el coche a tu taller habitual, al concesionario oficial de la marca o a tu casa si el taller está cerrado. Si no conoces ningún taller en la zona, te orientamos."),
        ],
        faq=[("¿Podéis remolcar un coche automático o eléctrico?", "Sí. Usamos grúa de plataforma, que carga el vehículo entero sin que las ruedas giren, que es la forma recomendada por los fabricantes para coches automáticos, eléctricos e híbridos."),
             ("¿Puedo ir en la grúa con mi coche?", "Normalmente sí, puedes acompañarnos en la cabina hasta el destino. Coméntalo al pedir el servicio.")]),
    "grua-accidente-barcelona": dict(
        h1="Grúa por accidente en Barcelona",
        title="Grúa por Accidente en Barcelona 24h",
        desc="Grúa tras accidente en Barcelona 24h: retirada de vehículos siniestrados en calles, rondas y autopistas. Salida inmediata. Llama al 671 44 86 39.",
        intro="Después de un accidente lo último que necesitas es esperar. Retiramos tu vehículo siniestrado de la calle, la ronda o la autopista y lo llevamos al taller o al depósito que indiques.",
        sections=[
            ("Qué hacer tras un accidente", "Primero, ponte a salvo: chaleco reflectante y fuera de la calzada. Señaliza el vehículo, llama al 112 si hay heridos y rellena el parte amistoso con el otro conductor. Después llámanos o mándanos tu ubicación por WhatsApp y nos encargamos del vehículo."),
            ("Rondas, autopistas y vías rápidas", "Trabajamos en la Ronda de Dalt, la Ronda Litoral, la Gran Via, la Diagonal, la C-31, la C-32, la A-2, la AP-7 y la B-23, entre otras. Conocemos los accesos y retiramos el vehículo de forma rápida y segura."),
            ("Si tu seguro tarda", "Si la asistencia de tu seguro tarda demasiado o no cubre lo que necesitas, podemos hacer el servicio directamente y darte la factura para que la reclames."),
        ],
        faq=[("¿Trabajáis con seguros?", "Podemos hacer el servicio de forma particular y darte la factura detallada para que la presentes a tu aseguradora. Consúltanos tu caso concreto."),
             ("¿Retiráis coches que no ruedan?", "Sí. Los vehículos accidentados con ruedas o dirección dañadas se cargan con la plataforma y el cabrestante de la grúa.")]),
    "arranque-bateria-barcelona": dict(
        h1="Arranque de batería en Barcelona",
        title="Arranque de Batería Barcelona 24h a Domicilio",
        desc="¿Tu coche no arranca? Arranque de batería a domicilio en Barcelona 24h, en la calle o en tu parking. Llegamos rápido. Llama o WhatsApp 671 44 86 39.",
        intro="Batería descargada por el frío, por dejarte las luces encendidas o por pasar días sin usar el coche. Vamos a donde estés, en la calle o en tu parking, y arrancamos el vehículo en el momento.",
        sections=[
            ("Arranque en el sitio", "Arrancamos el motor con un equipo de arranque profesional, sin necesidad de otro coche ni de pinzas. En la mayoría de los casos sigues tu camino en pocos minutos."),
            ("Cuando la batería está agotada", "Si la batería ya no carga, te lo decimos al momento. Podemos llevar el coche al taller o ayudarte a sustituirla para que no te vuelva a dejar tirado."),
            ("Señales de batería débil", "El motor gira lento al arrancar, las luces del salpicadero parpadean o el coche tiene más de 4 o 5 años con la batería original. Si notas alguno de estos síntomas, revisa la batería antes de quedarte tirado."),
        ],
        faq=[("¿Venís a parkings subterráneos?", "Sí, el arranque de batería se puede hacer en casi cualquier parking, porque no hace falta meter la grúa."),
             ("¿Cuánto tarda el arranque?", "Una vez en el sitio, el arranque suele llevar solo unos minutos.")]),
    "cambio-rueda-pinchazo-barcelona": dict(
        h1="Pinchazo y cambio de rueda en Barcelona",
        title="Pinchazo y Cambio de Rueda Barcelona 24h",
        desc="¿Has pinchado? Cambio de rueda en Barcelona 24h, en la calle, la ronda o la autopista. Sin repuesto, te llevamos al taller. Llama al 671 44 86 39.",
        intro="Un pinchazo en plena ronda o de noche puede ser peligroso. Vamos a donde estés: cambiamos la rueda en el sitio o, si no tienes repuesto, llevamos el coche al taller más cercano.",
        sections=[
            ("Cambio de rueda en el momento", "Ponemos tu rueda de repuesto o de galleta de forma segura, con las herramientas adecuadas, incluso si las tuercas están muy apretadas o tienes tuerca antirrobo con su llave."),
            ("Sin rueda de repuesto", "Muchos coches nuevos solo llevan kit antipinchazos. Si el kit no basta o la rueda está reventada, cargamos el coche en la grúa y lo llevamos a un taller de neumáticos."),
        ],
        faq=[("¿Qué hago si pincho en la autopista?", "Sal de la calzada si puedes, ponte el chaleco, coloca la señal V-16 y espera detrás del guardarraíl. Llámanos y no intentes cambiar la rueda en el carril."),
             ("¿Cambiáis ruedas de furgonetas?", "Sí, cambiamos ruedas de turismos, SUV y furgonetas.")]),
    "grua-motos-barcelona": dict(
        h1="Grúa para motos en Barcelona",
        title="Grúa para Motos en Barcelona 24h",
        desc="Grúa para motos y scooters en Barcelona 24h. Traslado seguro con anclajes específicos, por avería o accidente. Llama o WhatsApp 671 44 86 39.",
        intro="Barcelona es una ciudad de motos y scooters, y sabemos cómo transportarlos sin un rasguño. Recogemos tu moto averiada o accidentada y la llevamos al taller o a tu casa.",
        sections=[
            ("Transporte seguro de motos", "Usamos calzos y cinchas específicas para motos, que sujetan la moto por los puntos adecuados sin dañar el carenado ni las suspensiones."),
            ("Scooters, motos grandes y eléctricas", "Trasladamos scooters de 125 cc, motos de gran cilindrada, motos eléctricas y de trail. Si la moto está muy dañada tras una caída, también la recogemos."),
        ],
        faq=[("¿Recogéis motos sin llaves?", "Depende del caso. Consúltanos: necesitamos comprobar que eres el titular o tienes autorización."),
             ("¿Podéis llevar mi moto a la ITV o a otra ciudad?", "Sí, hacemos traslados programados de motos a la ITV, al taller o a cualquier ciudad de España.")]),
    "transporte-vehiculos-barcelona": dict(
        h1="Transporte de vehículos desde Barcelona",
        title="Transporte de Vehículos Barcelona | Toda España",
        desc="Transporte de coches y motos desde Barcelona a toda España. Traslados programados, compraventa, mudanzas y talleres. Presupuesto cerrado: 671 44 86 39.",
        intro="¿Has comprado un coche en otra ciudad, te mudas o necesitas llevar el vehículo a un taller lejos de Barcelona? Hacemos el transporte en grúa, puerta a puerta y con presupuesto cerrado.",
        sections=[
            ("Traslados programados", "Acordamos contigo fecha, hora de recogida y lugar de entrega. El vehículo viaja sobre la plataforma, sin sumar kilómetros ni desgaste."),
            ("Dentro de Cataluña y a toda España", "Trasladamos vehículos a Girona, Tarragona, Lleida y al resto de Cataluña, así como a Madrid, Valencia, Zaragoza, Andorra y cualquier punto de España."),
        ],
        faq=[("¿Cómo se calcula el precio de un traslado largo?", "Según los kilómetros, el tipo de vehículo y la fecha. Envíanos origen, destino y modelo por WhatsApp y te damos un precio cerrado."),
             ("¿Transportáis coches que no funcionan?", "Sí, el vehículo no necesita arrancar: se carga con el cabrestante de la grúa.")]),
    "retirada-coches-desguace-barcelona": dict(
        h1="Retirada de coches para desguace en Barcelona",
        title="Retirada de Coches para Desguace en Barcelona",
        desc="Retiramos tu coche viejo, averiado o siniestrado en Barcelona y lo llevamos a un desguace autorizado para darlo de baja. Llama al 671 44 86 39.",
        intro="¿Tienes un coche viejo ocupando una plaza de parking o que ya no merece la pena reparar? Lo recogemos y lo llevamos a un Centro Autorizado de Tratamiento (CAT) para que se tramite la baja definitiva en la DGT.",
        sections=[
            ("Baja oficial en la DGT", "El desguace autorizado te entrega el certificado de destrucción y tramita la baja, así dejas de pagar el impuesto de circulación y el seguro del vehículo."),
            ("Qué necesitas", "La documentación del vehículo (permiso de circulación y ficha técnica) y el DNI del titular. Si te falta algún documento, consúltanos y te orientamos."),
        ],
        faq=[("¿Recogéis coches sin ITV o sin batería?", "Sí, el coche no necesita arrancar ni tener la ITV en vigor para que lo retiremos."),
             ("¿Recogéis en parkings comunitarios?", "Sí, en la mayoría de los casos. Indícanos la altura del parking y el acceso.")]),
}

# ---------------- PLANTILLAS ----------------
# CSS en línea (menos peticiones = carga más rápida, mejor para Google)
CSS = re.sub(r"\s*\n\s*", "", re.sub(r"/\*.*?\*/", "", (ROOT / "css/styles.css").read_text(encoding="utf-8"), flags=re.S))


def ld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'


BUSINESS = {
    "@context": "https://schema.org",
    "@type": ["AutomotiveBusiness", "EmergencyService"],
    "@id": f"{SITE}/#negocio",
    "name": NAME,
    "alternateName": ["Grúas Asistencia 24H Barcelona", "Grúa 24 horas Barcelona"],
    "description": "Servicio de grúa y asistencia en carretera 24 horas en Barcelona y área metropolitana: remolque de coches, rescate tras accidente, arranque de batería, pinchazos y traslados.",
    "url": f"{SITE}/",
    "telephone": PHONE_FULL,
    "logo": f"{SITE}/img/logo-claro.png",
    "image": [f"{SITE}/img/og-image.jpg", f"{SITE}/img/logo-claro.png", f"{SITE}/img/logo-oscuro.png"],
    "priceRange": "€€",
    "currenciesAccepted": "EUR",
    "paymentAccepted": "Efectivo, Tarjeta, Bizum, Transferencia",
    "address": {"@type": "PostalAddress", "addressLocality": "Barcelona", "addressRegion": "Cataluña", "addressCountry": "ES"},
    "geo": {"@type": "GeoCoordinates", "latitude": 41.3874, "longitude": 2.1686},
    "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "opens": "00:00", "closes": "23:59"}],
    "areaServed": [{"@type": "City", "name": "Barcelona"}] + [{"@type": "City", "name": z["name"]} for z in ZONES]
                  + [{"@type": "AdministrativeArea", "name": "Área Metropolitana de Barcelona"}],
    "contactPoint": {"@type": "ContactPoint", "telephone": PHONE_FULL, "contactType": "emergency",
                     "availableLanguage": ["es", "ca"], "hoursAvailable": "Mo-Su 00:00-23:59"},
    "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Servicios de grúa y asistencia en carretera",
                        "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s[1], "description": s[2]}} for s in SERVICES]},
    "sameAs": [],
}


def head(title, desc, path, extra_ld=(), robots="index, follow, max-image-preview:large", preload=False):
    url = f"{SITE}{path}"
    pre = '<link rel="preload" as="image" href="/img/logo-oscuro.webp" type="image/webp" fetchpriority="high">' if preload else ""
    ga = ""
    if GA4_ID:
        ga = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>'
              f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA4_ID}');</script>")
    gsc = f'<meta name="google-site-verification" content="{GSC_VERIFY}">' if GSC_VERIFY else ""
    lds = "\n".join(ld(x) for x in extra_ld)
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="es-ES" href="{url}">
<meta name="author" content="{NAME}">
<meta name="theme-color" content="#0f0f10">
<meta name="format-detection" content="telephone=yes">
<meta name="geo.region" content="ES-CT">
<meta name="geo.placename" content="Barcelona">
<meta name="geo.position" content="41.3874;2.1686">
<meta name="ICBM" content="41.3874, 2.1686">
{gsc}
<meta property="og:type" content="website">
<meta property="og:locale" content="es_ES">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Logo de {NAME}, grúa 24 horas">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/img/og-image.jpg">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/img/icon-32.png">
<link rel="apple-touch-icon" href="/img/icon-180.png">
<link rel="manifest" href="/site.webmanifest">
{pre}
<style>{CSS}</style>
{ld(BUSINESS)}
{lds}
{ga}
</head>
<body>
<a class="skip" href="#main">Saltar al contenido</a>
<div class="top">🚨 Grúa 24 horas en Barcelona · Llama ahora: <a href="tel:{PHONE_INTL}" data-track="click_llamar">{PHONE_TXT}</a></div>
<header class="site">
 <div class="wrap nav">
  <a class="brand" href="/" aria-label="{NAME} - Inicio"><img src="/img/icon-192.png" alt="" width="46" height="46">
   <span>ASISTENCIA 24H<small>BARCELONA</small></span></a>
  <nav aria-label="Principal"><ul class="menu">
   <li><a href="/#servicios">Servicios</a></li><li><a href="/#zonas">Zonas</a></li>
   <li><a href="/#como-funciona">Cómo funciona</a></li><li><a href="/#preguntas">Preguntas</a></li><li><a href="/#contacto">Contacto</a></li>
  </ul></nav>
  <a class="btn btn-y" href="tel:{PHONE_INTL}" data-track="click_llamar">{ICON["tel"]}<span>{PHONE_TXT}</span></a>
 </div>
</header>
<main id="main">
"""


def foot():
    zl = "".join(f'<li><a href="/{z["slug"]}/">Grúa en {z["name"]}</a></li>' for z in ZONES)
    return f"""</main>
<section class="cta-band" id="contacto">
 <div class="wrap">
  <h2>¿Necesitas una grúa ahora?</h2>
  <p>Llámanos o envíanos tu ubicación por WhatsApp. Respondemos 24 horas, 365 días.</p>
  <a class="phone-big" href="tel:{PHONE_INTL}" data-track="click_llamar">{PHONE_FULL}</a>
  <div class="ctas">
   <a class="btn btn-y" href="tel:{PHONE_INTL}" data-track="click_llamar">{ICON["tel"]} Llamar ahora</a>
   <a class="btn btn-wa" href="{wa()}" target="_blank" rel="noopener" data-track="click_whatsapp">{ICON["wa"]} WhatsApp</a>
  </div>
 </div>
</section>
<footer>
 <div class="wrap">
  <div class="fgrid">
   <div>
    <picture><source srcset="/img/logo-oscuro.webp" type="image/webp"><img src="/img/logo-oscuro.png" alt="{NAME}" width="220" height="110" loading="lazy" style="width:220px;margin-bottom:14px"></picture>
    <p>Servicio de grúa y asistencia en carretera 24 horas en Barcelona y su área metropolitana.</p>
    <p><strong style="color:#fff">Teléfono y WhatsApp:</strong> <a href="tel:{PHONE_INTL}">{PHONE_FULL}</a><br>
    <strong style="color:#fff">Horario:</strong> 24 horas, 365 días</p>
   </div>
   <div><h3>Servicios</h3><ul>{"".join(f'<li><a href="/{s[3]}/">{s[1]}</a></li>' for s in SERVICES if s[3])}</ul></div>
   <div><h3>Zonas</h3><ul><li><a href="/">Grúa en Barcelona</a></li>{zl}</ul></div>
  </div>
  <div class="legal"><span>© <span id="year">{date.today().year}</span> {NAME}. Todos los derechos reservados.</span>
   <span><a href="/privacidad/">Privacidad</a></span></div>
 </div>
</footer>
<a class="wa-float" href="{wa()}" target="_blank" rel="noopener" aria-label="Pedir grúa por WhatsApp" data-track="click_whatsapp">{ICON["wa"]}</a>
<nav class="mbar" aria-label="Contacto rápido">
 <a class="c" href="tel:{PHONE_INTL}" data-track="click_llamar">{ICON["tel"]} Llamar</a>
 <a class="w" href="{wa()}" target="_blank" rel="noopener" data-track="click_whatsapp">{ICON["wa"]} WhatsApp</a>
</nav>
<script src="/js/main.js" defer></script>
</body>
</html>
"""


def ctas(extra=""):
    return f"""<div class="ctas">
 <a class="btn btn-y" href="tel:{PHONE_INTL}" data-track="click_llamar">{ICON["tel"]} Llamar: {PHONE_TXT}</a>
 <a class="btn btn-wa" href="{wa(extra)}" target="_blank" rel="noopener" data-track="click_whatsapp">{ICON["wa"]} Pedir grúa por WhatsApp</a>
</div>"""


def services_html(h="h3", skip=None):
    out = ""
    for i, t, d, slug in SERVICES:
        if slug and slug == skip:
            continue
        name = f'<a href="/{slug}/" class="cardlink">{t}</a>' if slug else t
        out += f'<article class="card"><div class="ic">{SICON[i]}</div><{h}>{name}</{h}><p>{d}</p></article>'
    return out


def faq_html(items=FAQ):
    return "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)


def faq_ld(items=FAQ):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def crumbs_ld(name, path):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": f"{SITE}{path}"}]}

STEPS = f"""<ol class="steps">
 <li><h3>Llama o escribe</h3><p class="muted">Contacta al {PHONE_TXT} por teléfono o WhatsApp a cualquier hora.</p></li>
 <li><h3>Envía tu ubicación</h3><p class="muted">Compártela por WhatsApp y dinos qué le pasa al vehículo y a dónde va.</p></li>
 <li><h3>Presupuesto al momento</h3><p class="muted">Te damos precio y hora estimada de llegada antes de salir. Sin sorpresas.</p></li>
 <li><h3>Llegamos y lo resolvemos</h3><p class="muted">Reparamos en el sitio si es posible o llevamos tu coche donde necesites.</p></li>
</ol>"""


# ---------------- PÁGINAS ----------------
def index():
    title = f"Grúa 24 Horas Barcelona | Asistencia en Carretera ☎ {PHONE_TXT}"
    desc = f"Grúa 24h en Barcelona y área metropolitana: remolque de coches y motos, accidentes, batería y pinchazos. Precio al momento. Llama o WhatsApp {PHONE_TXT}."
    website = {"@context": "https://schema.org", "@type": "WebSite", "@id": f"{SITE}/#web", "url": f"{SITE}/", "name": NAME,
               "inLanguage": "es-ES", "publisher": {"@id": f"{SITE}/#negocio"}}
    zones = "".join(f'<li><span>{d}</span></li>' for d in BCN_DISTRICTS) + "".join(
        f'<li><a href="/{z["slug"]}/">{z["name"]}</a></li>' for z in ZONES)
    body = f"""
<section class="hero">
 <div class="wrap grid">
  <div>
   <span class="badge"><span class="dot"></span> Disponibles ahora · 24h / 365 días</span>
   <h1>Grúa 24 horas en <span class="hl">Barcelona</span></h1>
   <p class="lead">Servicio de grúa y asistencia en carretera en Barcelona y toda el área metropolitana. ¿Avería, accidente, batería o pinchazo? Salimos al momento, de día y de noche.</p>
   {ctas()}
   <ul class="ticks"><li>Llegada rápida</li><li>Presupuesto sin compromiso</li><li>Coches, furgonetas y motos</li><li>Pago con tarjeta y Bizum</li></ul>
  </div>
  <div class="hero-logo">
   <picture><source srcset="/img/logo-oscuro.webp" type="image/webp"><img src="/img/logo-oscuro.png" alt="Asistencia 24H Barcelona - servicio de grúa" width="520" height="261" fetchpriority="high"></picture>
  </div>
 </div>
</section>

<section class="alt" aria-label="Datos del servicio">
 <div class="wrap stats">
  <div class="stat"><b>24h</b>Todos los días</div>
  <div class="stat"><b>365</b>Días al año</div>
  <div class="stat"><b>AMB</b>Barcelona y alrededores</div>
  <div class="stat"><b>0 €</b>Por pedir presupuesto</div>
 </div>
</section>

<section id="servicios">
 <div class="wrap">
  <span class="kicker">Servicios</span>
  <h2>Servicio de grúa y asistencia en carretera en Barcelona</h2>
  <p class="muted">Todo lo que necesitas cuando tu vehículo te deja tirado, con un único número de contacto disponible las 24 horas.</p>
  <div class="cards">{services_html()}</div>
 </div>
</section>

<section class="light">
 <div class="wrap split">
  <div>
   <span class="kicker">Quiénes somos</span>
   <h2>Tu grúa de confianza en Barcelona</h2>
   <p class="muted">En <strong>{NAME}</strong> nos dedicamos al remolque y la asistencia en carretera de coches, furgonetas y motos. Conocemos Barcelona y sus accesos —Rondas, Gran Via, Diagonal, C-31, C-32, A-2, AP-7, B-23— y sabemos lo importante que es llegar rápido cuando estás parado en la carretera.</p>
   <p class="muted">Trato directo, sin centralitas: hablas con quien va a ir a ayudarte. Te damos el precio antes de salir y tratamos tu vehículo como si fuera nuestro.</p>
   <ul class="zones"><li><span>✔ Trato directo</span></li><li><span>✔ Precio claro</span></li><li><span>✔ Grúa de plataforma</span></li></ul>
  </div>
  <picture><source srcset="/img/logo-claro.webp" type="image/webp"><img src="/img/logo-claro.png" alt="Logo Asistencia 24H Barcelona con grúa de remolque" width="600" height="377" loading="lazy"></picture>
 </div>
</section>

<section id="como-funciona" class="alt">
 <div class="wrap">
  <span class="kicker">Cómo funciona</span>
  <h2>Pedir una grúa es muy fácil</h2>
  {STEPS}
 </div>
</section>

<section id="zonas">
 <div class="wrap">
  <span class="kicker">Zonas de servicio</span>
  <h2>Grúa en Barcelona y área metropolitana</h2>
  <p class="muted">Cubrimos todos los distritos de Barcelona y los municipios de alrededor. Si no ves tu zona, llámanos: seguramente también llegamos.</p>
  <ul class="zones">{zones}</ul>
 </div>
</section>

<section class="light">
 <div class="wrap prose">
  <span class="kicker">Grúa en Barcelona</span>
  <h2>Grúa barata y de confianza en Barcelona, 24 horas</h2>
  <p>Cuando buscas una <strong>grúa cerca de ti en Barcelona</strong> quieres tres cosas: que llegue rápido, que el precio sea claro y que traten bien tu coche. En {NAME} trabajamos así desde el primer minuto: te cogemos el teléfono a cualquier hora, te damos el precio antes de salir y llevamos tu vehículo sobre plataforma hasta donde nos digas.</p>
  <h3>¿Cuánto cuesta una grúa en Barcelona?</h3>
  <p>El precio de una grúa depende de los kilómetros del traslado, del tipo de vehículo (coche, furgoneta o moto), de si está en un parking o en la vía pública y de la hora del servicio. Por eso no damos tarifas genéricas: mándanos tu ubicación y el destino por WhatsApp y te respondemos con un <strong>precio cerrado y sin compromiso</strong>. Sin suplementos sorpresa al llegar.</p>
  <h3>Auxilio en carretera en rondas y autopistas</h3>
  <p>Damos auxilio en carretera en la Ronda de Dalt, la Ronda Litoral, la Gran Via, la Diagonal, la Meridiana, la C-31, la C-32, la C-58, la A-2, la AP-7 y la B-23. Si te quedas parado en una vía rápida, ponte a salvo detrás del guardarraíl, activa la baliza V-16 y llámanos al <a href="tel:{PHONE_INTL}">{PHONE_TXT}</a>.</p>
  <h3>¿Y si mi seguro no cubre la grúa o tarda demasiado?</h3>
  <p>Es habitual que la asistencia del seguro tarde horas en llegar o que no cubra traslados largos o vehículos sin seguro en vigor. Nosotros hacemos el servicio de forma particular y te entregamos la factura, para que puedas reclamarla a tu aseguradora si corresponde.</p>
 </div>
</section>

<section id="preguntas" class="alt">
 <div class="wrap prose">
  <span class="kicker">Preguntas frecuentes</span>
  <h2>Dudas sobre nuestro servicio de grúa</h2>
  {faq_html()}
 </div>
</section>
"""
    return head(title, desc, "/", [website, faq_ld()], preload=True) + body + foot()


def zone_faq(z):
    n = z["name"]
    return [
        (f"¿Cuánto tarda la grúa en llegar a {n}?",
         f"Salimos en cuanto recibimos tu llamada o tu ubicación por WhatsApp. {n} está {z['near']}, así que solemos llegar en poco tiempo. Al hablar contigo te damos una hora estimada según el tráfico."),
        (f"¿En qué zonas de {n} dais servicio?",
         f"En todo el municipio: {z['places']}. También atendemos averías y accidentes en {z['roads']}."),
        (f"¿A dónde lleváis mi coche desde {n}?",
         f"A donde prefieras: un taller de {n}, tu concesionario oficial en Barcelona, tu domicilio o cualquier otra dirección. Si no conoces ningún taller en la zona, te orientamos."),
        (f"¿Cuánto cuesta la grúa en {n}?",
         "Depende de la distancia hasta el destino, del vehículo y de la hora. Envíanos tu ubicación y el destino por WhatsApp y te damos un precio cerrado y sin compromiso antes de salir."),
    ]


def zone(z):
    n = z["name"]
    path = f"/{z['slug']}/"
    title = f"Grúa 24h {n} ☎ {PHONE_TXT}"
    desc = f"Grúa 24h en {n}: remolque de coches y motos, accidentes, batería y pinchazos. Precio al momento. Llama o WhatsApp {PHONE_TXT}."
    faq = zone_faq(z)
    svc = {"@context": "https://schema.org", "@type": "Service", "serviceType": "Servicio de grúa y asistencia en carretera",
           "name": f"Grúa 24 horas en {n}", "provider": {"@id": f"{SITE}/#negocio"},
           "areaServed": {"@type": "City", "name": n}, "availableChannel": {"@type": "ServiceChannel", "servicePhone": {"@type": "ContactPoint", "telephone": PHONE_FULL}}}
    others = "".join(f'<li><a href="/{o["slug"]}/">Grúa en {o["name"]}</a></li>' for o in ZONES if o is not z)
    body = f"""
<section class="hero">
 <div class="wrap">
  <nav class="breadcrumb" aria-label="Migas de pan"><a href="/">Inicio</a> › Grúa en {n}</nav>
  <span class="badge"><span class="dot"></span> Disponibles ahora en {n}</span>
  <h1>Grúa 24 horas en <span class="hl">{n}</span></h1>
  <p class="lead">{z["intro"]}</p>
  {ctas(n + " - ")}
  <ul class="ticks"><li>24h / 365 días</li><li>Presupuesto al momento</li><li>Coches, furgonetas y motos</li></ul>
 </div>
</section>

<section>
 <div class="wrap">
  <span class="kicker">Servicios en {n}</span>
  <h2>Asistencia en carretera en {n}</h2>
  <p class="muted">{n} está {z["near"]}. Atendemos averías y accidentes en todo el municipio: {z["places"]}, y en vías como {z["roads"]}.</p>
  <div class="cards">{services_html()}</div>
 </div>
</section>

<section class="alt">
 <div class="wrap">
  <span class="kicker">Cómo funciona</span>
  <h2>Pide tu grúa en {n} en 4 pasos</h2>
  {STEPS}
 </div>
</section>

<section>
 <div class="wrap prose">
  <span class="kicker">Preguntas frecuentes</span>
  <h2>Grúa en {n}: preguntas frecuentes</h2>
  {faq_html(faq)}
 </div>
</section>

<section class="alt">
 <div class="wrap">
  <h2>Otras zonas donde trabajamos</h2>
  <ul class="zones"><li><a href="/">Grúa en Barcelona</a></li>{others}</ul>
 </div>
</section>
"""
    return head(title, desc, path, [crumbs_ld(f"Grúa en {n}", path), svc, faq_ld(faq)]) + body + foot()


def service_page(slug):
    sp = SERVICE_PAGES[slug]
    icon, name, short, _ = next(s for s in SERVICES if s[3] == slug)
    path = f"/{slug}/"
    svc = {"@context": "https://schema.org", "@type": "Service", "serviceType": name, "name": sp["h1"],
           "description": sp["desc"], "provider": {"@id": f"{SITE}/#negocio"},
           "areaServed": [{"@type": "City", "name": "Barcelona"}] + [{"@type": "City", "name": z["name"]} for z in ZONES],
           "hoursAvailable": "Mo-Su 00:00-23:59"}
    sections = "".join(f"<h2>{h}</h2><p>{t}</p>" for h, t in sp["sections"])
    zl = "".join(f'<li><a href="/{z["slug"]}/">{z["name"]}</a></li>' for z in ZONES)
    body = f"""
<section class="hero">
 <div class="wrap">
  <nav class="breadcrumb" aria-label="Migas de pan"><a href="/">Inicio</a> › {name}</nav>
  <span class="badge"><span class="dot"></span> Servicio 24h / 365 días</span>
  <h1>{sp["h1"]}</h1>
  <p class="lead">{sp["intro"]}</p>
  {ctas(name + " - ")}
  <ul class="ticks"><li>Salida inmediata</li><li>Precio cerrado antes de salir</li><li>Barcelona y área metropolitana</li></ul>
 </div>
</section>

<section class="light">
 <div class="wrap prose">{sections}</div>
</section>

<section class="alt">
 <div class="wrap">
  <span class="kicker">Cómo funciona</span>
  <h2>Así de fácil es pedirnos ayuda</h2>
  {STEPS}
 </div>
</section>

<section>
 <div class="wrap prose">
  <span class="kicker">Preguntas frecuentes</span>
  <h2>{name}: dudas habituales</h2>
  {faq_html(sp["faq"])}
 </div>
</section>

<section class="alt">
 <div class="wrap">
  <h2>Otros servicios</h2>
  <div class="cards">{services_html(skip=slug)}</div>
  <h2 style="margin-top:48px">Zonas donde hacemos este servicio</h2>
  <ul class="zones"><li><a href="/">Barcelona</a></li>{zl}</ul>
 </div>
</section>
"""
    return head(f"{sp['title']} ☎ {PHONE_TXT}", sp["desc"], path, [crumbs_ld(name, path), svc, faq_ld(sp["faq"])]) + body + foot()


def legal_page(slug, title, html):
    body = f"""<section><div class="wrap prose"><nav class="breadcrumb"><a href="/">Inicio</a> › {title}</nav><h1>{title}</h1>{html}</div></section>"""
    return head(f"{title} | {NAME}", f"{title} de {NAME}.", f"/{slug}/", robots="noindex, follow") + body + foot()


LEGAL = {
    "privacidad": ("Política de privacidad", f"""
<p>De acuerdo con el Reglamento (UE) 2016/679 (RGPD) y la LO 3/2018 (LOPDGDD):</p>
<ul><li><strong>Responsable:</strong> {OWNER} ({NIF}) · {PHONE_FULL} · {EMAIL}</li>
<li><strong>Finalidad:</strong> atender tu solicitud de grúa o asistencia, elaborar presupuestos y prestar el servicio.</li>
<li><strong>Legitimación:</strong> tu consentimiento al contactarnos y la ejecución del servicio solicitado.</li>
<li><strong>Datos tratados:</strong> nombre, teléfono, ubicación y datos del vehículo que nos facilites.</li>
<li><strong>Conservación:</strong> el tiempo necesario para prestar el servicio y cumplir obligaciones legales.</li>
<li><strong>Destinatarios:</strong> no se ceden datos a terceros salvo obligación legal. Si nos contactas por WhatsApp se aplica también la política de WhatsApp (Meta).</li>
<li><strong>Derechos:</strong> puedes ejercer acceso, rectificación, supresión, oposición, limitación y portabilidad escribiendo a {EMAIL}, y reclamar ante la Agencia Española de Protección de Datos (www.aepd.es).</li></ul>
<p>Esta web no tiene formularios: solo recibimos los datos que tú nos envías por teléfono o WhatsApp.</p>"""),
}


def page_404():
    body = f"""<section class="hero"><div class="wrap center"><h1>Página no encontrada</h1>
<p class="lead" style="margin-inline:auto">La página que buscas no existe, pero si necesitas una grúa estamos disponibles 24 horas.</p>
<div class="ctas" style="justify-content:center"><a class="btn btn-o" href="/">Volver al inicio</a>
<a class="btn btn-y" href="tel:{PHONE_INTL}">{ICON["tel"]} {PHONE_TXT}</a></div></div></section>"""
    return head(f"Página no encontrada | {NAME}", "Página no encontrada.", "/404.html", robots="noindex, follow") + body + foot()


def relativize(rel, txt):
    """Rutas relativas: la web funciona en GitHub Pages (/gruaweb/) y en un dominio propio sin cambios."""
    if rel == "404.html":
        # GitHub Pages sirve el 404 en cualquier ruta: fijamos la base según dónde esté publicada la web
        base = ('<script>document.write(\'<base href="\'+(location.hostname.endsWith(".github.io")'
                '?"/"+location.pathname.split("/")[1]+"/":"/")+\'">\')</script>')
        txt, prefix = txt.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n' + base, 1), ""
    else:
        prefix = "../" * rel.count("/") or "./"
    for attr in ("href", "src", "srcset"):
        txt = txt.replace(f'{attr}="/', f'{attr}="{prefix}')
    return txt


def write(rel, txt):
    if rel.endswith(".html"):
        txt = relativize(rel, txt)
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(txt, encoding="utf-8")
    print("✓", rel)


def main():
    write("index.html", index())
    for z in ZONES:
        write(f"{z['slug']}/index.html", zone(z))
    for slug in SERVICE_PAGES:
        write(f"{slug}/index.html", service_page(slug))
    for slug, (t, h) in LEGAL.items():
        write(f"{slug}/index.html", legal_page(slug, t, h))
    write("404.html", page_404())

    urls = [("/", "1.0", "weekly")] + [(f"/{s}/", "0.9", "monthly") for s in SERVICE_PAGES] + [(f"/{z['slug']}/", "0.8", "monthly") for z in ZONES]
    sm = "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{c}</changefreq><priority>{p}</priority>"
                 + (f"<image:image><image:loc>{SITE}/img/logo-claro.png</image:loc></image:image>" if u == "/" else "") + "</url>\n"
                 for u, p, c in urls)
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
          'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + sm + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /404.html\n\nSitemap: {SITE}/sitemap.xml\n")
    write("site.webmanifest", json.dumps({
        "name": NAME, "short_name": "Grúa 24H BCN", "description": "Grúa y asistencia en carretera 24h en Barcelona",
        "start_url": "./", "display": "standalone", "background_color": "#0f0f10", "theme_color": "#0f0f10", "lang": "es",
        "icons": [{"src": "img/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "img/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]},
        ensure_ascii=False, indent=2))
    write("llms.txt", f"# {NAME}\n\n> Servicio de grúa y asistencia en carretera 24 horas en Barcelona y área metropolitana.\n\n"
          f"- Teléfono y WhatsApp: {PHONE_FULL}\n- Horario: 24 horas, 365 días\n- Zonas: Barcelona, " + ", ".join(z["name"] for z in ZONES) +
          "\n- Servicios: " + ", ".join(s[1] for s in SERVICES) + f"\n- Web: {SITE}/\n")


if __name__ == "__main__":
    main()
