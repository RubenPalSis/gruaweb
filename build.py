#!/usr/bin/env python3
"""Genera la web estática de PL Grúas en español (raíz), catalán (/ca/) e inglés (/en/).

Edita la CONFIGURACIÓN y ejecuta:  python3 build.py
Crea index.html, páginas de zona, de servicio y legales en los tres idiomas, 404, sitemap.xml, robots.txt y manifest.
Los textos traducibles se escriben con L("español", "català", "english").
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

# ---------------- IDIOMAS ----------------
LANGS = {  # el primero es el idioma por defecto y va en la raíz
    "es": dict(name="Español", locale="es_ES"),
    "ca": dict(name="Català", locale="ca_ES"),
    "en": dict(name="English", locale="en_GB"),
}
DEFAULT = "es"
CUR = DEFAULT  # idioma que se está generando


class L(dict):
    """Texto traducible: L("español", "català", "english")."""

    def __init__(self, es, ca, en):
        super().__init__(es=es, ca=ca, en=en)


def t(x, **kw):
    """Texto en el idioma actual (con .format(**kw) si se pasan variables)."""
    s = x[CUR] if isinstance(x, L) else x
    return s.format(**kw) if kw else s


def lp(path, lang=None):
    """Ruta con el prefijo del idioma: /grua-badalona/ -> /ca/grua-badalona/."""
    lang = lang or CUR
    return path if lang == DEFAULT else f"/{lang}{path}"


def en_(n, hl=False):
    """'en Badalona' / 'a Badalona' / 'al Prat de Llobregat' / 'in Badalona'."""
    prep, name = {"es": "en", "en": "in"}.get(CUR, "a"), n
    if CUR == "ca":
        if n.startswith("El "):
            prep, name = "al", n[3:]
        elif n.startswith("L'"):
            name = "l'" + n[2:]
    return f'{prep} <span class="hl">{name}</span>' if hl else f"{prep} {name}"


FLAG = {
    "es": '<svg viewBox="0 0 750 500" aria-hidden="true"><rect width="750" height="500" fill="#c60b1e"/><rect y="125" width="750" height="250" fill="#ffc400"/></svg>',
    "ca": '<svg viewBox="0 0 810 540" aria-hidden="true"><rect width="810" height="540" fill="#fcdd09"/><path d="M0 90h810M0 210h810M0 330h810M0 450h810" stroke="#da121a" stroke-width="60"/></svg>',
    "en": '<svg viewBox="0 0 60 30" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><clipPath id="uk"><path d="M30 15h30v15zv15H0zH0V0zV0h30z"/></clipPath><path d="M0 0v30h60V0z" fill="#012169"/><path d="M0 0l60 30m0-30L0 30" stroke="#fff" stroke-width="6"/><path d="M0 0l60 30m0-30L0 30" clip-path="url(#uk)" stroke="#c8102e" stroke-width="4"/><path d="M30 0v30M0 15h60" stroke="#fff" stroke-width="10"/><path d="M30 0v30M0 15h60" stroke="#c8102e" stroke-width="6"/></svg>',
}

WA_MSG = L("Hola, necesito una grúa", "Hola, necessito una grua", "Hi, I need a tow truck")
WA_AT = L("Estoy en", "Soc a", "I'm at")


def wa(motivo="", lugar=""):
    """Enlace de WhatsApp con mensaje ya escrito: motivo (p.ej. "mi coche no arranca") y lugar (p.ej. "Badalona")."""
    msg = t(WA_MSG) + (f", {motivo}" if motivo else "") + f". {t(WA_AT)}: " + (f"{lugar}, " if lugar else "")
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
    ("grua", L("Remolque de coches averiados", "Remolc de cotxes avariats", "Broken-down car towing"),
     L("Al taller o a casa, en grúa de plataforma.", "Al taller o a casa, en grua de plataforma.", "To the garage or home, on a flatbed tow truck."),
     "remolque-coches-barcelona"),
    ("acc", L("Rescate tras accidente", "Rescat després d'un accident", "Accident recovery"),
     L("Retirada rápida en calles, rondas y autopistas.", "Retirada ràpida a carrers, rondes i autopistes.", "Fast removal from streets, ring roads and motorways."),
     "grua-accidente-barcelona"),
    ("bat", L("Arranque de batería", "Arrencada de bateria", "Battery jump-start"),
     L("¿No arranca? Lo arrancamos donde estés.", "No arrenca? L'engeguem on siguis.", "Won't start? We'll jump-start it wherever you are."),
     "arranque-bateria-barcelona"),
    ("rueda", L("Pinchazo y cambio de rueda", "Punxada i canvi de roda", "Flat tyre and wheel change"),
     L("Cambiamos la rueda en el momento.", "Canviem la roda a l'instant.", "We change the wheel on the spot."),
     "cambio-rueda-pinchazo-barcelona"),
    ("fuel", L("Falta de combustible", "Falta de combustible", "Out of fuel"),
     L("Te llevamos combustible o a la gasolinera.", "Et portem combustible o et portem a la benzinera.", "We bring you fuel or tow you to a petrol station."),
     "falta-combustible-barcelona"),
    ("moto", L("Traslado de motos", "Trasllat de motos", "Motorbike transport"),
     L("Motos y scooters con anclajes específicos.", "Motos i escúters amb ancoratges específics.", "Motorbikes and scooters with dedicated tie-downs."),
     "grua-motos-barcelona"),
    ("km", L("Traslados de larga distancia", "Trasllats de llarga distància", "Long-distance transport"),
     L("A toda Cataluña y España, precio cerrado.", "A tot Catalunya i Espanya, preu tancat.", "Anywhere in Catalonia and Spain, at a fixed price."),
     "transporte-vehiculos-barcelona"),
    ("llave", L("Traslados a ITV y taller", "Trasllats a l'ITV i al taller", "Transfers to ITV and garage"),
     L("Coches que no pueden circular.", "Cotxes que no poden circular.", "For cars that can't be driven."),
     "traslado-itv-taller-barcelona"),
    ("baja", L("Retirada para desguace", "Retirada per a desballestament", "Scrap car collection"),
     L("A desguace autorizado para la baja.", "A un desballestament autoritzat per a la baixa.", "To an authorised scrapyard for deregistration."),
     "retirada-coches-desguace-barcelona"),
]

BCN_DISTRICTS = ["Ciutat Vella", "Eixample", "Sants-Montjuïc", "Les Corts", "Sarrià-Sant Gervasi", "Gràcia",
                 "Horta-Guinardó", "Nou Barris", "Sant Andreu", "Sant Martí", "Poblenou", "Zona Franca"]

ZONES = [
    dict(slug="grua-hospitalet-de-llobregat", name="L'Hospitalet de Llobregat",
         near=L("pegada a Barcelona: se llega en pocos minutos por la Gran Via o la Ronda Litoral",
                "tocant a Barcelona: s'hi arriba en pocs minuts per la Gran Via o la Ronda Litoral",
                "right next to Barcelona, just a few minutes away via the Gran Via or the Ronda Litoral"),
         roads=L("la Gran Via, la Ronda Litoral, la B-10 y la C-31",
                 "la Gran Via, la Ronda Litoral, la B-10 i la C-31",
                 "the Gran Via, the Ronda Litoral, the B-10 and the C-31"),
         places=L("Bellvitge, Collblanc, La Torrassa, Santa Eulàlia, Can Serra y la Fira Gran Via",
                  "Bellvitge, Collblanc, La Torrassa, Santa Eulàlia, Can Serra i la Fira Gran Via",
                  "Bellvitge, Collblanc, La Torrassa, Santa Eulàlia, Can Serra and Fira Gran Via"),
         intro=L("L'Hospitalet está pegada a Barcelona y una de las zonas con más tráfico del área metropolitana. Por eso tenemos grúa disponible para llegar en muy poco tiempo a cualquier barrio.",
                 "L'Hospitalet és tocant a Barcelona i és una de les zones amb més trànsit de l'àrea metropolitana. Per això tenim grua disponible per arribar en molt poc temps a qualsevol barri.",
                 "L'Hospitalet borders Barcelona and is one of the busiest areas in the metropolitan region. That's why we have a tow truck ready to reach any neighbourhood in no time.")),
    dict(slug="grua-badalona", name="Badalona",
         near=L("justo al norte de Barcelona, con acceso directo por la C-31 y la Ronda Litoral",
                "just al nord de Barcelona, amb accés directe per la C-31 i la Ronda Litoral",
                "just north of Barcelona, with direct access via the C-31 and the Ronda Litoral"),
         roads=L("la C-31, la B-20 (Ronda de Dalt), la Ronda Litoral y la autopista C-32",
                 "la C-31, la B-20 (Ronda de Dalt), la Ronda Litoral i l'autopista C-32",
                 "the C-31, the B-20 (Ronda de Dalt), the Ronda Litoral and the C-32 motorway"),
         places=L("el Centre, Llefià, Sant Roc, Montigalà, Pomar, Bufalà y el Port de Badalona",
                  "el Centre, Llefià, Sant Roc, Montigalà, Pomar, Bufalà i el Port de Badalona",
                  "the Centre, Llefià, Sant Roc, Montigalà, Pomar, Bufalà and Badalona Port"),
         intro=L("Damos servicio de grúa y asistencia en carretera en todo Badalona, desde el puerto hasta los barrios altos, de día y de noche.",
                 "Donem servei de grua i assistència en carretera a tot Badalona, des del port fins als barris alts, de dia i de nit.",
                 "We provide towing and roadside assistance throughout Badalona, from the port to the upper neighbourhoods, day and night.")),
    dict(slug="grua-cornella-de-llobregat", name="Cornellà de Llobregat",
         near=L("a un paso de Barcelona por la Ronda de Dalt y la B-23",
                "a un pas de Barcelona per la Ronda de Dalt i la B-23",
                "a stone's throw from Barcelona via the Ronda de Dalt and the B-23"),
         roads=L("la B-23, la A-2, la Ronda de Dalt y la C-245",
                 "la B-23, l'A-2, la Ronda de Dalt i la C-245",
                 "the B-23, the A-2, the Ronda de Dalt and the C-245"),
         places=L("Almeda, Sant Ildefons, Fontsanta, Gavarra y la zona del RCDE Stadium",
                  "Almeda, Sant Ildefons, Fontsanta, Gavarra i la zona de l'RCDE Stadium",
                  "Almeda, Sant Ildefons, Fontsanta, Gavarra and the RCDE Stadium area"),
         intro=L("En Cornellà atendemos averías y accidentes tanto en el casco urbano como en los accesos a la A-2 y la B-23.",
                 "A Cornellà atenem avaries i accidents tant al nucli urbà com als accessos a l'A-2 i la B-23.",
                 "In Cornellà we handle breakdowns and accidents both in town and on the A-2 and B-23 access roads.")),
    dict(slug="grua-el-prat-de-llobregat", name="El Prat de Llobregat",
         near=L("junto a Barcelona y al aeropuerto, con acceso rápido por la C-31 y la Ronda Litoral",
                "al costat de Barcelona i de l'aeroport, amb accés ràpid per la C-31 i la Ronda Litoral",
                "next to Barcelona and the airport, with quick access via the C-31 and the Ronda Litoral"),
         roads=L("la C-31, la autovía de Castelldefels, la B-22 y los accesos al Aeropuerto",
                 "la C-31, l'autovia de Castelldefels, la B-22 i els accessos a l'Aeroport",
                 "the C-31, the Castelldefels motorway, the B-22 and the airport access roads"),
         places=L("el centro del Prat, Sant Cosme, el polígono Mas Blau y el Aeropuerto Josep Tarradellas Barcelona-El Prat (T1 y T2)",
                  "el centre del Prat, Sant Cosme, el polígon Mas Blau i l'Aeroport Josep Tarradellas Barcelona-El Prat (T1 i T2)",
                  "El Prat town centre, Sant Cosme, the Mas Blau business park and Josep Tarradellas Barcelona-El Prat Airport (T1 and T2)"),
         intro=L("¿Tu coche te ha dejado tirado de camino al aeropuerto o en los polígonos del Prat? Llámanos y vamos a por ti.",
                 "El cotxe t'ha deixat tirat de camí a l'aeroport o als polígons del Prat? Truca'ns i venim a buscar-te.",
                 "Has your car broken down on the way to the airport or in El Prat's industrial estates? Call us and we'll come and get you.")),
    dict(slug="grua-santa-coloma-de-gramenet", name="Santa Coloma de Gramenet",
         near=L("al otro lado del río Besòs, conectada con Barcelona por la B-20",
                "a l'altra banda del riu Besòs, connectada amb Barcelona per la B-20",
                "across the Besòs river, connected to Barcelona by the B-20"),
         roads=L("la B-20, la C-31 y la C-58", "la B-20, la C-31 i la C-58", "the B-20, the C-31 and the C-58"),
         places=L("Singuerlín, Fondo, Can Mariner, Santa Rosa, Riu Nord y Riu Sud",
                  "Singuerlín, Fondo, Can Mariner, Santa Rosa, Riu Nord i Riu Sud",
                  "Singuerlín, Fondo, Can Mariner, Santa Rosa, Riu Nord and Riu Sud"),
         intro=L("Ofrecemos grúa 24 horas en Santa Coloma de Gramenet con salida inmediata hacia cualquier barrio de la ciudad.",
                 "Oferim grua 24 hores a Santa Coloma de Gramenet amb sortida immediata cap a qualsevol barri de la ciutat.",
                 "We offer a 24-hour tow truck service in Santa Coloma de Gramenet, setting off immediately to any part of the city.")),
    dict(slug="grua-sant-adria-de-besos", name="Sant Adrià de Besòs",
         near=L("en la desembocadura del Besòs, a pocos minutos del Fòrum y de la Ronda Litoral",
                "a la desembocadura del Besòs, a pocs minuts del Fòrum i de la Ronda Litoral",
                "at the mouth of the Besòs, a few minutes from the Fòrum and the Ronda Litoral"),
         roads=L("la Ronda Litoral, la C-31 y la B-10", "la Ronda Litoral, la C-31 i la B-10", "the Ronda Litoral, the C-31 and the B-10"),
         places=L("La Mina, Sant Joan Baptista, Besòs y el Port Fòrum",
                  "La Mina, Sant Joan Baptista, Besòs i el Port Fòrum",
                  "La Mina, Sant Joan Baptista, Besòs and Port Fòrum"),
         intro=L("Desde el Fòrum hasta La Mina, recogemos tu vehículo averiado o accidentado en Sant Adrià de Besòs a cualquier hora.",
                 "Del Fòrum a La Mina, recollim el teu vehicle avariat o accidentat a Sant Adrià de Besòs a qualsevol hora.",
                 "From the Fòrum to La Mina, we pick up your broken-down or damaged vehicle in Sant Adrià de Besòs at any time.")),
    dict(slug="grua-esplugues-de-llobregat", name="Esplugues de Llobregat",
         near=L("al final de la Diagonal, conectada con Barcelona por la Ronda de Dalt",
                "al final de la Diagonal, connectada amb Barcelona per la Ronda de Dalt",
                "at the end of Avinguda Diagonal, connected to Barcelona by the Ronda de Dalt"),
         roads=L("la B-23, la Ronda de Dalt y la N-340", "la B-23, la Ronda de Dalt i la N-340", "the B-23, the Ronda de Dalt and the N-340"),
         places=L("Can Vidalet, La Plana, Ciutat Diagonal y El Gall",
                  "Can Vidalet, La Plana, Ciutat Diagonal i El Gall",
                  "Can Vidalet, La Plana, Ciutat Diagonal and El Gall"),
         intro=L("En Esplugues y Ciutat Diagonal te ofrecemos asistencia en carretera rápida, también en los accesos a la Diagonal y la B-23.",
                 "A Esplugues i Ciutat Diagonal t'oferim assistència en carretera ràpida, també als accessos a la Diagonal i la B-23.",
                 "In Esplugues and Ciutat Diagonal we offer fast roadside assistance, including on the Diagonal and B-23 access roads.")),
    dict(slug="grua-sant-cugat-del-valles", name="Sant Cugat del Vallès",
         near=L("al otro lado de Collserola, a pocos minutos por los túneles de Vallvidrera (C-16)",
                "a l'altra banda de Collserola, a pocs minuts pels túnels de Vallvidrera (C-16)",
                "on the other side of Collserola, a few minutes away through the Vallvidrera tunnels (C-16)"),
         roads=L("la AP-7, la C-16 (túneles de Vallvidrera) y la B-30",
                 "l'AP-7, la C-16 (túnels de Vallvidrera) i la B-30",
                 "the AP-7, the C-16 (Vallvidrera tunnels) and the B-30"),
         places=L("el centro, Valldoreix, Mira-sol, Les Planes, La Floresta y el Parc Tecnològic del Vallès",
                  "el centre, Valldoreix, Mira-sol, Les Planes, La Floresta i el Parc Tecnològic del Vallès",
                  "the town centre, Valldoreix, Mira-sol, Les Planes, La Floresta and the Parc Tecnològic del Vallès"),
         intro=L("Cubrimos Sant Cugat y su entorno, incluidos los túneles de Vallvidrera, la AP-7 y las urbanizaciones de la zona.",
                 "Cobrim Sant Cugat i el seu entorn, inclosos els túnels de Vallvidrera, l'AP-7 i les urbanitzacions de la zona.",
                 "We cover Sant Cugat and the surrounding area, including the Vallvidrera tunnels, the AP-7 and the local residential estates.")),
    dict(slug="grua-sant-boi-de-llobregat", name="Sant Boi de Llobregat",
         near=L("en el Baix Llobregat, a pocos minutos de Barcelona por la B-23 y la C-32",
                "al Baix Llobregat, a pocs minuts de Barcelona per la B-23 i la C-32",
                "in the Baix Llobregat, a few minutes from Barcelona via the B-23 and the C-32"),
         roads=L("la C-32, la C-245, la B-23 y la A-2", "la C-32, la C-245, la B-23 i l'A-2", "the C-32, the C-245, the B-23 and the A-2"),
         places=L("Marianao, Casablanca, Camps Blancs, Ciutat Cooperativa, Cooperativa-Molí Nou y los polígonos industriales",
                  "Marianao, Casablanca, Camps Blancs, Ciutat Cooperativa, Cooperativa-Molí Nou i els polígons industrials",
                  "Marianao, Casablanca, Camps Blancs, Ciutat Cooperativa, Cooperativa-Molí Nou and the industrial estates"),
         intro=L("En Sant Boi atendemos averías y accidentes en el casco urbano, en los polígonos y en la C-32 y la C-245, a cualquier hora.",
                 "A Sant Boi atenem avaries i accidents al nucli urbà, als polígons i a la C-32 i la C-245, a qualsevol hora.",
                 "In Sant Boi we deal with breakdowns and accidents in town, in the industrial estates and on the C-32 and C-245, at any hour.")),
    dict(slug="grua-castelldefels", name="Castelldefels",
         near=L("en la costa del Baix Llobregat, conectada con Barcelona por la C-32 y la autovía de Castelldefels (C-31)",
                "a la costa del Baix Llobregat, connectada amb Barcelona per la C-32 i l'autovia de Castelldefels (C-31)",
                "on the Baix Llobregat coast, connected to Barcelona by the C-32 and the Castelldefels motorway (C-31)"),
         roads=L("la C-32, la C-31 (autovía de Castelldefels) y la C-245",
                 "la C-32, la C-31 (autovia de Castelldefels) i la C-245",
                 "the C-32, the C-31 (Castelldefels motorway) and the C-245"),
         places=L("la Platja, Montmar, Bellamar, Can Bou, el Poal y el Canal Olímpic",
                  "la Platja, Montmar, Bellamar, Can Bou, el Poal i el Canal Olímpic",
                  "the beach area, Montmar, Bellamar, Can Bou, El Poal and the Canal Olímpic"),
         intro=L("¿Avería volviendo de la playa o en la C-32? Damos servicio de grúa 24 horas en toda Castelldefels, incluidas las urbanizaciones de montaña.",
                 "Avaria tornant de la platja o a la C-32? Donem servei de grua 24 hores a tot Castelldefels, incloses les urbanitzacions de muntanya.",
                 "Broken down on the way back from the beach or on the C-32? We provide a 24-hour towing service throughout Castelldefels, including the hillside estates.")),
    dict(slug="grua-sitges", name="Sitges",
         near=L("en la costa del Garraf, conectada con Barcelona por la C-32 (túneles del Garraf) y la C-31",
                "a la costa del Garraf, connectada amb Barcelona per la C-32 (túnels del Garraf) i la C-31",
                "on the Garraf coast, connected to Barcelona by the C-32 (Garraf tunnels) and the C-31"),
         roads=L("la C-32 (autopista del Garraf) y la C-31 (carretera de las Costas del Garraf)",
                 "la C-32 (autopista del Garraf) i la C-31 (carretera de les Costes del Garraf)",
                 "the C-32 (Garraf motorway) and the C-31 (Garraf coast road)"),
         places=L("el centro, Terramar, Vallpineda, Levantina, Can Girona, el Port d'Aiguadolç, Garraf y Les Botigues de Sitges",
                  "el centre, Terramar, Vallpineda, Levantina, Can Girona, el Port d'Aiguadolç, Garraf i les Botigues de Sitges",
                  "the town centre, Terramar, Vallpineda, Levantina, Can Girona, Port d'Aiguadolç, Garraf and Les Botigues de Sitges"),
         intro=L("¿Avería en los túneles del Garraf, en la carretera de las Costas o paseando por Sitges? Damos servicio de grúa 24 horas en todo el municipio, de Garraf a Terramar.",
                 "Avaria als túnels del Garraf, a la carretera de les Costes o passejant per Sitges? Donem servei de grua 24 hores a tot el municipi, de Garraf a Terramar.",
                 "Broken down in the Garraf tunnels, on the coast road or around Sitges? We provide a 24-hour towing service across the whole municipality, from Garraf to Terramar.")),
    dict(slug="grua-gava", name="Gavà",
         near=L("entre Viladecans y Castelldefels, con acceso directo por la C-32 y la C-245",
                "entre Viladecans i Castelldefels, amb accés directe per la C-32 i la C-245",
                "between Viladecans and Castelldefels, with direct access via the C-32 and the C-245"),
         roads=L("la C-32, la C-245 y la autovía de Castelldefels",
                 "la C-32, la C-245 i l'autovia de Castelldefels",
                 "the C-32, the C-245 and the Castelldefels motorway"),
         places=L("el centro, Gavà Mar, Can Tries, Bruguers y el polígono de Les Massotes",
                  "el centre, Gavà Mar, Can Tries, Bruguers i el polígon de Les Massotes",
                  "the town centre, Gavà Mar, Can Tries, Bruguers and the Les Massotes industrial estate"),
         intro=L("Recogemos tu coche averiado o accidentado en Gavà y Gavà Mar, de día y de noche, y lo llevamos donde nos digas.",
                 "Recollim el teu cotxe avariat o accidentat a Gavà i Gavà Mar, de dia i de nit, i el portem on ens diguis.",
                 "We pick up your broken-down or damaged car in Gavà and Gavà Mar, day or night, and take it wherever you need.")),
    dict(slug="grua-viladecans", name="Viladecans",
         near=L("en el Baix Llobregat, junto a la C-32 y a pocos minutos del aeropuerto",
                "al Baix Llobregat, al costat de la C-32 i a pocs minuts de l'aeroport",
                "in the Baix Llobregat, next to the C-32 and a few minutes from the airport"),
         roads=L("la C-32, la C-245 y la autovía de Castelldefels",
                 "la C-32, la C-245 i l'autovia de Castelldefels",
                 "the C-32, the C-245 and the Castelldefels motorway"),
         places=L("el centro, Torre-roja, Montserratina, Alba-Rosa, Sales y el polígono Can Calderon",
                  "el centre, Torre-roja, Montserratina, Alba-Rosa, Sales i el polígon Can Calderon",
                  "the town centre, Torre-roja, Montserratina, Alba-Rosa, Sales and the Can Calderon industrial estate"),
         intro=L("Ofrecemos grúa y asistencia en carretera en Viladecans y sus polígonos industriales, con salida inmediata las 24 horas.",
                 "Oferim grua i assistència en carretera a Viladecans i als seus polígons industrials, amb sortida immediata les 24 hores.",
                 "We offer towing and roadside assistance in Viladecans and its industrial estates, setting off immediately 24 hours a day.")),
    dict(slug="grua-sant-feliu-de-llobregat", name="Sant Feliu de Llobregat",
         near=L("junto a la B-23, a pocos minutos de la Diagonal",
                "al costat de la B-23, a pocs minuts de la Diagonal",
                "next to the B-23, a few minutes from the Diagonal"),
         roads=L("la B-23, la N-340 y la AP-7", "la B-23, la N-340 i l'AP-7", "the B-23, the N-340 and the AP-7"),
         places=L("el centro, Mas Lluí, Can Calders, Les Grases y el polígono Eixample Nord",
                  "el centre, Mas Lluí, Can Calders, Les Grases i el polígon Eixample Nord",
                  "the town centre, Mas Lluí, Can Calders, Les Grases and the Eixample Nord industrial estate"),
         intro=L("En Sant Feliu de Llobregat te ayudamos con averías, pinchazos y accidentes, también en la B-23 y la N-340.",
                 "A Sant Feliu de Llobregat t'ajudem amb avaries, punxades i accidents, també a la B-23 i la N-340.",
                 "In Sant Feliu de Llobregat we help with breakdowns, flat tyres and accidents, including on the B-23 and the N-340.")),
    dict(slug="grua-sant-joan-despi", name="Sant Joan Despí",
         near=L("entre Cornellà y Sant Feliu, con salida directa a la B-23 y la Ronda de Dalt",
                "entre Cornellà i Sant Feliu, amb sortida directa a la B-23 i la Ronda de Dalt",
                "between Cornellà and Sant Feliu, with direct access to the B-23 and the Ronda de Dalt"),
         roads=L("la B-23, la N-340 y la Ronda de Dalt", "la B-23, la N-340 i la Ronda de Dalt", "the B-23, the N-340 and the Ronda de Dalt"),
         places=L("el centro, Les Planes, Torreblanca, el Pla del Llobregat y la Ciutat Esportiva del FC Barcelona",
                  "el centre, Les Planes, Torreblanca, el Pla del Llobregat i la Ciutat Esportiva del FC Barcelona",
                  "the town centre, Les Planes, Torreblanca, Pla del Llobregat and FC Barcelona's Ciutat Esportiva"),
         intro=L("Damos servicio de grúa 24 horas en Sant Joan Despí, tanto en el centro como en los accesos a la B-23.",
                 "Donem servei de grua 24 hores a Sant Joan Despí, tant al centre com als accessos a la B-23.",
                 "We provide a 24-hour towing service in Sant Joan Despí, both in the centre and on the B-23 access roads.")),
    dict(slug="grua-montcada-i-reixac", name="Montcada i Reixac",
         near=L("al norte de Barcelona, conectada por la C-17, la C-33 y la B-20",
                "al nord de Barcelona, connectada per la C-17, la C-33 i la B-20",
                "north of Barcelona, connected by the C-17, the C-33 and the B-20"),
         roads=L("la C-17, la C-33, la C-58 y la B-30", "la C-17, la C-33, la C-58 i la B-30", "the C-17, the C-33, the C-58 and the B-30"),
         places=L("Montcada Centre, Can Sant Joan, La Ribera, Terra Nostra, Can Cuiàs y Mas Rampinyo",
                  "Montcada Centre, Can Sant Joan, La Ribera, Terra Nostra, Can Cuiàs i Mas Rampinyo",
                  "Montcada Centre, Can Sant Joan, La Ribera, Terra Nostra, Can Cuiàs and Mas Rampinyo"),
         intro=L("Atendemos averías y accidentes en Montcada i Reixac y en las vías de alta capacidad que la cruzan, como la C-17, la C-33 y la C-58.",
                 "Atenem avaries i accidents a Montcada i Reixac i a les vies d'alta capacitat que la travessen, com la C-17, la C-33 i la C-58.",
                 "We handle breakdowns and accidents in Montcada i Reixac and on the major roads that cross it, such as the C-17, C-33 and C-58.")),
    dict(slug="grua-cerdanyola-del-valles", name="Cerdanyola del Vallès",
         near=L("en el Vallès Occidental, al otro lado de Collserola, con acceso por la AP-7 y la C-58",
                "al Vallès Occidental, a l'altra banda de Collserola, amb accés per l'AP-7 i la C-58",
                "in the Vallès Occidental, on the other side of Collserola, with access via the AP-7 and the C-58"),
         roads=L("la AP-7, la C-58, la B-30 y la BV-1414", "l'AP-7, la C-58, la B-30 i la BV-1414", "the AP-7, the C-58, the B-30 and the BV-1414"),
         places=L("el centro, Serraparera, Montflorit, Bellaterra, la UAB y el Parc de l'Alba",
                  "el centre, Serraparera, Montflorit, Bellaterra, la UAB i el Parc de l'Alba",
                  "the town centre, Serraparera, Montflorit, Bellaterra, the UAB campus and the Parc de l'Alba"),
         intro=L("Cubrimos Cerdanyola del Vallès, Bellaterra y la zona de la UAB con grúa 24 horas, también en la AP-7 y la C-58.",
                 "Cobrim Cerdanyola del Vallès, Bellaterra i la zona de la UAB amb grua 24 hores, també a l'AP-7 i la C-58.",
                 "We cover Cerdanyola del Vallès, Bellaterra and the UAB area with a 24-hour tow truck, including on the AP-7 and C-58.")),
]

FAQ = [
    (L("¿Cuánto tarda la grúa?", "Quant triga la grua?", "How long does the tow truck take?"),
     L("Salimos en cuanto nos llamas o nos envías tu ubicación por WhatsApp. Te damos la hora estimada de llegada al momento.",
       "Sortim tan bon punt ens truques o ens envies la teva ubicació per WhatsApp. Et donem l'hora estimada d'arribada a l'instant.",
       "We set off as soon as you call or send us your location on WhatsApp. We'll give you an estimated arrival time straight away.")),
    (L("¿Cuánto cuesta una grúa en Barcelona?", "Quant costa una grua a Barcelona?", "How much does a tow truck cost in Barcelona?"),
     L("Depende de la distancia, el vehículo y la hora. Mándanos ubicación y destino por WhatsApp y te damos un precio cerrado y sin compromiso antes de salir.",
       "Depèn de la distància, el vehicle i l'hora. Envia'ns ubicació i destinació per WhatsApp i et donem un preu tancat i sense compromís abans de sortir.",
       "It depends on the distance, the vehicle and the time of day. Send us your location and destination on WhatsApp and we'll give you a fixed, no-obligation price before setting off.")),
    (L("¿Trabajáis de noche y festivos?", "Treballeu de nit i en festius?", "Do you work nights and holidays?"),
     L("Sí, 24 horas, los 365 días del año.", "Sí, 24 hores, els 365 dies de l'any.", "Yes, 24 hours a day, 365 days a year.")),
    (L("¿Lleváis el coche a mi taller?", "Porteu el cotxe al meu taller?", "Can you take the car to my garage?"),
     L("Sí, al taller, concesionario o domicilio que nos digas, dentro y fuera de Barcelona.",
       "Sí, al taller, concessionari o domicili que ens diguis, dins i fora de Barcelona.",
       "Yes, to whichever garage, dealership or address you choose, in or outside Barcelona.")),
    (L("¿Y si mi seguro tarda o no me cubre?", "I si l'assegurança triga o no em cobreix?", "What if my insurance is slow or doesn't cover me?"),
     L("Puedes pedir el servicio de forma particular: el profesional que lo realice te entregará la factura para que la reclames a tu aseguradora.",
       "Pots demanar el servei de manera particular: el professional que el faci et lliurarà la factura perquè la reclamis a la teva asseguradora.",
       "You can book the service privately: the professional who carries it out will give you an invoice so you can claim it from your insurer.")),
    (L("¿Qué hago si me quedo parado en una ronda o autopista?", "Què faig si em quedo aturat en una ronda o autopista?",
       "What should I do if I break down on a ring road or motorway?"),
     L("Ponte el chaleco, activa la baliza V-16, sal detrás del guardarraíl y llámanos. Cubrimos rondas, Gran Via, Diagonal, C-31, C-32, C-58, A-2, AP-7 y B-23.",
       "Posa't l'armilla, activa la balisa V-16, surt darrere de la tanca de seguretat i truca'ns. Cobrim rondes, Gran Via, Diagonal, C-31, C-32, C-58, A-2, AP-7 i B-23.",
       "Put on your hi-vis vest, switch on your V-16 beacon, get behind the crash barrier and call us. We cover the ring roads, Gran Via, Diagonal, C-31, C-32, C-58, A-2, AP-7 and B-23.")),
]


SERVICE_PAGES = {
    "falta-combustible-barcelona": dict(
        h1=L("Sin gasolina en Barcelona", "Sense benzina a Barcelona", "Out of fuel in Barcelona"),
        title=L("Sin Gasolina en Barcelona: Asistencia 24h", "Sense Benzina a Barcelona: Assistència 24h", "Out of Fuel in Barcelona: 24h Assistance"),
        desc=L("¿Te has quedado sin gasolina o diésel en Barcelona? Te llevamos combustible o el coche a la gasolinera, 24 horas. Llama al 671 44 86 39.",
               "T'has quedat sense benzina o gasoil a Barcelona? Et portem combustible o portem el cotxe a la benzinera, 24 hores. Truca al 671 44 86 39.",
               "Run out of petrol or diesel in Barcelona? We bring you fuel or take your car to a petrol station, 24 hours a day. Call 671 44 86 39."),
        intro=L("¿Te has quedado sin combustible? Te lo llevamos o remolcamos el coche a la gasolinera más cercana.",
                "T'has quedat sense combustible? Te'l portem o remolquem el cotxe fins a la benzinera més propera.",
                "Run out of fuel? We'll bring it to you or tow your car to the nearest petrol station."),
        sections=[
            (L("Combustible donde estés", "Combustible on siguis", "Fuel wherever you are"),
             L("Gasolina o diésel para llegar a la gasolinera.", "Benzina o gasoil per arribar a la benzinera.", "Petrol or diesel to get you to the petrol station.")),
            (L("Rondas y autopistas", "Rondes i autopistes", "Ring roads and motorways"),
             L("Te sacamos de la vía rápida con seguridad.", "Et traiem de la via ràpida amb seguretat.", "We get you off the fast road safely.")),
            (L("¿Combustible equivocado?", "Combustible equivocat?", "Wrong fuel?"),
             L("Si has repostado mal, no arranques: lo llevamos al taller.", "Si has repostat malament, no engeguis el motor: el portem al taller.",
               "If you've filled up with the wrong fuel, don't start the engine: we'll take it to the garage.")),
        ],
        faq=[(L("¿Qué hago si me quedo sin gasolina en la ronda?", "Què faig si em quedo sense benzina a la ronda?", "What should I do if I run out of fuel on the ring road?"),
              L("Sal del carril si puedes, ponte el chaleco, activa la baliza V-16 y llámanos.",
                "Surt del carril si pots, posa't l'armilla, activa la balisa V-16 i truca'ns.",
                "Get out of the lane if you can, put on your hi-vis vest, switch on your V-16 beacon and call us.")),
             (L("¿Y si he echado gasolina en un diésel?", "I si he posat benzina en un dièsel?", "What if I've put petrol in a diesel?"),
              L("No arranques el motor. Lo llevamos en grúa al taller para vaciar el depósito.",
                "No engeguis el motor. El portem amb grua al taller per buidar el dipòsit.",
                "Don't start the engine. We'll tow it to the garage so the tank can be drained."))]),
    "traslado-itv-taller-barcelona": dict(
        h1=L("Traslado a ITV y taller en Barcelona", "Trasllat a l'ITV i al taller a Barcelona", "Transfers to ITV and garage in Barcelona"),
        title=L("Traslado de Coches a ITV y Taller en Barcelona", "Trasllat de Cotxes a l'ITV i al Taller a Barcelona", "Car Transfers to ITV and Garage in Barcelona"),
        desc=L("Llevamos en grúa tu coche sin ITV, sin seguro o que no puede circular al taller o a la estación de ITV en Barcelona. Llama al 671 44 86 39.",
               "Portem amb grua el teu cotxe sense ITV, sense assegurança o que no pot circular al taller o a l'estació d'ITV a Barcelona. Truca al 671 44 86 39.",
               "We tow your car to the garage or the ITV inspection station in Barcelona if it has no valid ITV, no insurance or can't be driven. Call 671 44 86 39."),
        intro=L("Movemos en grúa los coches que no pueden circular: sin ITV, sin batería o con la ITV desfavorable.",
                "Movem amb grua els cotxes que no poden circular: sense ITV, sense bateria o amb l'ITV desfavorable.",
                "We tow cars that can't be driven: no valid ITV (vehicle inspection), a flat battery or a failed inspection."),
        sections=[
            (L("A la estación de ITV", "A l'estació d'ITV", "To the ITV station"),
             L("Llevamos y traemos tu coche a la cita.", "Portem i tornem el teu cotxe a la cita.", "We take your car to its appointment and bring it back.")),
            (L("Al taller que elijas", "Al taller que triïs", "To the garage of your choice"),
             L("Tu taller de confianza o el concesionario.", "El teu taller de confiança o el concessionari.", "Your trusted garage or the dealership.")),
            (L("Coches parados mucho tiempo", "Cotxes aturats molt de temps", "Cars left unused for a long time"),
             L("Sin batería, sin seguro o sin ITV en vigor.", "Sense bateria, sense assegurança o sense ITV en vigor.", "Flat battery, no insurance or an expired ITV.")),
        ],
        faq=[(L("¿Puedo llevar a la ITV un coche con la ITV caducada?", "Puc portar a l'ITV un cotxe amb l'ITV caducada?", "Can I take a car with an expired ITV to the inspection?"),
              L("Conducirlo puede suponer una multa. En grúa lo trasladas sin riesgo.", "Conduir-lo pot suposar una multa. Amb grua el trasllades sense risc.",
                "Driving it could get you a fine. By tow truck you can move it with no risk.")),
             (L("¿Podéis esperar y traer el coche de vuelta?", "Podeu esperar i tornar el cotxe?", "Can you wait and bring the car back?"),
              L("Sí, organizamos ida y vuelta. Pídenos precio.", "Sí, organitzem anada i tornada. Demana'ns preu.", "Yes, we arrange return trips. Ask us for a price."))]),
    "remolque-coches-barcelona": dict(
        h1=L("Remolque de coches en Barcelona", "Remolc de cotxes a Barcelona", "Car towing in Barcelona"),
        title=L("Remolque de Coches Barcelona 24h", "Remolc de Cotxes Barcelona 24h", "Car Towing Barcelona 24h"),
        desc=L("Remolque de coches averiados en Barcelona las 24 horas. Grúa de plataforma, traslado al taller o domicilio y presupuesto al momento.",
               "Remolc de cotxes avariats a Barcelona les 24 hores. Grua de plataforma, trasllat al taller o a domicili i pressupost a l'instant.",
               "Broken-down car towing in Barcelona, 24 hours a day. Flatbed tow truck, transport to the garage or your home and an instant quote."),
        intro=L("¿Tu coche se ha parado? Lo llevamos en grúa al taller, concesionario o a tu casa.",
                "El teu cotxe s'ha aturat? El portem amb grua al taller, al concessionari o a casa teva.",
                "Has your car stopped? We'll tow it to the garage, the dealership or your home."),
        sections=[
            (L("Grúa de plataforma: tu coche no sufre", "Grua de plataforma: el teu cotxe no pateix", "Flatbed tow truck: no strain on your car"),
             L("Lo cargamos sin arrastrarlo: ideal para automáticos y eléctricos.", "El carreguem sense arrossegar-lo: ideal per a automàtics i elèctrics.",
               "We load it without dragging it: ideal for automatics and electric cars.")),
            (L("Coches, furgonetas, eléctricos y 4x4", "Cotxes, furgonetes, elèctrics i 4x4", "Cars, vans, EVs and 4x4s"),
             L("Turismos, furgonetas, SUV, híbridos y eléctricos.", "Turismes, furgonetes, SUV, híbrids i elèctrics.", "Cars, vans, SUVs, hybrids and electric vehicles.")),
            (L("A tu taller de confianza o a donde necesites", "Al teu taller de confiança o on necessitis", "To your trusted garage or wherever you need"),
             L("Taller, concesionario o tu casa: tú eliges.", "Taller, concessionari o casa teva: tu tries.", "Garage, dealership or home: you choose.")),
        ],
        faq=[(L("¿Podéis remolcar un coche automático o eléctrico?", "Podeu remolcar un cotxe automàtic o elèctric?", "Can you tow an automatic or electric car?"),
              L("Sí. Usamos grúa de plataforma, que carga el vehículo entero sin que las ruedas giren, que es la forma recomendada por los fabricantes para coches automáticos, eléctricos e híbridos.",
                "Sí. Utilitzem grua de plataforma, que carrega el vehicle sencer sense que les rodes girin, que és la manera recomanada pels fabricants per a cotxes automàtics, elèctrics i híbrids.",
                "Yes. We use a flatbed tow truck, which carries the whole vehicle without the wheels turning, the method manufacturers recommend for automatic, electric and hybrid cars.")),
             (L("¿Puedo ir en la grúa con mi coche?", "Puc anar a la grua amb el meu cotxe?", "Can I ride in the tow truck with my car?"),
              L("Normalmente sí, puedes acompañarnos en la cabina hasta el destino. Coméntalo al pedir el servicio.",
                "Normalment sí, pots acompanyar-nos a la cabina fins a la destinació. Comenta-ho quan demanis el servei.",
                "Usually yes, you can ride with us in the cab to the destination. Just mention it when you book."))]),
    "grua-accidente-barcelona": dict(
        h1=L("Grúa por accidente en Barcelona", "Grua per accident a Barcelona", "Accident towing in Barcelona"),
        title=L("Grúa por Accidente en Barcelona 24h", "Grua per Accident a Barcelona 24h", "Accident Tow Truck in Barcelona 24h"),
        desc=L("Grúa tras accidente en Barcelona 24h: retirada de vehículos siniestrados en calles, rondas y autopistas. Salida inmediata. Llama al 671 44 86 39.",
               "Grua després d'un accident a Barcelona 24h: retirada de vehicles sinistrats a carrers, rondes i autopistes. Sortida immediata. Truca al 671 44 86 39.",
               "Tow truck after an accident in Barcelona 24h: removal of damaged vehicles from streets, ring roads and motorways. Immediate dispatch. Call 671 44 86 39."),
        intro=L("Retiramos tu vehículo de la calle, la ronda o la autopista y lo llevamos donde nos digas.",
                "Retirem el teu vehicle del carrer, la ronda o l'autopista i el portem on ens diguis.",
                "We remove your vehicle from the street, ring road or motorway and take it wherever you tell us."),
        sections=[
            (L("Qué hacer tras un accidente", "Què fer després d'un accident", "What to do after an accident"),
             L("Ponte a salvo, llama al 112 si hay heridos y después a nosotros.", "Posa't a salvo, truca al 112 si hi ha ferits i després a nosaltres.",
               "Get to safety, call 112 if anyone is injured, then call us.")),
            (L("Rondas, autopistas y vías rápidas", "Rondes, autopistes i vies ràpides", "Ring roads, motorways and expressways"),
             L("Rondas, Gran Via, C-31, C-32, A-2, AP-7 y B-23.", "Rondes, Gran Via, C-31, C-32, A-2, AP-7 i B-23.", "Ring roads, Gran Via, C-31, C-32, A-2, AP-7 and B-23.")),
            (L("Si tu seguro tarda", "Si la teva assegurança triga", "If your insurer is slow"),
             L("Puedes pedirlo de forma particular y reclamar la factura a tu seguro.", "Pots demanar-lo de manera particular i reclamar la factura a l'assegurança.",
               "You can book it privately and claim the invoice from your insurer.")),
        ],
        faq=[(L("¿Trabajáis con seguros?", "Treballeu amb assegurances?", "Do you work with insurance companies?"),
              L("Puedes pedir el servicio de forma particular: el profesional que lo realice te dará la factura detallada para que la presentes a tu aseguradora. Consúltanos tu caso concreto.",
                "Pots demanar el servei de manera particular: el professional que el faci et donarà la factura detallada perquè la presentis a la teva asseguradora. Consulta'ns el teu cas concret.",
                "You can book the service privately: the professional who carries it out will give you an itemised invoice to submit to your insurer. Ask us about your specific case.")),
             (L("¿Retiráis coches que no ruedan?", "Retireu cotxes que no roden?", "Do you remove cars that can't roll?"),
              L("Sí. Los vehículos accidentados con ruedas o dirección dañadas se cargan con la plataforma y el cabrestante de la grúa.",
                "Sí. Els vehicles accidentats amb les rodes o la direcció danyades es carreguen amb la plataforma i el cabrestant de la grua.",
                "Yes. Accident-damaged vehicles with broken wheels or steering are loaded using the truck's flatbed and winch."))]),
    "arranque-bateria-barcelona": dict(
        h1=L("Arranque de batería en Barcelona", "Arrencada de bateria a Barcelona", "Battery jump-start in Barcelona"),
        title=L("Arranque de Batería Barcelona 24h a Domicilio", "Arrencada de Bateria Barcelona 24h a Domicili", "Battery Jump-Start Barcelona 24h, We Come to You"),
        desc=L("¿Tu coche no arranca? Arranque de batería a domicilio en Barcelona 24h, en la calle o en tu parking. Llegamos rápido. Llama o WhatsApp 671 44 86 39.",
               "El teu cotxe no arrenca? Arrencada de bateria a domicili a Barcelona 24h, al carrer o al teu pàrquing. Arribem ràpid. Truca o WhatsApp 671 44 86 39.",
               "Car won't start? Mobile battery jump-start in Barcelona 24h, on the street or in your car park. We get there fast. Call or WhatsApp 671 44 86 39."),
        intro=L("¿El coche no arranca? Vamos a donde estés, en la calle o en tu parking.",
                "El cotxe no arrenca? Venim on siguis, al carrer o al teu pàrquing.",
                "Car won't start? We come to you, on the street or in your car park."),
        sections=[
            (L("Arranque en el sitio", "Arrencada al mateix lloc", "On-the-spot jump-start"),
             L("Equipo profesional, sin necesidad de otro coche.", "Equip professional, sense necessitat d'un altre cotxe.", "Professional equipment, no second car needed.")),
            (L("Cuando la batería está agotada", "Quan la bateria està esgotada", "When the battery is dead"),
             L("Si no carga, te llevamos al taller o te ayudamos a cambiarla.", "Si no carrega, et portem al taller o t'ajudem a canviar-la.",
               "If it won't charge, we take you to the garage or help you replace it.")),
            (L("Señales de batería débil", "Senyals de bateria feble", "Signs of a weak battery"),
             L("Arranque lento o luces que parpadean: revísala a tiempo.", "Arrencada lenta o llums que parpellegen: revisa-la a temps.",
               "Slow cranking or flickering lights: get it checked in time.")),
        ],
        faq=[(L("¿Venís a parkings subterráneos?", "Veniu a pàrquings subterranis?", "Do you come to underground car parks?"),
              L("Sí, el arranque de batería se puede hacer en casi cualquier parking, porque no hace falta meter la grúa.",
                "Sí, l'arrencada de bateria es pot fer gairebé a qualsevol pàrquing, perquè no cal fer entrar la grua.",
                "Yes, a jump-start can be done in almost any car park, since the tow truck doesn't need to get in.")),
             (L("¿Cuánto tarda el arranque?", "Quant triga l'arrencada?", "How long does a jump-start take?"),
              L("Una vez en el sitio, el arranque suele llevar solo unos minutos.", "Un cop allà, l'arrencada sol durar només uns minuts.",
                "Once we're there, it usually takes just a few minutes."))]),
    "cambio-rueda-pinchazo-barcelona": dict(
        h1=L("Pinchazo y cambio de rueda en Barcelona", "Punxada i canvi de roda a Barcelona", "Flat tyre and wheel change in Barcelona"),
        title=L("Pinchazo y Cambio de Rueda Barcelona 24h", "Punxada i Canvi de Roda Barcelona 24h", "Flat Tyre and Wheel Change Barcelona 24h"),
        desc=L("¿Has pinchado? Cambio de rueda en Barcelona 24h, en la calle, la ronda o la autopista. Sin repuesto, te llevamos al taller. Llama al 671 44 86 39.",
               "Has punxat? Canvi de roda a Barcelona 24h, al carrer, a la ronda o a l'autopista. Sense recanvi, et portem al taller. Truca al 671 44 86 39.",
               "Got a flat? Wheel change in Barcelona 24h, on the street, ring road or motorway. No spare? We'll take you to the garage. Call 671 44 86 39."),
        intro=L("Cambiamos la rueda en el sitio o llevamos el coche al taller.",
                "Canviem la roda al mateix lloc o portem el cotxe al taller.",
                "We change the wheel on the spot or take the car to the garage."),
        sections=[
            (L("Cambio de rueda en el momento", "Canvi de roda a l'instant", "Wheel change on the spot"),
             L("Ponemos tu rueda de repuesto de forma segura.", "Posem la teva roda de recanvi de manera segura.", "We fit your spare wheel safely.")),
            (L("Sin rueda de repuesto", "Sense roda de recanvi", "No spare wheel"),
             L("Si el kit antipinchazos no basta, te llevamos al taller.", "Si el kit antipunxades no és suficient, et portem al taller.",
               "If the puncture repair kit isn't enough, we'll take you to the garage.")),
        ],
        faq=[(L("¿Qué hago si pincho en la autopista?", "Què faig si punxo a l'autopista?", "What should I do if I get a flat on the motorway?"),
              L("Sal de la calzada si puedes, ponte el chaleco, coloca la señal V-16 y espera detrás del guardarraíl. Llámanos y no intentes cambiar la rueda en el carril.",
                "Surt de la calçada si pots, posa't l'armilla, col·loca el senyal V-16 i espera darrere de la tanca de seguretat. Truca'ns i no intentis canviar la roda al carril.",
                "Pull off the carriageway if you can, put on your hi-vis vest, switch on your V-16 beacon and wait behind the crash barrier. Call us and don't try to change the wheel in the lane.")),
             (L("¿Cambiáis ruedas de furgonetas?", "Canvieu rodes de furgonetes?", "Do you change van tyres?"),
              L("Sí, cambiamos ruedas de turismos, SUV y furgonetas.", "Sí, canviem rodes de turismes, SUV i furgonetes.", "Yes, we change wheels on cars, SUVs and vans."))]),
    "grua-motos-barcelona": dict(
        h1=L("Grúa para motos en Barcelona", "Grua per a motos a Barcelona", "Motorbike towing in Barcelona"),
        title=L("Grúa para Motos en Barcelona 24h", "Grua per a Motos a Barcelona 24h", "Motorbike Tow Truck in Barcelona 24h"),
        desc=L("Grúa para motos y scooters en Barcelona 24h. Traslado seguro con anclajes específicos, por avería o accidente. Llama o WhatsApp 671 44 86 39.",
               "Grua per a motos i escúters a Barcelona 24h. Trasllat segur amb ancoratges específics, per avaria o accident. Truca o WhatsApp 671 44 86 39.",
               "Tow truck for motorbikes and scooters in Barcelona 24h. Safe transport with dedicated tie-downs, after a breakdown or accident. Call or WhatsApp 671 44 86 39."),
        intro=L("Recogemos tu moto o scooter averiado o accidentado y lo llevamos al taller o a casa.",
                "Recollim la teva moto o escúter avariat o accidentat i el portem al taller o a casa.",
                "We collect your broken-down or crashed motorbike or scooter and take it to the garage or home."),
        sections=[
            (L("Transporte seguro de motos", "Transport segur de motos", "Safe motorbike transport"),
             L("Calzos y cinchas específicos, sin dañar el carenado.", "Calços i cintes específics, sense danyar el carenat.",
               "Dedicated wheel chocks and straps, without damaging the fairing.")),
            (L("Scooters, motos grandes y eléctricas", "Escúters, motos grans i elèctriques", "Scooters, big bikes and electric bikes"),
             L("Desde scooters de 125 cc hasta motos de gran cilindrada.", "Des d'escúters de 125 cc fins a motos de gran cilindrada.",
               "From 125cc scooters to large-displacement motorbikes.")),
        ],
        faq=[(L("¿Recogéis motos sin llaves?", "Recolliu motos sense claus?", "Do you collect motorbikes without keys?"),
              L("Depende del caso. Consúltanos: necesitamos comprobar que eres el titular o tienes autorización.",
                "Depèn del cas. Consulta'ns: hem de comprovar que n'ets el titular o que tens autorització.",
                "It depends. Ask us: we need to check that you're the owner or have authorisation.")),
             (L("¿Podéis llevar mi moto a la ITV o a otra ciudad?", "Podeu portar la meva moto a l'ITV o a una altra ciutat?", "Can you take my motorbike to the ITV or another city?"),
              L("Sí, hacemos traslados programados de motos a la ITV, al taller o a cualquier ciudad de España.",
                "Sí, fem trasllats programats de motos a l'ITV, al taller o a qualsevol ciutat d'Espanya.",
                "Yes, we do scheduled motorbike transfers to the ITV, the garage or any city in Spain."))]),
    "transporte-vehiculos-barcelona": dict(
        h1=L("Transporte de vehículos desde Barcelona", "Transport de vehicles des de Barcelona", "Vehicle transport from Barcelona"),
        title=L("Transporte de Vehículos Barcelona | Toda España", "Transport de Vehicles Barcelona | Tot Espanya", "Vehicle Transport Barcelona | All of Spain"),
        desc=L("Transporte de coches y motos desde Barcelona a toda España. Traslados programados, compraventa, mudanzas y talleres. Presupuesto cerrado: 671 44 86 39.",
               "Transport de cotxes i motos des de Barcelona a tot Espanya. Trasllats programats, compravenda, mudances i tallers. Pressupost tancat: 671 44 86 39.",
               "Car and motorbike transport from Barcelona to anywhere in Spain. Scheduled transfers, vehicle sales, house moves and garages. Fixed quote: 671 44 86 39."),
        intro=L("Llevamos tu coche o moto puerta a puerta, con precio cerrado.",
                "Portem el teu cotxe o moto porta a porta, amb preu tancat.",
                "We take your car or motorbike door to door, at a fixed price."),
        sections=[
            (L("Traslados programados", "Trasllats programats", "Scheduled transfers"),
             L("Tú eliges día, hora y lugar de entrega.", "Tu tries dia, hora i lloc de lliurament.", "You choose the day, time and delivery location.")),
            (L("Dentro de Cataluña y a toda España", "Dins de Catalunya i a tot Espanya", "Within Catalonia and all over Spain"),
             L("Girona, Tarragona, Lleida, Madrid, Valencia y más.", "Girona, Tarragona, Lleida, Madrid, València i més.", "Girona, Tarragona, Lleida, Madrid, Valencia and more.")),
        ],
        faq=[(L("¿Cómo se calcula el precio de un traslado largo?", "Com es calcula el preu d'un trasllat llarg?", "How is the price of a long-distance transfer calculated?"),
              L("Según los kilómetros, el tipo de vehículo y la fecha. Envíanos origen, destino y modelo por WhatsApp y te damos un precio cerrado.",
                "Segons els quilòmetres, el tipus de vehicle i la data. Envia'ns origen, destinació i model per WhatsApp i et donem un preu tancat.",
                "Based on the distance, the type of vehicle and the date. Send us the origin, destination and model on WhatsApp and we'll give you a fixed price.")),
             (L("¿Transportáis coches que no funcionan?", "Transporteu cotxes que no funcionen?", "Do you transport cars that don't run?"),
              L("Sí, el vehículo no necesita arrancar: se carga con el cabrestante de la grúa.",
                "Sí, no cal que el vehicle arrenqui: es carrega amb el cabrestant de la grua.",
                "Yes, the vehicle doesn't need to start: it's loaded with the truck's winch."))]),
    "retirada-coches-desguace-barcelona": dict(
        h1=L("Retirada de coches para desguace en Barcelona", "Retirada de cotxes per a desballestament a Barcelona", "Scrap car collection in Barcelona"),
        title=L("Retirada de Coches para Desguace en Barcelona", "Retirada de Cotxes per a Desballestament a Barcelona", "Scrap Car Collection in Barcelona"),
        desc=L("Retiramos tu coche viejo, averiado o siniestrado en Barcelona y lo llevamos a un desguace autorizado para darlo de baja. Llama al 671 44 86 39.",
               "Retirem el teu cotxe vell, avariat o sinistrat a Barcelona i el portem a un desballestament autoritzat per donar-lo de baixa. Truca al 671 44 86 39.",
               "We collect your old, broken-down or written-off car in Barcelona and take it to an authorised scrapyard for deregistration. Call 671 44 86 39."),
        intro=L("Recogemos tu coche viejo y lo llevamos a un desguace autorizado para darlo de baja.",
                "Recollim el teu cotxe vell i el portem a un desballestament autoritzat per donar-lo de baixa.",
                "We collect your old car and take it to an authorised scrapyard to be deregistered."),
        sections=[
            (L("Baja oficial en la DGT", "Baixa oficial a la DGT", "Official deregistration with the DGT"),
             L("Te llevamos a un desguace autorizado que tramita la baja.", "Et portem a un desballestament autoritzat que tramita la baixa.",
               "We take it to an authorised scrapyard that handles the deregistration.")),
            (L("Qué necesitas", "Què necessites", "What you need"),
             L("Permiso de circulación, ficha técnica y DNI del titular.", "Permís de circulació, fitxa tècnica i DNI del titular.",
               "Vehicle registration certificate, technical data sheet and the owner's ID.")),
        ],
        faq=[(L("¿Recogéis coches sin ITV o sin batería?", "Recolliu cotxes sense ITV o sense bateria?", "Do you collect cars without a valid ITV or with a flat battery?"),
              L("Sí, el coche no necesita arrancar ni tener la ITV en vigor para que lo retiremos.",
                "Sí, no cal que el cotxe arrenqui ni que tingui l'ITV en vigor perquè el retirem.",
                "Yes, the car doesn't need to start or have a valid ITV for us to collect it.")),
             (L("¿Recogéis en parkings comunitarios?", "Recolliu en pàrquings comunitaris?", "Do you collect from residential car parks?"),
              L("Sí, en la mayoría de los casos. Indícanos la altura del parking y el acceso.",
                "Sí, en la majoria dels casos. Indica'ns l'alçada del pàrquing i l'accés.",
                "Yes, in most cases. Let us know the car park's height clearance and access."))]),
}

NOTA_COLABORADORES = L(
    "Algunos servicios pueden ser realizados por profesionales autónomos o empresas colaboradoras independientes. "
    "En estos casos, el servicio será ejecutado y cobrado directamente por el colaborador asignado, quien actuará como "
    "profesional independiente. Al solicitar el servicio, el cliente acepta que la prestación pueda ser realizada por uno de nuestros colaboradores.",
    "Alguns serveis poden ser realitzats per professionals autònoms o empreses col·laboradores independents. "
    "En aquests casos, el servei serà executat i cobrat directament pel col·laborador assignat, que actuarà com a "
    "professional independent. En sol·licitar el servei, el client accepta que la prestació pugui ser realitzada per un dels nostres col·laboradors.",
    "Some services may be carried out by self-employed professionals or independent partner companies. "
    "In such cases, the service will be performed and charged directly by the assigned partner, acting as an "
    "independent professional. By requesting the service, the customer accepts that it may be provided by one of our partners.")

RED = (L("Amplia red de profesionales colaboradores", "Àmplia xarxa de professionals col·laboradors", "A wide network of partner professionals"), [
    L("Contamos con una amplia red de profesionales autónomos y empresas colaboradoras independientes especializados en asistencia en carretera, transporte y traslado de vehículos.",
      "Comptem amb una àmplia xarxa de professionals autònoms i empreses col·laboradores independents especialitzats en assistència en carretera, transport i trasllat de vehicles.",
      "We work with a wide network of self-employed professionals and independent partner companies specialising in roadside assistance and vehicle transport."),
    L("Gracias a nuestra red de colaboradores podemos ofrecer una mayor cobertura geográfica, rapidez de respuesta y disponibilidad, adaptándonos a las necesidades de cada servicio.",
      "Gràcies a la nostra xarxa de col·laboradors podem oferir una cobertura geogràfica més àmplia, rapidesa de resposta i disponibilitat, i adaptar-nos a les necessitats de cada servei.",
      "Thanks to our partner network we can offer wider geographical coverage, faster response times and greater availability, adapting to the needs of each job."),
    L("Cuando recibimos una solicitud, podemos asignarla a uno de nuestros colaboradores disponibles en la zona correspondiente, en función de las características y necesidades del servicio.",
      "Quan rebem una sol·licitud, podem assignar-la a un dels nostres col·laboradors disponibles a la zona corresponent, en funció de les característiques i necessitats del servei.",
      "When we receive a request, we may assign it to one of our available partners in the relevant area, depending on the characteristics and needs of the service."),
])

FUNCIONAMIENTO = [  # (título, párrafos) — portada y Condiciones de servicio
    (L("Gestión e intermediación de servicios", "Gestió i intermediació de serveis", "Service management and intermediation"), [
        L("Nuestra empresa se encarga de recibir, gestionar y coordinar solicitudes de asistencia y transporte de vehículos, poniendo al cliente en contacto con profesionales colaboradores independientes.",
          "La nostra empresa s'encarrega de rebre, gestionar i coordinar sol·licituds d'assistència i transport de vehicles, i posa el client en contacte amb professionals col·laboradors independents.",
          "Our company receives, manages and coordinates requests for vehicle assistance and transport, putting customers in touch with independent partner professionals."),
        L("Una vez aceptado el servicio, el colaborador asignado se encarga de realizar directamente la prestación utilizando sus propios vehículos, medios y recursos profesionales.",
          "Un cop acceptat el servei, el col·laborador assignat s'encarrega de fer directament la prestació amb els seus propis vehicles, mitjans i recursos professionals.",
          "Once the service has been accepted, the assigned partner carries it out directly using their own vehicles, equipment and professional resources."),
        L("El colaborador será quien preste materialmente el servicio y cobre directamente al cliente por el trabajo realizado.",
          "El col·laborador serà qui presti materialment el servei i cobri directament al client pel treball realitzat.",
          "The partner is the one who physically provides the service and charges the customer directly for the work done.")]),
    (L("Profesionales independientes", "Professionals independents", "Independent professionals"), [
        L("Los servicios pueden ser realizados por profesionales autónomos o empresas colaboradoras independientes.",
          "Els serveis poden ser realitzats per professionals autònoms o empreses col·laboradores independents.",
          "Services may be carried out by self-employed professionals or independent partner companies."),
        L("Cada colaborador desarrolla su actividad por cuenta propia y es responsable de disponer de los vehículos, medios, permisos, autorizaciones y seguros necesarios para ejercer legalmente su actividad.",
          "Cada col·laborador desenvolupa la seva activitat per compte propi i és responsable de disposar dels vehicles, mitjans, permisos, autoritzacions i assegurances necessaris per exercir legalment la seva activitat.",
          "Each partner operates on their own account and is responsible for having the vehicles, equipment, permits, authorisations and insurance needed to carry out their activity lawfully."),
        L("La asignación de un colaborador permite ofrecer al cliente una respuesta rápida y una mayor cobertura, especialmente cuando el servicio se encuentra fuera de nuestra zona habitual de actuación.",
          "L'assignació d'un col·laborador permet oferir al client una resposta ràpida i una cobertura més àmplia, especialment quan el servei es troba fora de la nostra zona habitual d'actuació.",
          "Assigning a partner allows us to offer customers a fast response and wider coverage, especially when the service is outside our usual area of operation.")]),
    (L("Condiciones del servicio", "Condicions del servei", "Service conditions"), [
        L("Antes de la realización del servicio, el cliente será informado de las condiciones y del precio correspondiente.",
          "Abans de la realització del servei, el client serà informat de les condicions i del preu corresponent.",
          "Before the service is carried out, the customer will be informed of the conditions and the corresponding price."),
        L("Cuando el servicio sea realizado por un colaborador independiente, el cliente será informado de que la ejecución material del servicio corresponde al profesional o empresa colaboradora asignada.",
          "Quan el servei el faci un col·laborador independent, el client serà informat que l'execució material del servei correspon al professional o a l'empresa col·laboradora assignada.",
          "When the service is carried out by an independent partner, the customer will be informed that the physical performance of the service is the responsibility of the assigned professional or partner company."),
        L("El pago del servicio se realizará directamente al colaborador que haya realizado la asistencia o transporte, quien será responsable de emitir el correspondiente justificante o factura conforme a la normativa aplicable.",
          "El pagament del servei es farà directament al col·laborador que hagi fet l'assistència o el transport, que serà responsable d'emetre el justificant o la factura corresponent d'acord amb la normativa aplicable.",
          "Payment for the service will be made directly to the partner who provided the assistance or transport, who will be responsible for issuing the corresponding receipt or invoice in accordance with applicable regulations."),
        L("Nuestra empresa percibe una comisión del colaborador por las labores de captación, gestión y coordinación del servicio.",
          "La nostra empresa percep una comissió del col·laborador per les tasques de captació, gestió i coordinació del servei.",
          "Our company receives a commission from the partner for finding, managing and coordinating the service.")]),
    (L("Atención de incidencias", "Atenció d'incidències", "Handling issues"), [
        L("En caso de producirse cualquier incidencia relacionada con un servicio realizado por un colaborador, nuestra empresa podrá facilitar la gestión y comunicación entre el cliente y el profesional que haya realizado materialmente el servicio.",
          "En cas que es produeixi qualsevol incidència relacionada amb un servei fet per un col·laborador, la nostra empresa podrà facilitar la gestió i la comunicació entre el client i el professional que hagi fet materialment el servei.",
          "If any issue arises in connection with a service carried out by a partner, our company may help with the handling of and communication between the customer and the professional who physically carried out the service."),
        L("El colaborador será responsable de la correcta ejecución material del servicio dentro del ámbito de sus obligaciones profesionales y legales, así como de disponer de los seguros correspondientes.",
          "El col·laborador serà responsable de la correcta execució material del servei dins de l'àmbit de les seves obligacions professionals i legals, així com de disposar de les assegurances corresponents.",
          "The partner is responsible for the proper physical performance of the service within the scope of their professional and legal obligations, and for holding the relevant insurance."),
        L("Todo ello se entiende sin perjuicio de las responsabilidades que legalmente puedan corresponder a cada una de las partes.",
          "Tot això s'entén sense perjudici de les responsabilitats que legalment puguin correspondre a cadascuna de les parts.",
          "All of the above is without prejudice to any liability that may legally correspond to each of the parties.")]),
]

LEGAL = [("aviso-legal", L("Aviso legal", "Avís legal", "Legal notice")),
         ("politica-privacidad", L("Política de privacidad", "Política de privacitat", "Privacy policy")),
         ("politica-cookies", L("Política de cookies", "Política de cookies", "Cookie policy")),
         ("condiciones-servicio", L("Condiciones de servicio", "Condicions del servei", "Terms of service"))]

# Textos de la interfaz
UI = {
    "skip": L("Saltar al contenido", "Salta al contingut", "Skip to content"),
    "home": L("Inicio", "Inici", "Home"),
    "nav": L("Principal", "Principal", "Main"),
    "slogan": L("SERVICIO 24H", "SERVEI 24H", "24H SERVICE"),
    "m_serv": L("Servicios", "Serveis", "Services"),
    "m_zonas": L("Zonas", "Zones", "Areas"),
    "m_como": L("Cómo funciona", "Com funciona", "How it works"),
    "m_faq": L("Preguntas", "Preguntes", "FAQ"),
    "m_cont": L("Contacto", "Contacte", "Contact"),
    "lang": L("Idioma", "Idioma", "Language"),
    "cta_h": L("¿Necesitas una grúa ahora?", "Necessites una grua ara?", "Need a tow truck now?"),
    "cta_p": L("Respondemos 24 horas, 365 días.", "Responem 24 hores, 365 dies.", "We answer 24 hours a day, 365 days a year."),
    "call_now": L("Llamar ahora", "Truca ara", "Call now"),
    "call": L("Llamar", "Trucar", "Call"),
    "important": L("Importante", "Important", "Important"),
    "f_about": L("Gestión de servicios de grúa y asistencia en carretera 24h en Barcelona y área metropolitana, con una amplia red de profesionales colaboradores.",
                 "Gestió de serveis de grua i assistència en carretera 24h a Barcelona i l'àrea metropolitana, amb una àmplia xarxa de professionals col·laboradors.",
                 "24h towing and roadside assistance management in Barcelona and the metropolitan area, backed by a wide network of partner professionals."),
    "h24": L("24 horas", "24 hores", "24 hours"),
    "d365": L("365 días al año", "365 dies l'any", "365 days a year"),
    "telwa": L("Teléfono y WhatsApp", "Telèfon i WhatsApp", "Phone and WhatsApp"),
    "amb": L("y área metropolitana", "i àrea metropolitana", "and metro area"),
    "legal_nav": L("Información legal", "Informació legal", "Legal information"),
    "made": L("Página web creada por", "Pàgina web creada per", "Website by"),
    "wa_aria": L("Pedir grúa por WhatsApp", "Demanar grua per WhatsApp", "Request a tow truck via WhatsApp"),
    "wa_q": L("¿Necesitas una grúa?", "Necessites una grua?", "Need a tow truck?"),
    "wa_w": L("Escríbenos", "Escriu-nos", "Message us"),
    "faq_h": L("Preguntas frecuentes", "Preguntes freqüents", "Frequently asked questions"),
    "logo_alt": L("Logo de {n}", "Logotip de {n}", "{n} logo"),
    "og_alt": L("Logo de {n}, grúa 24 horas", "Logotip de {n}, grua 24 hores", "{n} logo, 24-hour tow truck"),
    "tow_in": L("Grúa {en}", "Grua {en}", "Tow truck {en}"),
}

# ---------------- PLANTILLAS ----------------
# CSS en línea (menos peticiones = carga más rápida, mejor para Google)
CSS = re.sub(r"\s*\n\s*", "", re.sub(r"/\*.*?\*/", "", (ROOT / "css/styles.css").read_text(encoding="utf-8"), flags=re.S))


def ld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'


def business():
    return {
        "@context": "https://schema.org",
        "@type": ["AutomotiveBusiness", "EmergencyService"],
        "@id": f"{SITE}/#negocio",
        "name": NAME,
        "alternateName": ["PL Grúas Servicio 24H", "Grúa 24 horas Barcelona"],
        "description": t(L(
            "Gestión y coordinación, con una red de profesionales colaboradores, de servicios de grúa y asistencia en carretera 24 horas en Barcelona y área metropolitana: remolque de coches, rescate tras accidente, arranque de batería, pinchazos y traslados.",
            "Gestió i coordinació, amb una xarxa de professionals col·laboradors, de serveis de grua i assistència en carretera 24 hores a Barcelona i l'àrea metropolitana: remolc de cotxes, rescat després d'accident, arrencada de bateria, punxades i trasllats.",
            "Management and coordination, through a network of partner professionals, of 24-hour towing and roadside assistance services in Barcelona and the metropolitan area: car towing, accident recovery, battery jump-starts, flat tyres and vehicle transport.")),
        "url": f"{SITE}{lp('/')}",
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
                         "availableLanguage": ["es", "ca", "en"], "hoursAvailable": "Mo-Su 00:00-23:59"},
        "hasOfferCatalog": {"@type": "OfferCatalog",
                            "name": t(L("Servicios de grúa y asistencia en carretera", "Serveis de grua i assistència en carretera", "Towing and roadside assistance services")),
                            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": t(s[1]), "description": t(s[2])}} for s in SERVICES]},
        "sameAs": [],
    }


def lang_switch(path):
    """Selector de idioma (bandera + código) arriba a la derecha. path=None: todos los idiomas llevan a su portada."""
    items = "".join(
        f'<li><a href="{lp(path or "/", l)}" hreflang="{l}" lang="{l}"{' aria-current="page"' if l == CUR else ""}>'
        f'{FLAG[l]}<span>{m["name"]}</span></a></li>' for l, m in LANGS.items())
    return (f'<details class="lang"><summary aria-label="{t(UI["lang"])}: {LANGS[CUR]["name"]}">{FLAG[CUR]}<span>{CUR.upper()}</span></summary>'
            f'<ul>{items}</ul></details>')


def head(title, desc, path, extra_ld=(), robots="index, follow, max-image-preview:large", preload=False, alternates=True):
    """path: ruta sin prefijo de idioma (p.ej. /grua-badalona/)."""
    url = f"{SITE}{lp(path)}"
    pre = '<link rel="preload" as="image" href="/img/logo-negro.webp" type="image/webp" fetchpriority="high">' if preload else ""
    ga = ""
    if GA4_ID:
        ga = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>'
              f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA4_ID}');</script>")
    gsc = f'<meta name="google-site-verification" content="{GSC_VERIFY}">' if GSC_VERIFY else ""
    hreflang = ""
    if alternates:
        hreflang = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{lp(path, l)}">' for l in LANGS)
        hreflang += f'\n<link rel="alternate" hreflang="x-default" href="{SITE}{path}">'
    og_alt = "\n".join(f'<meta property="og:locale:alternate" content="{m["locale"]}">' for l, m in LANGS.items() if l != CUR)
    lds = "\n".join(ld(x) for x in extra_ld)
    return f"""<!DOCTYPE html>
