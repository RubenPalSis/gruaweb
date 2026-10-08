#!/usr/bin/env python3
"""Genera la web estática de PL Grúas.

Edita la CONFIGURACIÓN y ejecuta:  python3 build.py
Crea index.html, páginas de zona, páginas legales, 404, sitemap.xml, robots.txt y manifest.
"""
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import quote

# ---------------- CONFIGURACIÓN ----------------
SITE = "https://gruaspl.es"  # <- cambia por tu dominio real (sin / final)
NAME = "PL Grúas"
PHONE_INTL = "+34671448639"
PHONE_TXT = "671 44 86 39"
PHONE_FULL = "+34 671 44 86 39"
WA_MSG = "Hola, necesito una grúa"
GA4_ID = ""  # p.ej. "G-XXXXXXX" para Google Analytics (opcional)
GSC_VERIFY = ""  # código de verificación de Google Search Console (opcional)
# Datos del titular para Aviso legal y Política de privacidad (obligatorios por la LSSI y el RGPD)
TITULAR = "Pedro Luis Ramos Aguilar"  # nombre y apellidos o razón social
NIF = "47779753J"
DOMICILIO = "Ctra. d'Esplugues, 208, 1.º 2.ª, 08940 Cornellà de Llobregat (Barcelona)"  # dirección completa
EMAIL = "gruaspl@gmail.com"
# -----------------------------------------------

ROOT = Path(__file__).parent
TODAY = date.today().isoformat()


def wa(motivo="", lugar=""):
    """Enlace de WhatsApp con mensaje ya escrito: motivo (p.ej. "mi coche no arranca") y lugar (p.ej. "Badalona")."""
    msg = WA_MSG + (f", {motivo}" if motivo else "") + ". Estoy en: " + (f"{lugar}, " if lugar else "")
    return f"https://wa.me/{PHONE_INTL[1:]}?text={quote(msg)}"


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
    "reloj": f'<svg {SV}><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "euro": f'<svg {SV}><path d="M17 6.5A7 7 0 1 0 17 17.5M4 10h9M4 14h9"/></svg>',
    "escudo": f'<svg {SV}><path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6l-8-3z"/><path d="m9 12 2 2 4-4"/></svg>',
    "pin": f'<svg {SV}><path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>',
    "chat": f'<svg {SV}><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/></svg>',
    "baja": f'<svg {SV}><path d="M3 6h18M8 6V4h8v2m-9 0 1 14h8l1-14"/></svg>',
}

SERVICES = [  # (icono, nombre, descripción corta, página propia o None)
    ("grua", "Remolque de coches averiados", "Al taller o a casa, en grúa de plataforma.", "remolque-coches-barcelona"),
    ("acc", "Rescate tras accidente", "Retirada rápida en calles, rondas y autopistas.", "grua-accidente-barcelona"),
    ("bat", "Arranque de batería", "¿No arranca? Lo arrancamos donde estés.", "arranque-bateria-barcelona"),
    ("rueda", "Pinchazo y cambio de rueda", "Cambiamos la rueda en el momento.", "cambio-rueda-pinchazo-barcelona"),
    ("fuel", "Falta de combustible", "Te llevamos combustible o a la gasolinera.", "falta-combustible-barcelona"),
    ("moto", "Traslado de motos", "Motos y scooters con anclajes específicos.", "grua-motos-barcelona"),
    ("km", "Traslados de larga distancia", "A toda Cataluña y España, precio cerrado.", "transporte-vehiculos-barcelona"),
    ("llave", "Traslados a ITV y taller", "Coches que no pueden circular.", "traslado-itv-taller-barcelona"),
    ("baja", "Retirada para desguace", "A desguace autorizado para la baja.", "retirada-coches-desguace-barcelona"),
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
    ("¿Cuánto tarda la grúa?",
     "Salimos en cuanto nos llamas o nos envías tu ubicación por WhatsApp. Te damos la hora estimada de llegada al momento."),
    ("¿Cuánto cuesta una grúa en Barcelona?",
     "Depende de la distancia, el vehículo y la hora. Mándanos ubicación y destino por WhatsApp y te damos un precio cerrado y sin compromiso antes de salir."),
    ("¿Trabajáis de noche y festivos?",
     "Sí, 24 horas, los 365 días del año."),
    ("¿Lleváis el coche a mi taller?",
     "Sí, al taller, concesionario o domicilio que nos digas, dentro y fuera de Barcelona."),
    ("¿Y si mi seguro tarda o no me cubre?",
     "Puedes pedir el servicio de forma particular: el profesional que lo realice te entregará la factura para que la reclames a tu aseguradora."),
    ("¿Qué hago si me quedo parado en una ronda o autopista?",
     "Ponte el chaleco, activa la baliza V-16, sal detrás del guardarraíl y llámanos. Cubrimos rondas, Gran Via, Diagonal, C-31, C-32, C-58, A-2, AP-7 y B-23."),
]