<html lang="{CUR}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
{hreflang}
<meta name="author" content="{NAME}">
<meta name="theme-color" content="#0f0f10">
<meta name="format-detection" content="telephone=yes">
<meta name="geo.region" content="ES-CT">
<meta name="geo.placename" content="Barcelona">
<meta name="geo.position" content="41.3874;2.1686">
<meta name="ICBM" content="41.3874, 2.1686">
{gsc}
<meta property="og:type" content="website">
<meta property="og:locale" content="{LANGS[CUR]["locale"]}">
{og_alt}
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{t(UI["og_alt"], n=NAME)}">
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
{ld(business())}
{lds}
{ga}
</head>
<body>
<a class="skip" href="#main">{t(UI["skip"])}</a>
<header class="site">
 <div class="wrap nav">
  <a class="brand" href="{lp("/")}" aria-label="{NAME} - {t(UI["home"])}"><img src="/img/icon-192.png" alt="" width="46" height="46">
   <span>PL GRÚAS<small>{t(UI["slogan"])}</small></span></a>
  <nav aria-label="{t(UI["nav"])}"><ul class="menu">
   <li><a href="{lp("/")}#servicios">{t(UI["m_serv"])}</a></li><li><a href="{lp("/")}#zonas">{t(UI["m_zonas"])}</a></li>
   <li><a href="{lp("/")}#como-funciona">{t(UI["m_como"])}</a></li><li><a href="{lp("/")}#preguntas">{t(UI["m_faq"])}</a></li><li><a href="{lp("/")}#contacto">{t(UI["m_cont"])}</a></li>
  </ul></nav>
  <div class="nav-r">
   <a class="btn btn-y" href="tel:{PHONE_INTL}" data-track="click_llamar">{ICON["tel"]}<span>{PHONE_TXT}</span></a>
   {lang_switch(path if alternates else None)}
  </div>
 </div>
</header>
<main id="main">
"""


def short(n):
    return n.replace("de Llobregat", "").replace("del Vallès", "").strip()


def foot(wa_url=None):
    wa_url = wa_url or wa()
    return f"""</main>
<section class="cta-band" id="contacto">
 <div class="wrap">
  <h2>{t(UI["cta_h"])}</h2>
  <p>{t(UI["cta_p"])}</p>
  <a class="phone-big" href="tel:{PHONE_INTL}" data-track="click_llamar">{PHONE_FULL}</a>
  <div class="ctas">
   <a class="btn btn-y" href="tel:{PHONE_INTL}" data-track="click_llamar">{ICON["tel"]} {t(UI["call_now"])}</a>
  </div>
  <p class="nota"><b>{t(UI["important"])}:</b> {t(NOTA_COLABORADORES)}</p>
 </div>
</section>
<footer>
 <div class="road" aria-hidden="true"></div>
 <div class="wrap">
  <div class="fgrid">
   <div class="fbrand">
    <picture><source srcset="/img/logo-oscuro.webp" type="image/webp"><img src="/img/logo-oscuro.png" alt="{NAME}" width="240" height="214" loading="lazy"></picture>
    <p>{t(UI["f_about"])}</p>
   </div>
   <nav aria-label="Servicios"><h3>{t(UI["m_serv"])}</h3><ul>{"".join(f'<li><a href="{lp(f"/{s[3]}/")}">{t(s[1])}</a></li>' for s in SERVICES if s[3])}</ul></nav>
   <nav aria-label="Zonas"><h3>{t(UI["m_zonas"])}</h3><ul class="cols">{"".join(f'<li><a href="{lp(f"/{z['slug']}/")}">{short(z["name"])}</a></li>' for z in ZONES)}</ul></nav>
   <div><h3>{t(UI["m_cont"])}</h3>
    <ul class="fcontact">
     <li>{SICON["reloj"]}<span><b>{t(UI["h24"])}</b>{t(UI["d365"])}</span></li>
     <li>{ICON["tel"]}<span><b><a href="tel:{PHONE_INTL}">{PHONE_FULL}</a></b>{t(UI["telwa"])}</span></li>
     <li>{SICON["pin"]}<span><b>Barcelona</b>{t(UI["amb"])}</span></li>
    </ul>
   </div>
  </div>
  <div class="legal"><span>© <span id="year">{date.today().year}</span> {NAME}</span>
   <nav class="flegal" aria-label="{t(UI["legal_nav"])}">{" | ".join(f'<a href="{lp(f"/{s}/")}">{t(ti)}</a>' for s, ti in LEGAL)}</nav>
   <span>{t(UI["made"])} <a href="https://zetaweb.es/" target="_blank" rel="noopener">ZetaWeb</a></span></div>
 </div>