SERVICE_PAGES = {
    "falta-combustible-barcelona": dict(
        h1="Sin gasolina en Barcelona",
        title="Sin Gasolina en Barcelona: Asistencia 24h",
        desc="¿Te has quedado sin gasolina o diésel en Barcelona? Te llevamos combustible o el coche a la gasolinera, 24 horas. Llama al 671 44 86 39.",
        intro="¿Te has quedado sin combustible? Te lo llevamos o remolcamos el coche a la gasolinera más cercana.",
        sections=[
            ("Combustible donde estés", "Gasolina o diésel para llegar a la gasolinera."),
            ("Rondas y autopistas", "Te sacamos de la vía rápida con seguridad."),
            ("¿Combustible equivocado?", "Si has repostado mal, no arranques: lo llevamos al taller."),
        ],
        faq=[("¿Qué hago si me quedo sin gasolina en la ronda?", "Sal del carril si puedes, ponte el chaleco, activa la baliza V-16 y llámanos."),
             ("¿Y si he echado gasolina en un diésel?", "No arranques el motor. Lo llevamos en grúa al taller para vaciar el depósito.")]),
    "traslado-itv-taller-barcelona": dict(
        h1="Traslado a ITV y taller en Barcelona",
        title="Traslado de Coches a ITV y Taller en Barcelona",
        desc="Llevamos en grúa tu coche sin ITV, sin seguro o que no puede circular al taller o a la estación de ITV en Barcelona. Llama al 671 44 86 39.",
        intro="Movemos en grúa los coches que no pueden circular: sin ITV, sin batería o con la ITV desfavorable.",
        sections=[
            ("A la estación de ITV", "Llevamos y traemos tu coche a la cita."),
            ("Al taller que elijas", "Tu taller de confianza o el concesionario."),
            ("Coches parados mucho tiempo", "Sin batería, sin seguro o sin ITV en vigor."),
        ],
        faq=[("¿Puedo llevar a la ITV un coche con la ITV caducada?", "Conducirlo puede suponer una multa. En grúa lo trasladas sin riesgo."),
             ("¿Podéis esperar y traer el coche de vuelta?", "Sí, organizamos ida y vuelta. Pídenos precio.")]),
    "remolque-coches-barcelona": dict(
        h1="Remolque de coches en Barcelona",
        title="Remolque de Coches Barcelona 24h",
        desc="Remolque de coches averiados en Barcelona las 24 horas. Grúa de plataforma, traslado al taller o domicilio y presupuesto al momento.",
        intro="¿Tu coche se ha parado? Lo llevamos en grúa al taller, concesionario o a tu casa.",
        sections=[
            ("Grúa de plataforma: tu coche no sufre", "Lo cargamos sin arrastrarlo: ideal para automáticos y eléctricos."),
            ("Coches, furgonetas, eléctricos y 4x4", "Turismos, furgonetas, SUV, híbridos y eléctricos."),
            ("A tu taller de confianza o a donde necesites", "Taller, concesionario o tu casa: tú eliges."),
        ],
        faq=[("¿Podéis remolcar un coche automático o eléctrico?", "Sí. Usamos grúa de plataforma, que carga el vehículo entero sin que las ruedas giren, que es la forma recomendada por los fabricantes para coches automáticos, eléctricos e híbridos."),
             ("¿Puedo ir en la grúa con mi coche?", "Normalmente sí, puedes acompañarnos en la cabina hasta el destino. Coméntalo al pedir el servicio.")]),
    "grua-accidente-barcelona": dict(
        h1="Grúa por accidente en Barcelona",
        title="Grúa por Accidente en Barcelona 24h",
        desc="Grúa tras accidente en Barcelona 24h: retirada de vehículos siniestrados en calles, rondas y autopistas. Salida inmediata. Llama al 671 44 86 39.",
        intro="Retiramos tu vehículo de la calle, la ronda o la autopista y lo llevamos donde nos digas.",
        sections=[
            ("Qué hacer tras un accidente", "Ponte a salvo, llama al 112 si hay heridos y después a nosotros."),
            ("Rondas, autopistas y vías rápidas", "Rondas, Gran Via, C-31, C-32, A-2, AP-7 y B-23."),
            ("Si tu seguro tarda", "Puedes pedirlo de forma particular y reclamar la factura a tu seguro."),
        ],
        faq=[("¿Trabajáis con seguros?", "Puedes pedir el servicio de forma particular: el profesional que lo realice te dará la factura detallada para que la presentes a tu aseguradora. Consúltanos tu caso concreto."),
             ("¿Retiráis coches que no ruedan?", "Sí. Los vehículos accidentados con ruedas o dirección dañadas se cargan con la plataforma y el cabrestante de la grúa.")]),
    "arranque-bateria-barcelona": dict(
        h1="Arranque de batería en Barcelona",
        title="Arranque de Batería Barcelona 24h a Domicilio",
        desc="¿Tu coche no arranca? Arranque de batería a domicilio en Barcelona 24h, en la calle o en tu parking. Llegamos rápido. Llama o WhatsApp 671 44 86 39.",
        intro="¿El coche no arranca? Vamos a donde estés, en la calle o en tu parking.",
        sections=[
            ("Arranque en el sitio", "Equipo profesional, sin necesidad de otro coche."),
            ("Cuando la batería está agotada", "Si no carga, te llevamos al taller o te ayudamos a cambiarla."),
            ("Señales de batería débil", "Arranque lento o luces que parpadean: revísala a tiempo."),
        ],
        faq=[("¿Venís a parkings subterráneos?", "Sí, el arranque de batería se puede hacer en casi cualquier parking, porque no hace falta meter la grúa."),
             ("¿Cuánto tarda el arranque?", "Una vez en el sitio, el arranque suele llevar solo unos minutos.")]),
    "cambio-rueda-pinchazo-barcelona": dict(
        h1="Pinchazo y cambio de rueda en Barcelona",
        title="Pinchazo y Cambio de Rueda Barcelona 24h",
        desc="¿Has pinchado? Cambio de rueda en Barcelona 24h, en la calle, la ronda o la autopista. Sin repuesto, te llevamos al taller. Llama al 671 44 86 39.",
        intro="Cambiamos la rueda en el sitio o llevamos el coche al taller.",
        sections=[
            ("Cambio de rueda en el momento", "Ponemos tu rueda de repuesto de forma segura."),
            ("Sin rueda de repuesto", "Si el kit antipinchazos no basta, te llevamos al taller."),
        ],
        faq=[("¿Qué hago si pincho en la autopista?", "Sal de la calzada si puedes, ponte el chaleco, coloca la señal V-16 y espera detrás del guardarraíl. Llámanos y no intentes cambiar la rueda en el carril."),
             ("¿Cambiáis ruedas de furgonetas?", "Sí, cambiamos ruedas de turismos, SUV y furgonetas.")]),
    "grua-motos-barcelona": dict(
        h1="Grúa para motos en Barcelona",
        title="Grúa para Motos en Barcelona 24h",
        desc="Grúa para motos y scooters en Barcelona 24h. Traslado seguro con anclajes específicos, por avería o accidente. Llama o WhatsApp 671 44 86 39.",
        intro="Recogemos tu moto o scooter averiado o accidentado y lo llevamos al taller o a casa.",
        sections=[
            ("Transporte seguro de motos", "Calzos y cinchas específicos, sin dañar el carenado."),
            ("Scooters, motos grandes y eléctricas", "Desde scooters de 125 cc hasta motos de gran cilindrada."),
        ],
        faq=[("¿Recogéis motos sin llaves?", "Depende del caso. Consúltanos: necesitamos comprobar que eres el titular o tienes autorización."),
             ("¿Podéis llevar mi moto a la ITV o a otra ciudad?", "Sí, hacemos traslados programados de motos a la ITV, al taller o a cualquier ciudad de España.")]),
    "transporte-vehiculos-barcelona": dict(
        h1="Transporte de vehículos desde Barcelona",
        title="Transporte de Vehículos Barcelona | Toda España",
        desc="Transporte de coches y motos desde Barcelona a toda España. Traslados programados, compraventa, mudanzas y talleres. Presupuesto cerrado: 671 44 86 39.",
        intro="Llevamos tu coche o moto puerta a puerta, con precio cerrado.",
        sections=[
            ("Traslados programados", "Tú eliges día, hora y lugar de entrega."),
            ("Dentro de Cataluña y a toda España", "Girona, Tarragona, Lleida, Madrid, Valencia y más."),
        ],
        faq=[("¿Cómo se calcula el precio de un traslado largo?", "Según los kilómetros, el tipo de vehículo y la fecha. Envíanos origen, destino y modelo por WhatsApp y te damos un precio cerrado."),
             ("¿Transportáis coches que no funcionan?", "Sí, el vehículo no necesita arrancar: se carga con el cabrestante de la grúa.")]),
    "retirada-coches-desguace-barcelona": dict(
        h1="Retirada de coches para desguace en Barcelona",
        title="Retirada de Coches para Desguace en Barcelona",
        desc="Retiramos tu coche viejo, averiado o siniestrado en Barcelona y lo llevamos a un desguace autorizado para darlo de baja. Llama al 671 44 86 39.",
        intro="Recogemos tu coche viejo y lo llevamos a un desguace autorizado para darlo de baja.",
        sections=[
            ("Baja oficial en la DGT", "Te llevamos a un desguace autorizado que tramita la baja."),
            ("Qué necesitas", "Permiso de circulación, ficha técnica y DNI del titular."),
        ],
        faq=[("¿Recogéis coches sin ITV o sin batería?", "Sí, el coche no necesita arrancar ni tener la ITV en vigor para que lo retiremos."),
             ("¿Recogéis en parkings comunitarios?", "Sí, en la mayoría de los casos. Indícanos la altura del parking y el acceso.")]),
}