</footer>
<a class="wa-float" href="{wa_url}" target="_blank" rel="noopener" aria-label="{t(UI["wa_aria"])}" data-track="click_whatsapp"><span class="wa-ic">{ICON["wa"]}</span><span class="wa-txt"><small>{t(UI["wa_q"])}</small>{t(UI["wa_w"])}</span></a>
<script src="/js/main.js" defer></script>
</body>
</html>
"""


def ctas():
    return f"""<div class="ctas">
 <a class="btn btn-y" href="tel:{PHONE_INTL}" data-track="click_llamar">{ICON["tel"]} {t(UI["call"])}: {PHONE_TXT}</a>
</div>"""


def services_html(h="h3", skip=None):
    out = ""
    for i, ti, d, slug in SERVICES:
        if slug and slug == skip:
            continue
        name = f'<a href="{lp(f"/{slug}/")}" class="cardlink">{t(ti)}</a>' if slug else t(ti)
        out += f'<article class="card"><div class="ic">{SICON[i]}</div><{h}>{name}</{h}><p>{t(d)}</p></article>'
    return out


def faq_html(items=FAQ):
    return '<div class="faq">' + "".join(f"<details><summary>{t(q)}</summary><p>{t(a)}</p></details>" for q, a in items) + "</div>"


def faq_ld(items=FAQ):
    return {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": CUR,
            "mainEntity": [{"@type": "Question", "name": t(q), "acceptedAnswer": {"@type": "Answer", "text": t(a)}} for q, a in items]}


def crumbs_ld(name, path):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": t(UI["home"]), "item": f"{SITE}{lp('/')}"},
        {"@type": "ListItem", "position": 2, "name": name, "item": f"{SITE}{lp(path)}"}]}


def steps():
    s = [(ICON["tel"], L("Llama o escribe", "Truca o escriu", "Call or message"), L("A cualquier hora", "A qualsevol hora", "Any time")),
         (SICON["pin"], L("Envía tu ubicación", "Envia la teva ubicació", "Send your location"),
          L("Por WhatsApp, en un toque", "Per WhatsApp, amb un toc", "Via WhatsApp, in one tap")),
         (SICON["euro"], L("Te damos precio", "Et donem preu", "Get a price"), L("Cerrado, antes de salir", "Tancat, abans de sortir", "Fixed, before we set off")),
         (SICON["grua"], L("Llegamos", "Arribem", "We arrive"), L("Y lo solucionamos", "I ho solucionem", "And sort it out"))]
    return '<ol class="steps">\n' + "\n".join(f" <li>{i}<h3>{t(h)}</h3><p>{t(p)}</p></li>" for i, h, p in s) + "\n</ol>"


# ---------------- PÁGINAS ----------------
def index():
    title = f"{NAME} | {t(L('Grúa 24 Horas Barcelona', 'Grua 24 Hores Barcelona', '24 Hour Tow Truck Barcelona'))} ☎ {PHONE_TXT}"
    desc = t(L("Grúa 24h en Barcelona y área metropolitana: remolque de coches y motos, accidentes, batería y pinchazos. Precio al momento. Llama o WhatsApp {p}.",
               "Grua 24h a Barcelona i l'àrea metropolitana: remolc de cotxes i motos, accidents, bateria i punxades. Preu a l'instant. Truca o WhatsApp {p}.",
               "24h tow truck in Barcelona and the metropolitan area: car and motorbike towing, accidents, batteries and flat tyres. Instant quote. Call or WhatsApp {p}."),
             p=PHONE_TXT)
    website = {"@context": "https://schema.org", "@type": "WebSite", "@id": f"{SITE}/#web", "url": f"{SITE}{lp('/')}", "name": NAME,
               "inLanguage": CUR, "publisher": {"@id": f"{SITE}/#negocio"}}
    zones = f'<li><span>{t(L("Barcelona (todos los distritos)", "Barcelona (tots els districtes)", "Barcelona (all districts)"))}</span></li>' + "".join(
        f'<li><a href="{lp(f"/{z['slug']}/")}">{z["name"]}</a></li>' for z in ZONES)
    quick = "".join(
        f'<a class="q" href="{wa(t(m))}" target="_blank" rel="noopener" data-track="click_whatsapp">{SICON[i]}<span>{t(ti)}</span></a>'
        for i, ti, m in [
            ("bat", L("No arranca", "No arrenca", "Won't start"), L("mi coche no arranca", "el meu cotxe no arrenca", "my car won't start")),
            ("acc", L("Accidente", "Accident", "Accident"), L("he tenido un accidente", "he tingut un accident", "I've had an accident")),
            ("rueda", L("Pinchazo", "Punxada", "Flat tyre"), L("he pinchado una rueda", "he punxat una roda", "I have a flat tyre")),
            ("fuel", L("Sin gasolina", "Sense benzina", "Out of fuel"), L("me he quedado sin combustible", "m'he quedat sense combustible", "I've run out of fuel")),
            ("grua", L("Avería", "Avaria", "Breakdown"), L("mi coche está averiado", "el meu cotxe està avariat", "my car has broken down")),
            ("moto", L("Moto", "Moto", "Motorbike"), L("es para una moto", "és per a una moto", "it's for a motorbike")),
            ("km", L("Traslado", "Trasllat", "Transport"), L("quiero presupuesto para un traslado", "vull pressupost per a un trasllat", "I'd like a quote for a transfer")),
            ("baja", L("Desguace", "Desballestament", "Scrapping"), L("quiero llevar un coche al desguace", "vull portar un cotxe al desballestament", "I want to scrap a car"))])
    body = f"""