NOTA_COLABORADORES = ("Algunos servicios pueden ser realizados por profesionales autónomos o empresas colaboradoras independientes. "
                      "En estos casos, el servicio será ejecutado y cobrado directamente por el colaborador asignado, quien actuará como "
                      "profesional independiente. Al solicitar el servicio, el cliente acepta que la prestación pueda ser realizada por uno de nuestros colaboradores.")

RED = ("Amplia red de profesionales colaboradores", [
    "Contamos con una amplia red de profesionales autónomos y empresas colaboradoras independientes especializados en asistencia en carretera, transporte y traslado de vehículos.",
    "Gracias a nuestra red de colaboradores podemos ofrecer una mayor cobertura geográfica, rapidez de respuesta y disponibilidad, adaptándonos a las necesidades de cada servicio.",
    "Cuando recibimos una solicitud, podemos asignarla a uno de nuestros colaboradores disponibles en la zona correspondiente, en función de las características y necesidades del servicio.",
])

FUNCIONAMIENTO = [  # (título, párrafos) — portada y Condiciones de servicio
    ("Gestión e intermediación de servicios", [
        "Nuestra empresa se encarga de recibir, gestionar y coordinar solicitudes de asistencia y transporte de vehículos, poniendo al cliente en contacto con profesionales colaboradores independientes.",
        "Una vez aceptado el servicio, el colaborador asignado se encarga de realizar directamente la prestación utilizando sus propios vehículos, medios y recursos profesionales.",
        "El colaborador será quien preste materialmente el servicio y cobre directamente al cliente por el trabajo realizado."]),
    ("Profesionales independientes", [
        "Los servicios pueden ser realizados por profesionales autónomos o empresas colaboradoras independientes.",
        "Cada colaborador desarrolla su actividad por cuenta propia y es responsable de disponer de los vehículos, medios, permisos, autorizaciones y seguros necesarios para ejercer legalmente su actividad.",
        "La asignación de un colaborador permite ofrecer al cliente una respuesta rápida y una mayor cobertura, especialmente cuando el servicio se encuentra fuera de nuestra zona habitual de actuación."]),
    ("Condiciones del servicio", [
        "Antes de la realización del servicio, el cliente será informado de las condiciones y del precio correspondiente.",
        "Cuando el servicio sea realizado por un colaborador independiente, el cliente será informado de que la ejecución material del servicio corresponde al profesional o empresa colaboradora asignada.",
        "El pago del servicio se realizará directamente al colaborador que haya realizado la asistencia o transporte, quien será responsable de emitir el correspondiente justificante o factura conforme a la normativa aplicable.",
        "Nuestra empresa percibe una comisión del colaborador por las labores de captación, gestión y coordinación del servicio."]),
    ("Atención de incidencias", [
        "En caso de producirse cualquier incidencia relacionada con un servicio realizado por un colaborador, nuestra empresa podrá facilitar la gestión y comunicación entre el cliente y el profesional que haya realizado materialmente el servicio.",
        "El colaborador será responsable de la correcta ejecución material del servicio dentro del ámbito de sus obligaciones profesionales y legales, así como de disponer de los seguros correspondientes.",
        "Todo ello se entiende sin perjuicio de las responsabilidades que legalmente puedan corresponder a cada una de las partes."]),
]

LEGAL = [("aviso-legal", "Aviso legal"), ("politica-privacidad", "Política de privacidad"),
         ("politica-cookies", "Política de cookies"), ("condiciones-servicio", "Condiciones de servicio")]

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
    "alternateName": ["PL Grúas Servicio 24H", "Grúa 24 horas Barcelona"],
    "description": "Gestión y coordinación, con una red de profesionales colaboradores, de servicios de grúa y asistencia en carretera 24 horas en Barcelona y área metropolitana: remolque de coches, rescate tras accidente, arranque de batería, pinchazos y traslados.",
    "url": f"{SITE}/",
    "telephone": PHONE_FULL,
    "logo": f"{SITE}/img/logo-claro.png",
    "image": [f"{SITE}/img/og-image.jpg", f"{SITE}/img/logo-claro.png", f"{SITE}/img/logo-oscuro.png"],
    "priceRange": "€€",
    "currenciesAccepted": "EUR",
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
<header class="site">
 <div class="wrap nav">
  <a class="brand" href="/" aria-label="{NAME} - Inicio"><img src="/img/icon-192.png" alt="" width="46" height="46">
   <span>PL GRÚAS<small>SERVICIO 24H</small></span></a>
  <nav aria-label="Principal"><ul class="menu">
   <li><a href="/#servicios">Servicios</a></li><li><a href="/#zonas">Zonas</a></li>
   <li><a href="/#como-funciona">Cómo funciona</a></li><li><a href="/#preguntas">Preguntas</a></li><li><a href="/#contacto">Contacto</a></li>
  </ul></nav>
  <a class="btn btn-y" href="tel:{PHONE_INTL}" data-track="click_llamar">{ICON["tel"]}<span>{PHONE_TXT}</span></a>
 </div>
</header>
<main id="main">
"""


def foot(wa_url=None):
    wa_url = wa_url or wa()
    return f"""</main>