<section class="hero">
 <div class="wrap grid">
  <div>
   <span class="badge"><span class="dot"></span> {t(L("Disponibles ahora · 24h", "Disponibles ara · 24h", "Available now · 24h"))}</span>
   <h1>{t(L('Grúa 24 horas en <span class="hl">Barcelona</span>', 'Grua 24 hores a <span class="hl">Barcelona</span>', '24-hour tow truck in <span class="hl">Barcelona</span>'))}</h1>
   <p class="lead">{t(L("Avería, accidente, batería o pinchazo. Salimos al momento, de día y de noche.",
                        "Avaria, accident, bateria o punxada. Sortim a l'instant, de dia i de nit.",
                        "Breakdown, accident, flat battery or flat tyre. We set off right away, day or night."))}</p>
   {ctas()}
  </div>
  <div class="hero-logo">
   <picture><source srcset="/img/logo-negro.webp" type="image/webp"><img src="/img/logo-negro.png" alt="{t(L("PL Grúas - servicio de grúa 24H", "PL Grúas - servei de grua 24H", "PL Grúas - 24H tow truck service"))}" width="520" height="468" fetchpriority="high"></picture>
  </div>
 </div>
</section>

<section class="feats" aria-label="{t(L("Por qué elegirnos", "Per què triar-nos", "Why choose us"))}">
 <div class="wrap fgrid4">
  <div class="feat">{SICON["reloj"]}<b>{t(L("24h / 365 días", "24h / 365 dies", "24h / 365 days"))}</b><span>{t(L("Noches y festivos", "Nits i festius", "Nights and holidays"))}</span></div>
  <div class="feat">{SICON["pin"]}<b>{t(L("Llegada rápida", "Arribada ràpida", "Fast arrival"))}</b><span>{t(L("Barcelona y AMB", "Barcelona i AMB", "Barcelona & metro area"))}</span></div>
  <div class="feat">{SICON["euro"]}<b>{t(L("Precio cerrado", "Preu tancat", "Fixed price"))}</b><span>{t(L("Antes de salir", "Abans de sortir", "Before we set off"))}</span></div>
  <div class="feat">{SICON["escudo"]}<b>{t(L("Grúa de plataforma", "Grua de plataforma", "Flatbed tow truck"))}</b><span>{t(L("Sin dañar tu coche", "Sense danyar el cotxe", "No damage to your car"))}</span></div>
 </div>