<section class="cta-band" id="contacto">
 <div class="wrap">
  <h2>¿Necesitas una grúa ahora?</h2>
  <p>Respondemos 24 horas, 365 días.</p>
  <a class="phone-big" href="tel:{PHONE_INTL}" data-track="click_llamar">{PHONE_FULL}</a>
  <div class="ctas">
   <a class="btn btn-y" href="tel:{PHONE_INTL}" data-track="click_llamar">{ICON["tel"]} Llamar ahora</a>
  </div>
  <p class="nota"><b>Importante:</b> {NOTA_COLABORADORES}</p>
 </div>
</section>
<footer>
 <div class="road" aria-hidden="true"></div>
 <div class="wrap">
  <div class="fgrid">
   <div class="fbrand">
    <picture><source srcset="/img/logo-oscuro.webp" type="image/webp"><img src="/img/logo-oscuro.png" alt="{NAME}" width="240" height="214" loading="lazy"></picture>
    <p>Gestión de servicios de grúa y asistencia en carretera 24h en Barcelona y área metropolitana, con una amplia red de profesionales colaboradores.</p>
   </div>
   <nav aria-label="Servicios"><h3>Servicios</h3><ul>{"".join(f'<li><a href="/{s[3]}/">{s[1]}</a></li>' for s in SERVICES if s[3])}</ul></nav>
   <nav aria-label="Zonas"><h3>Zonas</h3><ul class="cols">{"".join(f'<li><a href="/{z["slug"]}/">{z["name"].replace("de Llobregat", "").replace("del Vallès", "").strip()}</a></li>' for z in ZONES)}</ul></nav>
   <div><h3>Contacto</h3>
    <ul class="fcontact">
     <li>{SICON["reloj"]}<span><b>24 horas</b>365 días al año</span></li>
     <li>{ICON["tel"]}<span><b><a href="tel:{PHONE_INTL}">{PHONE_FULL}</a></b>Teléfono y WhatsApp</span></li>
     <li>{SICON["pin"]}<span><b>Barcelona</b>y área metropolitana</span></li>
    </ul>
   </div>
  </div>
  <div class="legal"><span>© <span id="year">{date.today().year}</span> {NAME}</span>
   <nav class="flegal" aria-label="Información legal">{" | ".join(f'<a href="/{s}/">{t}</a>' for s, t in LEGAL)}</nav>
   <span>Página web creada por <a href="https://zetaweb.es/" target="_blank" rel="noopener">ZetaWeb</a></span></div>
 </div>
</footer>
<a class="wa-float" href="{wa_url}" target="_blank" rel="noopener" aria-label="Pedir grúa por WhatsApp" data-track="click_whatsapp"><span class="wa-ic">{ICON["wa"]}</span><span class="wa-txt"><small>¿Necesitas una grúa?</small>Escríbenos</span></a>
<script src="/js/main.js" defer></script>
</body>
</html>
"""


def ctas():
    return f"""<div class="ctas">
 <a class="btn btn-y" href="tel:{PHONE_INTL}" data-track="click_llamar">{ICON["tel"]} Llamar: {PHONE_TXT}</a>
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
    return '<div class="faq">' + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items) + "</div>"


def faq_ld(items=FAQ):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def crumbs_ld(name, path):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": f"{SITE}{path}"}]}

STEPS = f"""<ol class="steps">
 <li>{ICON["tel"]}<h3>Llama o escribe</h3><p>A cualquier hora</p></li>
 <li>{SICON["pin"]}<h3>Envía tu ubicación</h3><p>Por WhatsApp, en un toque</p></li>
 <li>{SICON["euro"]}<h3>Te damos precio</h3><p>Cerrado, antes de salir</p></li>
 <li>{SICON["grua"]}<h3>Llegamos</h3><p>Y lo solucionamos</p></li>
</ol>"""


# ---------------- PÁGINAS ----------------
def index():
    title = f"{NAME} | Grúa 24 Horas Barcelona ☎ {PHONE_TXT}"
    desc = f"Grúa 24h en Barcelona y área metropolitana: remolque de coches y motos, accidentes, batería y pinchazos. Precio al momento. Llama o WhatsApp {PHONE_TXT}."
    website = {"@context": "https://schema.org", "@type": "WebSite", "@id": f"{SITE}/#web", "url": f"{SITE}/", "name": NAME,
               "inLanguage": "es-ES", "publisher": {"@id": f"{SITE}/#negocio"}}
    zones = '<li><span>Barcelona (todos los distritos)</span></li>' + "".join(
        f'<li><a href="/{z["slug"]}/">{z["name"]}</a></li>' for z in ZONES)
    quick = "".join(
        f'<a class="q" href="{wa(m)}" target="_blank" rel="noopener" data-track="click_whatsapp">{SICON[i]}<span>{t}</span></a>'
        for i, t, m in [("bat", "No arranca", "mi coche no arranca"), ("acc", "Accidente", "he tenido un accidente"),
                        ("rueda", "Pinchazo", "he pinchado una rueda"), ("fuel", "Sin gasolina", "me he quedado sin combustible"),
                        ("grua", "Avería", "mi coche está averiado"), ("moto", "Moto", "es para una moto"),
                        ("km", "Traslado", "quiero presupuesto para un traslado"), ("baja", "Desguace", "quiero llevar un coche al desguace")])
    body = f"""
<section class="hero">
 <div class="wrap grid">
  <div>
   <span class="badge"><span class="dot"></span> Disponibles ahora · 24h</span>
   <h1>Grúa 24 horas en <span class="hl">Barcelona</span></h1>
   <p class="lead">Avería, accidente, batería o pinchazo. Salimos al momento, de día y de noche.</p>
   {ctas()}
  </div>
  <div class="hero-logo">
   <picture><source srcset="/img/logo-oscuro.webp" type="image/webp"><img src="/img/logo-oscuro.png" alt="PL Grúas - servicio de grúa 24H" width="520" height="464" fetchpriority="high"></picture>
  </div>
 </div>
</section>

<section class="feats" aria-label="Por qué elegirnos">
 <div class="wrap fgrid4">
  <div class="feat">{SICON["reloj"]}<b>24h / 365 días</b><span>Noches y festivos</span></div>
  <div class="feat">{SICON["pin"]}<b>Llegada rápida</b><span>Barcelona y AMB</span></div>
  <div class="feat">{SICON["euro"]}<b>Precio cerrado</b><span>Antes de salir</span></div>
  <div class="feat">{SICON["escudo"]}<b>Grúa de plataforma</b><span>Sin dañar tu coche</span></div>
 </div>
</section>

<section class="quick">
 <div class="wrap center">
  <h2>¿Qué le pasa a tu coche?</h2>
  <p class="muted">Pulsa y te respondemos por WhatsApp al momento.</p>
  <div class="qgrid">{quick}</div>
 </div>
</section>

<section id="servicios">
 <div class="wrap">
  <h2>Servicios de grúa en Barcelona</h2>
  <div class="cards">{services_html()}</div>
 </div>
</section>

<section id="pasos" class="alt">
 <div class="wrap">
  <h2>Así de fácil</h2>
  {STEPS}
 </div>
</section>

<section class="truck light" id="colaboradores">
 <div class="wrap split">
  <picture><source srcset="/img/logo-claro.webp" type="image/webp"><img src="/img/logo-claro.png" alt="Logo de PL Grúas" width="600" height="535" loading="lazy"></picture>
  <div>
   <h2>{RED[0]}</h2>
   {"".join(f'<p class="muted">{t}</p>' for t in RED[1])}
  </div>
 </div>
</section>

<section id="como-funciona">
 <div class="wrap">
  <h2>Cómo funciona nuestro servicio</h2>
  <div class="incs two">{"".join(f'<article class="inc"><span class="tick">✓</span><div><h3>{h}</h3>{"".join(f"<p>{t}</p>" for t in ps)}</div></article>' for h, ps in FUNCIONAMIENTO)}</div>
  <p class="muted">Más información en nuestras <a href="/condiciones-servicio/">condiciones de servicio</a>.</p>
 </div>
</section>

<section id="zonas">
 <div class="wrap split zsplit">
  <div>
   <h2>Grúa en Barcelona y alrededores</h2>
   <ul class="zones">{zones}</ul>
  </div>
  <div class="map"><iframe title="Zona de servicio: Barcelona y área metropolitana" src="https://www.openstreetmap.org/export/embed.html?bbox=1.90%2C41.25%2C2.35%2C41.55&amp;layer=mapnik&amp;marker=41.3874%2C2.1686" loading="lazy"></iframe></div>
 </div>
</section>

<section id="preguntas" class="alt">
 <div class="wrap">
  <h2>Preguntas frecuentes</h2>
  {faq_html()}
 </div>
</section>
"""
    return head(title, desc, "/", [website, faq_ld()], preload=True) + body + foot()


def zone_faq(z):
    n = z["name"]
    return [
        (f"¿Cuánto tarda la grúa en llegar a {n}?",
         f"{n} está {z['near']}. Salimos al momento y te damos la hora estimada al llamar."),
        (f"¿Dónde dais servicio en {n}?",
         f"En todo el municipio: {z['places']}, y en {z['roads']}."),
        (f"¿Cuánto cuesta la grúa en {n}?",
         "Depende de la distancia y el vehículo. Te damos precio cerrado por WhatsApp antes de salir."),
    ]


def zone(z):
    n = z["name"]
    path = f"/{z['slug']}/"
    title = f"{NAME} | Grúa 24h {n} ☎ {PHONE_TXT}"
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
  {ctas()}
  <ul class="ticks"><li>24h / 365 días</li></ul>
 </div>
</section>

<section>
 <div class="wrap">
  <h2>Servicios de grúa en {n}</h2>
  <div class="cards">{services_html()}</div>
 </div>
</section>

<section>
 <div class="wrap">
  <h2>Preguntas frecuentes</h2>
  {faq_html(faq)}
 </div>
</section>

<section class="alt">
 <div class="wrap">
  <h2>Otras zonas</h2>
  <ul class="zones"><li><a href="/">Grúa en Barcelona</a></li>{others}</ul>
 </div>