</section>

<section class="quick">
 <div class="wrap center">
  <h2>{t(L("¿Qué le pasa a tu coche?", "Què li passa al teu cotxe?", "What's wrong with your car?"))}</h2>
  <p class="muted">{t(L("Pulsa y te respondemos por WhatsApp al momento.", "Prem i et responem per WhatsApp a l'instant.", "Tap and we'll reply on WhatsApp right away."))}</p>
  <div class="qgrid">{quick}</div>
 </div>
</section>

<section id="servicios">
 <div class="wrap">
  <h2>{t(L("Servicios de grúa en Barcelona", "Serveis de grua a Barcelona", "Towing services in Barcelona"))}</h2>
  <div class="cards">{services_html()}</div>
 </div>
</section>

<section id="pasos" class="alt">
 <div class="wrap">
  <h2>{t(L("Así de fácil", "Així de fàcil", "It's that easy"))}</h2>
  {steps()}
 </div>
</section>

<section class="truck light" id="colaboradores">
 <div class="wrap split">
  <picture><source srcset="/img/logo-claro.webp" type="image/webp"><img src="/img/logo-claro.png" alt="{t(UI["logo_alt"], n=NAME)}" width="600" height="535" loading="lazy"></picture>
  <div>
   <h2>{t(RED[0])}</h2>
   {"".join(f'<p class="muted">{t(x)}</p>' for x in RED[1])}
  </div>
 </div>