</section>
"""
    return head(title, desc, path, [crumbs_ld(f"Grúa en {n}", path), svc, faq_ld(faq)]) + body + foot(wa(lugar=n))


def service_page(slug):
    sp = SERVICE_PAGES[slug]
    icon, name, short, _ = next(s for s in SERVICES if s[3] == slug)
    path = f"/{slug}/"
    svc = {"@context": "https://schema.org", "@type": "Service", "serviceType": name, "name": sp["h1"],
           "description": sp["desc"], "provider": {"@id": f"{SITE}/#negocio"},
           "areaServed": [{"@type": "City", "name": "Barcelona"}] + [{"@type": "City", "name": z["name"]} for z in ZONES],
           "hoursAvailable": "Mo-Su 00:00-23:59"}
    sections = "".join(f'<article class="inc"><span class="tick">✓</span><div><h3>{h}</h3><p>{t}</p></div></article>' for h, t in sp["sections"])
    body = f"""
<section class="hero">
 <div class="wrap shero">
  <div>
   <nav class="breadcrumb" aria-label="Migas de pan"><a href="/">Inicio</a> › {name}</nav>
   <span class="badge"><span class="dot"></span> Servicio 24h / 365 días</span>
   <h1>{sp["h1"]}</h1>
   <p class="lead">{sp["intro"]}</p>
   {ctas()}
  </div>
  <div class="sicon" aria-hidden="true">{SICON[icon]}</div>
 </div>
</section>

<section>
 <div class="wrap">
  <h2>Qué incluye</h2>
  <div class="incs">{sections}</div>
 </div>
</section>

<section class="alt">
 <div class="wrap">
  <h2>Preguntas frecuentes</h2>
  {faq_html(sp["faq"])}
 </div>
</section>

<section>
 <div class="wrap">
  <h2>Otros servicios</h2>
  <div class="cards">{services_html(skip=slug)}</div>
 </div>
</section>
"""
    return head(f"{NAME} | {sp['title']} ☎ {PHONE_TXT}", sp["desc"], path, [crumbs_ld(name, path), svc, faq_ld(sp["faq"])]) + body + foot(wa(motivo=name.lower()))


def page_404():
    body = f"""<section class="hero"><div class="wrap center"><h1>Página no encontrada</h1>
<p class="lead" style="margin-inline:auto">La página que buscas no existe, pero si necesitas una grúa estamos disponibles 24 horas.</p>
<div class="ctas" style="justify-content:center"><a class="btn btn-o" href="/">Volver al inicio</a>
<a class="btn btn-y" href="tel:{PHONE_INTL}">{ICON["tel"]} {PHONE_TXT}</a></div></div></section>"""
    return head(f"Página no encontrada | {NAME}", "Página no encontrada.", "/404.html", robots="noindex, follow") + body + foot()


def dato(v, etiqueta):
    return v or f"<mark>[{etiqueta}]</mark>"


def legal_pages():
    tit, nif, dom, mail = dato(TITULAR, "Titular"), dato(NIF, "NIF"), dato(DOMICILIO, "Domicilio"), dato(EMAIL, "Email")
    ps = lambda lst: "".join(f"<p>{t}</p>" for t in lst)
    analytics = (" Además, utilizamos Google Analytics para obtener estadísticas anónimas de visitas; estas cookies solo se instalan si las aceptas."
                 if GA4_ID else " No utilizamos cookies analíticas ni publicitarias.")
    return {
        "aviso-legal": f"""
<h2>Datos identificativos</h2>
<p>En cumplimiento del artículo 10 de la Ley 34/2002, de Servicios de la Sociedad de la Información y de Comercio Electrónico (LSSI-CE), se informa de los datos del titular de este sitio web:</p>
<ul><li>Titular: {tit}</li><li>NIF: {nif}</li><li>Domicilio: {dom}</li><li>Teléfono: {PHONE_FULL}</li><li>Email: {mail}</li><li>Web: {SITE}</li></ul>
<h2>Objeto</h2>
<p>Este sitio web informa sobre el servicio de recepción, gestión y coordinación de solicitudes de grúa, asistencia en carretera y transporte de vehículos que presta {NAME}. Los servicios pueden ser realizados materialmente por profesionales autónomos o empresas colaboradoras independientes, tal y como se detalla en las <a href="/condiciones-servicio/">condiciones de servicio</a>.</p>
<h2>Propiedad intelectual</h2>
<p>Los textos, imágenes, logotipos y diseño de esta web son propiedad del titular o se usan con autorización. No se permite su reproducción sin consentimiento previo.</p>
<h2>Responsabilidad</h2>
<p>El titular no se hace responsable del mal uso que se haga de los contenidos de la web ni de los contenidos de sitios de terceros enlazados desde ella.</p>
<h2>Legislación aplicable</h2>
<p>Este aviso legal se rige por la legislación española.</p>""",
        "politica-privacidad": f"""