</section>

<section id="como-funciona">
 <div class="wrap">
  <h2>{t(L("Cómo funciona nuestro servicio", "Com funciona el nostre servei", "How our service works"))}</h2>
  <div class="incs two">{"".join(f'<article class="inc"><span class="tick">✓</span><div><h3>{t(h)}</h3>{"".join(f"<p>{t(x)}</p>" for x in ps)}</div></article>' for h, ps in FUNCIONAMIENTO)}</div>
  <p class="muted">{t(L('Más información en nuestras <a href="{u}">condiciones de servicio</a>.',
                        'Més informació a les nostres <a href="{u}">condicions del servei</a>.',
                        'More information in our <a href="{u}">terms of service</a>.'), u=lp("/condiciones-servicio/"))}</p>
 </div>
</section>

<section id="zonas">
 <div class="wrap split zsplit">
  <div>
   <h2>{t(L("Grúa en Barcelona y alrededores", "Grua a Barcelona i rodalies", "Tow trucks in Barcelona and surroundings"))}</h2>
   <ul class="zones">{zones}</ul>
  </div>
  <div class="map"><iframe title="{t(L("Zona de servicio: Barcelona y área metropolitana", "Zona de servei: Barcelona i àrea metropolitana", "Service area: Barcelona and metropolitan area"))}" src="https://www.openstreetmap.org/export/embed.html?bbox=1.76%2C41.20%2C2.35%2C41.55&amp;layer=mapnik&amp;marker=41.3874%2C2.1686" loading="lazy"></iframe></div>
 </div>
</section>

<section id="preguntas" class="alt">
 <div class="wrap">
  <h2>{t(UI["faq_h"])}</h2>
  {faq_html()}
 </div>
</section>
"""
    return head(title, desc, "/", [website, faq_ld()], preload=True) + body + foot()


def zone_faq(z):
    n = z["name"]
    return [
        (L(f"¿Cuánto tarda la grúa en llegar a {n}?", f"Quant triga la grua a arribar {en_(n)}?", f"How long does the tow truck take to reach {n}?"),
         L(f"{n} está {z['near']['es']}. Salimos al momento y te damos la hora estimada al llamar.",
           f"{n} és {z['near']['ca']}. Sortim a l'instant i et donem l'hora estimada quan truquis.",
           f"{n} is {z['near']['en']}. We set off right away and give you an estimated arrival time when you call.")),
        (L(f"¿Dónde dais servicio en {n}?", f"On doneu servei {en_(n)}?", f"Where do you operate in {n}?"),
         L(f"En todo el municipio: {z['places']['es']}, y en {z['roads']['es']}.",
           f"A tot el municipi: {z['places']['ca']}, i a {z['roads']['ca']}.",
           f"Across the whole municipality: {z['places']['en']}, as well as on {z['roads']['en']}.")),
        (L(f"¿Cuánto cuesta la grúa en {n}?", f"Quant costa la grua {en_(n)}?", f"How much does a tow truck cost in {n}?"),
         L("Depende de la distancia y el vehículo. Te damos precio cerrado por WhatsApp antes de salir.",
           "Depèn de la distància i del vehicle. Et donem preu tancat per WhatsApp abans de sortir.",
           "It depends on the distance and the vehicle. We'll give you a fixed price via WhatsApp before setting off.")),
    ]


def zone(z):
    n = z["name"]
    path = f"/{z['slug']}/"
    title = f"{NAME} | {t(L('Grúa 24h {n}', 'Grua 24h {n}', '24h Tow Truck {n}'), n=n)} ☎ {PHONE_TXT}"
    desc = t(L("Grúa 24h {en}: remolque de coches y motos, accidentes, batería y pinchazos. Precio al momento. Llama o WhatsApp {p}.",
               "Grua 24h {en}: remolc de cotxes i motos, accidents, bateria i punxades. Preu a l'instant. Truca o WhatsApp {p}.",
               "24h tow truck {en}: car and motorbike towing, accidents, batteries and flat tyres. Instant quote. Call or WhatsApp {p}."),
             en=en_(n), p=PHONE_TXT)
    faq = zone_faq(z)
    crumb = t(UI["tow_in"], en=en_(n))
    svc = {"@context": "https://schema.org", "@type": "Service",
           "serviceType": t(L("Servicio de grúa y asistencia en carretera", "Servei de grua i assistència en carretera", "Towing and roadside assistance service")),
           "name": t(L("Grúa 24 horas {en}", "Grua 24 hores {en}", "24-hour tow truck {en}"), en=en_(n)), "provider": {"@id": f"{SITE}/#negocio"},
           "areaServed": {"@type": "City", "name": n}, "availableChannel": {"@type": "ServiceChannel", "servicePhone": {"@type": "ContactPoint", "telephone": PHONE_FULL}}}
    others = "".join(f'<li><a href="{lp(f"/{o['slug']}/")}">{t(UI["tow_in"], en=en_(o["name"]))}</a></li>' for o in ZONES if o is not z)
    body = f"""
<section class="hero">
 <div class="wrap">
  <nav class="breadcrumb" aria-label="Migas de pan"><a href="{lp("/")}">{t(UI["home"])}</a> › {crumb}</nav>
  <span class="badge"><span class="dot"></span> {t(L("Disponibles ahora {en}", "Disponibles ara {en}", "Available now {en}"), en=en_(n))}</span>
  <h1>{t(L("Grúa 24 horas {en}", "Grua 24 hores {en}", "24-hour tow truck {en}"), en=en_(n, hl=True))}</h1>
  <p class="lead">{t(z["intro"])}</p>
  {ctas()}
  <ul class="ticks"><li>{t(L("24h / 365 días", "24h / 365 dies", "24h / 365 days"))}</li></ul>
 </div>
</section>

<section>
 <div class="wrap">
  <h2>{t(L("Servicios de grúa {en}", "Serveis de grua {en}", "Towing services {en}"), en=en_(n))}</h2>
  <div class="cards">{services_html()}</div>
 </div>
</section>

<section>
 <div class="wrap">
  <h2>{t(UI["faq_h"])}</h2>
  {faq_html(faq)}
 </div>
</section>

<section class="alt">
 <div class="wrap">
  <h2>{t(L("Otras zonas", "Altres zones", "Other areas"))}</h2>
  <ul class="zones"><li><a href="{lp("/")}">{t(UI["tow_in"], en=en_("Barcelona"))}</a></li>{others}</ul>
 </div>
</section>
"""
    return head(title, desc, path, [crumbs_ld(crumb, path), svc, faq_ld(faq)]) + body + foot(wa(lugar=n))


def service_page(slug):
    sp = SERVICE_PAGES[slug]
    icon, name, short_desc, _ = next(s for s in SERVICES if s[3] == slug)
    name = t(name)
    path = f"/{slug}/"
    svc = {"@context": "https://schema.org", "@type": "Service", "serviceType": name, "name": t(sp["h1"]),
           "description": t(sp["desc"]), "provider": {"@id": f"{SITE}/#negocio"},
           "areaServed": [{"@type": "City", "name": "Barcelona"}] + [{"@type": "City", "name": z["name"]} for z in ZONES],
           "hoursAvailable": "Mo-Su 00:00-23:59"}
    sections = "".join(f'<article class="inc"><span class="tick">✓</span><div><h3>{t(h)}</h3><p>{t(x)}</p></div></article>' for h, x in sp["sections"])
    body = f"""
<section class="hero">
 <div class="wrap shero">
  <div>
   <nav class="breadcrumb" aria-label="Migas de pan"><a href="{lp("/")}">{t(UI["home"])}</a> › {name}</nav>
   <span class="badge"><span class="dot"></span> {t(L("Servicio 24h / 365 días", "Servei 24h / 365 dies", "24h service / 365 days"))}</span>
   <h1>{t(sp["h1"])}</h1>
   <p class="lead">{t(sp["intro"])}</p>
   {ctas()}
  </div>
  <div class="sicon" aria-hidden="true">{SICON[icon]}</div>
 </div>
</section>

<section>
 <div class="wrap">
  <h2>{t(L("Qué incluye", "Què inclou", "What's included"))}</h2>
  <div class="incs">{sections}</div>
 </div>
</section>

<section class="alt">
 <div class="wrap">
  <h2>{t(UI["faq_h"])}</h2>
  {faq_html(sp["faq"])}
 </div>
</section>

<section>
 <div class="wrap">
  <h2>{t(L("Otros servicios", "Altres serveis", "Other services"))}</h2>
  <div class="cards">{services_html(skip=slug)}</div>
 </div>
</section>
"""
    return head(f"{NAME} | {t(sp['title'])} ☎ {PHONE_TXT}", t(sp["desc"]), path, [crumbs_ld(name, path), svc, faq_ld(sp["faq"])]) + body + foot(wa(motivo=name.lower()))


def page_404():
    body = f"""<section class="hero"><div class="wrap center"><h1>Página no encontrada</h1>