<h2>Responsable del tratamiento</h2>
<p>{tit} · NIF {nif} · {dom} · {mail} · {PHONE_FULL}</p>
<h2>Qué datos tratamos y para qué</h2>
<p>Cuando nos llamas o escribes por WhatsApp tratamos los datos que nos facilitas (nombre, teléfono, ubicación, datos del vehículo y del servicio solicitado) para gestionar tu solicitud, informarte del precio y coordinar la asistencia.</p>
<h2>Legitimación</h2>
<p>La base legal es la aplicación de medidas precontractuales y la ejecución del servicio que solicitas.</p>
<h2>Destinatarios</h2>
<p>Para poder prestar el servicio, tus datos se comunicarán al profesional autónomo o empresa colaboradora independiente que lo vaya a realizar. Las conversaciones por WhatsApp se rigen además por la política de privacidad de WhatsApp. No se ceden datos a otros terceros salvo obligación legal.</p>
<h2>Conservación</h2>
<p>Conservamos los datos el tiempo necesario para gestionar el servicio y atender posibles incidencias, y después durante los plazos legalmente exigidos.</p>
<h2>Tus derechos</h2>
<p>Puedes ejercer tus derechos de acceso, rectificación, supresión, oposición, limitación y portabilidad escribiendo a {mail}. También puedes presentar una reclamación ante la Agencia Española de Protección de Datos (www.aepd.es).</p>""",
        "politica-cookies": f"""
<h2>Qué son las cookies</h2>
<p>Las cookies son pequeños archivos que las webs guardan en tu navegador para funcionar o recordar información sobre tu visita.</p>
<h2>Cookies que utiliza esta web</h2>
<p>Esta web no utiliza cookies propias que requieran tu consentimiento.{analytics}</p>
<p>El mapa de la zona de servicio se muestra desde OpenStreetMap, que puede tratar datos técnicos de la conexión según su propia política de privacidad.</p>
<h2>Cómo desactivarlas</h2>
<p>Puedes bloquear o eliminar las cookies desde la configuración de tu navegador.</p>""",
        "condiciones-servicio": f"""
<h2>1. Objeto: gestión e intermediación</h2>
{ps(FUNCIONAMIENTO[0][1])}
<h2>2. Red de profesionales colaboradores</h2>
{ps(RED[1])}
<h2>3. Profesionales independientes</h2>
{ps(FUNCIONAMIENTO[1][1])}
<h2>4. Contratación, precio y pago</h2>
{ps(FUNCIONAMIENTO[2][1])}
<h2>5. Incidencias y reclamaciones</h2>
{ps(FUNCIONAMIENTO[3][1])}
<h2>6. Aceptación</h2>
<p>{NOTA_COLABORADORES}</p>
<p>Los datos del titular figuran en el <a href="/aviso-legal/">aviso legal</a>.</p>""",
    }


def legal_page(slug, title, content):
    body = f"""
<section class="hero">
 <div class="wrap">
  <nav class="breadcrumb" aria-label="Migas de pan"><a href="/">Inicio</a> › {title}</nav>
  <h1>{title}</h1>
 </div>
</section>
<section>
 <div class="wrap prose">{content}</div>
</section>
"""
    return head(f"{title} | {NAME}", f"{title} de {NAME}.", f"/{slug}/", robots="noindex, follow") + body + foot()


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
    pages = legal_pages()
    for slug, title in LEGAL:
        write(f"{slug}/index.html", legal_page(slug, title, pages[slug]))
    write("404.html", page_404())

    urls = [("/", "1.0", "weekly")] + [(f"/{s}/", "0.9", "monthly") for s in SERVICE_PAGES] + [(f"/{z['slug']}/", "0.8", "monthly") for z in ZONES]
    sm = "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{c}</changefreq><priority>{p}</priority>"
                 + (f"<image:image><image:loc>{SITE}/img/logo-claro.png</image:loc></image:image>" if u == "/" else "") + "</url>\n"
                 for u, p, c in urls)
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
          'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + sm + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /404.html\n\nSitemap: {SITE}/sitemap.xml\n")
    write("site.webmanifest", json.dumps({
        "name": NAME, "short_name": "PL Grúas", "description": "Grúa y asistencia en carretera 24h en Barcelona",
        "start_url": "./", "display": "standalone", "background_color": "#0f0f10", "theme_color": "#0f0f10", "lang": "es",
        "icons": [{"src": "img/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "img/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]},
        ensure_ascii=False, indent=2))
    write("llms.txt", f"# {NAME}\n\n> Gestión de servicios de grúa y asistencia en carretera 24 horas en Barcelona y área metropolitana. "
          "Los servicios pueden ser realizados y cobrados directamente por profesionales autónomos o empresas colaboradoras independientes.\n\n"
          f"- Teléfono y WhatsApp: {PHONE_FULL}\n- Horario: 24 horas, 365 días\n- Zonas: Barcelona, " + ", ".join(z["name"] for z in ZONES) +
          "\n- Servicios: " + ", ".join(s[1] for s in SERVICES) + f"\n- Web: {SITE}/\n")


if __name__ == "__main__":
    main()