<p class="lead" style="margin-inline:auto">La página que buscas no existe, pero si necesitas una grúa estamos disponibles 24 horas.</p>
<div class="ctas" style="justify-content:center"><a class="btn btn-o" href="/">Volver al inicio</a>
<a class="btn btn-y" href="tel:{PHONE_INTL}">{ICON["tel"]} {PHONE_TXT}</a></div></div></section>"""
    return head(f"Página no encontrada | {NAME}", "Página no encontrada.", "/404.html", robots="noindex, follow", alternates=False) + body + foot()


def dato(v, etiqueta):
    return v or f"<mark>[{etiqueta}]</mark>"


def legal_pages():
    tit, nif, dom, mail = dato(TITULAR, "Titular"), dato(NIF, "NIF"), dato(DOMICILIO, "Domicilio"), dato(EMAIL, "Email")
    ps = lambda lst: "".join(f"<p>{t(x)}</p>" for x in lst)
    cond = lp("/condiciones-servicio/")
    aviso = lp("/aviso-legal/")
    analytics = t(L(" Además, utilizamos Google Analytics para obtener estadísticas anónimas de visitas; estas cookies solo se instalan si las aceptas.",
                    " A més, utilitzem Google Analytics per obtenir estadístiques anònimes de visites; aquestes cookies només s'instal·len si les acceptes.",
                    " We also use Google Analytics to obtain anonymous visitor statistics; these cookies are only set if you accept them.")
                  if GA4_ID else L(" No utilizamos cookies analíticas ni publicitarias.", " No utilitzem cookies analítiques ni publicitàries.",
                                   " We do not use analytics or advertising cookies."))
    pages = {
        "aviso-legal": L(f"""
<h2>Datos identificativos</h2>
<p>En cumplimiento del artículo 10 de la Ley 34/2002, de Servicios de la Sociedad de la Información y de Comercio Electrónico (LSSI-CE), se informa de los datos del titular de este sitio web:</p>
<ul><li>Titular: {tit}</li><li>NIF: {nif}</li><li>Domicilio: {dom}</li><li>Teléfono: {PHONE_FULL}</li><li>Email: {mail}</li><li>Web: {SITE}</li></ul>
<h2>Objeto</h2>
<p>Este sitio web informa sobre el servicio de recepción, gestión y coordinación de solicitudes de grúa, asistencia en carretera y transporte de vehículos que presta {NAME}. Los servicios pueden ser realizados materialmente por profesionales autónomos o empresas colaboradoras independientes, tal y como se detalla en las <a href="{cond}">condiciones de servicio</a>.</p>
<h2>Propiedad intelectual</h2>
<p>Los textos, imágenes, logotipos y diseño de esta web son propiedad del titular o se usan con autorización. No se permite su reproducción sin consentimiento previo.</p>
<h2>Responsabilidad</h2>
<p>El titular no se hace responsable del mal uso que se haga de los contenidos de la web ni de los contenidos de sitios de terceros enlazados desde ella.</p>
<h2>Legislación aplicable</h2>
<p>Este aviso legal se rige por la legislación española.</p>""", f"""
<h2>Dades identificatives</h2>
<p>En compliment de l'article 10 de la Llei 34/2002, de serveis de la societat de la informació i de comerç electrònic (LSSI-CE), s'informa de les dades del titular d'aquest lloc web:</p>
<ul><li>Titular: {tit}</li><li>NIF: {nif}</li><li>Domicili: {dom}</li><li>Telèfon: {PHONE_FULL}</li><li>Correu electrònic: {mail}</li><li>Web: {SITE}</li></ul>
<h2>Objecte</h2>
<p>Aquest lloc web informa sobre el servei de recepció, gestió i coordinació de sol·licituds de grua, assistència en carretera i transport de vehicles que presta {NAME}. Els serveis poden ser realitzats materialment per professionals autònoms o empreses col·laboradores independents, tal com es detalla a les <a href="{cond}">condicions del servei</a>.</p>
<h2>Propietat intel·lectual</h2>
<p>Els textos, imatges, logotips i disseny d'aquest web són propietat del titular o s'utilitzen amb autorització. No se'n permet la reproducció sense consentiment previ.</p>
<h2>Responsabilitat</h2>
<p>El titular no es fa responsable del mal ús que es faci dels continguts del web ni dels continguts de llocs de tercers enllaçats des d'aquest.</p>
<h2>Legislació aplicable</h2>
<p>Aquest avís legal es regeix per la legislació espanyola. En cas de discrepància entre versions lingüístiques, prevaldrà la versió en castellà.</p>""", f"""
<h2>Identification details</h2>
<p>In compliance with Article 10 of Spanish Law 34/2002 on Information Society Services and Electronic Commerce (LSSI-CE), the details of the owner of this website are as follows:</p>
<ul><li>Owner: {tit}</li><li>Tax ID (NIF): {nif}</li><li>Address: {dom}</li><li>Phone: {PHONE_FULL}</li><li>Email: {mail}</li><li>Website: {SITE}</li></ul>
<h2>Purpose</h2>
<p>This website provides information about the service of receiving, managing and coordinating requests for towing, roadside assistance and vehicle transport offered by {NAME}. Services may be physically carried out by self-employed professionals or independent partner companies, as detailed in the <a href="{cond}">terms of service</a>.</p>
<h2>Intellectual property</h2>
<p>The texts, images, logos and design of this website are owned by the owner or used with permission. They may not be reproduced without prior consent.</p>
<h2>Liability</h2>
<p>The owner is not responsible for any misuse of the website's content or for the content of third-party sites linked from it.</p>
<h2>Applicable law</h2>
<p>This legal notice is governed by Spanish law. In the event of any discrepancy between language versions, the Spanish version shall prevail.</p>"""),
        "politica-privacidad": L(f"""
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
<p>Puedes ejercer tus derechos de acceso, rectificación, supresión, oposición, limitación y portabilidad escribiendo a {mail}. También puedes presentar una reclamación ante la Agencia Española de Protección de Datos (www.aepd.es).</p>""", f"""
<h2>Responsable del tractament</h2>
<p>{tit} · NIF {nif} · {dom} · {mail} · {PHONE_FULL}</p>
<h2>Quines dades tractem i per a què</h2>
<p>Quan ens truques o ens escrius per WhatsApp tractem les dades que ens facilites (nom, telèfon, ubicació, dades del vehicle i del servei sol·licitat) per gestionar la teva sol·licitud, informar-te del preu i coordinar l'assistència.</p>
<h2>Legitimació</h2>
<p>La base legal és l'aplicació de mesures precontractuals i l'execució del servei que sol·licites.</p>
<h2>Destinataris</h2>
<p>Per poder prestar el servei, les teves dades es comunicaran al professional autònom o a l'empresa col·laboradora independent que el faci. Les converses per WhatsApp es regeixen, a més, per la política de privacitat de WhatsApp. No se cedeixen dades a altres tercers excepte per obligació legal.</p>
<h2>Conservació</h2>
<p>Conservem les dades el temps necessari per gestionar el servei i atendre possibles incidències, i després durant els terminis legalment exigits.</p>
<h2>Els teus drets</h2>
<p>Pots exercir els drets d'accés, rectificació, supressió, oposició, limitació i portabilitat escrivint a {mail}. També pots presentar una reclamació davant l'Agència Espanyola de Protecció de Dades (www.aepd.es).</p>""", f"""
<h2>Data controller</h2>
<p>{tit} · NIF {nif} · {dom} · {mail} · {PHONE_FULL}</p>
<h2>What data we process and why</h2>
<p>When you call us or message us on WhatsApp, we process the data you provide (name, phone number, location, vehicle details and the service requested) in order to handle your request, tell you the price and coordinate the assistance.</p>
<h2>Legal basis</h2>
<p>The legal basis is the taking of pre-contractual steps and the performance of the service you request.</p>
<h2>Recipients</h2>
<p>In order to provide the service, your data will be shared with the self-employed professional or independent partner company that carries it out. WhatsApp conversations are also subject to WhatsApp's privacy policy. No data is disclosed to other third parties unless required by law.</p>
<h2>Retention</h2>
<p>We keep the data for as long as needed to manage the service and deal with any issues, and thereafter for the periods required by law.</p>
<h2>Your rights</h2>
<p>You can exercise your rights of access, rectification, erasure, objection, restriction and portability by writing to {mail}. You can also lodge a complaint with the Spanish Data Protection Agency (www.aepd.es).</p>"""),
        "politica-cookies": L(f"""
<h2>Qué son las cookies</h2>
<p>Las cookies son pequeños archivos que las webs guardan en tu navegador para funcionar o recordar información sobre tu visita.</p>
<h2>Cookies que utiliza esta web</h2>
<p>Esta web no utiliza cookies propias que requieran tu consentimiento.{analytics}</p>
<p>El mapa de la zona de servicio se muestra desde OpenStreetMap, que puede tratar datos técnicos de la conexión según su propia política de privacidad.</p>
<h2>Cómo desactivarlas</h2>
<p>Puedes bloquear o eliminar las cookies desde la configuración de tu navegador.</p>""", f"""
<h2>Què són les cookies</h2>
<p>Les cookies són petits arxius que els webs desen al teu navegador per funcionar o recordar informació sobre la teva visita.</p>
<h2>Cookies que utilitza aquest web</h2>
<p>Aquest web no utilitza cookies pròpies que requereixin el teu consentiment.{analytics}</p>
<p>El mapa de la zona de servei es mostra des d'OpenStreetMap, que pot tractar dades tècniques de la connexió segons la seva pròpia política de privacitat.</p>
<h2>Com desactivar-les</h2>
<p>Pots bloquejar o eliminar les cookies des de la configuració del teu navegador.</p>""", f"""
<h2>What are cookies</h2>
<p>Cookies are small files that websites store in your browser in order to work or remember information about your visit.</p>
<h2>Cookies used on this website</h2>
<p>This website does not use its own cookies that require your consent.{analytics}</p>
<p>The service area map is displayed from OpenStreetMap, which may process technical connection data in accordance with its own privacy policy.</p>
<h2>How to disable them</h2>
<p>You can block or delete cookies in your browser settings.</p>"""),
    }
    h = [L("1. Objeto: gestión e intermediación", "1. Objecte: gestió i intermediació", "1. Purpose: management and intermediation"),
         L("2. Red de profesionales colaboradores", "2. Xarxa de professionals col·laboradors", "2. Partner professional network"),
         L("3. Profesionales independientes", "3. Professionals independents", "3. Independent professionals"),
         L("4. Contratación, precio y pago", "4. Contractació, preu i pagament", "4. Booking, price and payment"),
         L("5. Incidencias y reclamaciones", "5. Incidències i reclamacions", "5. Issues and complaints"),
         L("6. Aceptación", "6. Acceptació", "6. Acceptance")]
    out = {k: t(v) for k, v in pages.items()}
    out["condiciones-servicio"] = f"""
<h2>{t(h[0])}</h2>
{ps(FUNCIONAMIENTO[0][1])}
<h2>{t(h[1])}</h2>
{ps(RED[1])}
<h2>{t(h[2])}</h2>
{ps(FUNCIONAMIENTO[1][1])}
<h2>{t(h[3])}</h2>
{ps(FUNCIONAMIENTO[2][1])}
<h2>{t(h[4])}</h2>
{ps(FUNCIONAMIENTO[3][1])}
<h2>{t(h[5])}</h2>
<p>{t(NOTA_COLABORADORES)}</p>
<p>{t(L('Los datos del titular figuran en el <a href="{u}">aviso legal</a>.', "Les dades del titular figuren a l'<a href=\"{u}\">avís legal</a>.",
          'The owner\'s details are set out in the <a href="{u}">legal notice</a>.'), u=aviso)}</p>"""
    return out


def legal_page(slug, title, content):
    body = f"""
<section class="hero">
 <div class="wrap">
  <nav class="breadcrumb" aria-label="Migas de pan"><a href="{lp("/")}">{t(UI["home"])}</a> › {title}</nav>
  <h1>{title}</h1>
 </div>
</section>
<section>
 <div class="wrap prose">{content}</div>
</section>
"""
    return head(f"{title} | {NAME}", f"{title} - {NAME}.", f"/{slug}/", robots="noindex, follow") + body + foot()


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
    global CUR
    for CUR in LANGS:
        pre = lp("/")[1:]  # "" en español, "ca/" o "en/" en los demás
        write(f"{pre}index.html", index())
        for z in ZONES:
            write(f"{pre}{z['slug']}/index.html", zone(z))
        for slug in SERVICE_PAGES:
            write(f"{pre}{slug}/index.html", service_page(slug))
        pages = legal_pages()
        for slug, title in LEGAL:
            write(f"{pre}{slug}/index.html", legal_page(slug, t(title), pages[slug]))
    CUR = DEFAULT
    write("404.html", page_404())

    urls = [("/", "1.0", "weekly")] + [(f"/{s}/", "0.9", "monthly") for s in SERVICE_PAGES] + [(f"/{z['slug']}/", "0.8", "monthly") for z in ZONES]
    alts = lambda u: "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{SITE}{lp(u, l)}"/>' for l in LANGS) + \
        f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{u}"/>'
    sm = "".join(f"<url><loc>{SITE}{lp(u, l)}</loc><lastmod>{TODAY}</lastmod><changefreq>{c}</changefreq><priority>{p}</priority>{alts(u)}"
                 + (f"<image:image><image:loc>{SITE}/img/logo-claro.png</image:loc></image:image>" if u == "/" else "") + "</url>\n"
                 for u, p, c in urls for l in LANGS)
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
          'xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + sm + "</urlset>\n")
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
          "\n- Servicios: " + ", ".join(s[1]["es"] for s in SERVICES) +
          f"\n- Idiomas: español ({SITE}/), catalán ({SITE}/ca/) e inglés ({SITE}/en/)\n- Web: {SITE}/\n")


if __name__ == "__main__":
    main()
