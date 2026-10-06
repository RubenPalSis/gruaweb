#!/usr/bin/env python3
"""Genera la web estática de Asistencia 24H Barcelona.

Edita la CONFIGURACIÓN y ejecuta:  python3 build.py
Crea index.html, páginas de zona, páginas legales, 404, sitemap.xml, robots.txt y manifest.
"""
import json
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

SERVICES = [
    ("grua", "Remolque de coches averiados", "Llevamos tu vehículo al taller, concesionario o domicilio que elijas, con grúa de plataforma y sin dañar el coche."),
    ("acc", "Rescate tras accidente", "Retirada rápida de vehículos siniestrados en calles, rondas y autopistas. Te ayudamos a despejar la vía con seguridad."),
    ("bat", "Arranque de batería", "¿El coche no arranca? Arrancamos tu batería en el sitio o la sustituimos para que sigas tu camino."),
    ("rueda", "Pinchazo y cambio de rueda", "Cambiamos la rueda pinchada en el momento. Si no tienes repuesto, trasladamos el vehículo al taller más cercano."),
    ("fuel", "Falta de combustible", "Te quedaste sin gasolina o diésel: te llevamos combustible o el coche hasta la gasolinera."),
    ("moto", "Traslado de motos", "Transporte de motos y scooters con anclajes específicos, también por avería o accidente."),
    ("km", "Traslados de larga distancia", "Transporte de vehículos dentro de Cataluña y a cualquier punto de España. Presupuesto cerrado."),
    ("llave", "Traslados a ITV y taller", "Movemos coches sin ITV, sin batería o que no pueden circular, con total seguridad y legalidad."),
    ("baja", "Retirada para desguace", "Recogemos tu coche viejo o siniestrado y lo llevamos a un centro autorizado para darlo de baja."),
]

BCN_DISTRICTS = ["Ciutat Vella", "Eixample", "Sants-Montjuïc", "Les Corts", "Sarrià-Sant Gervasi", "Gràcia",
                 "Horta-Guinardó", "Nou Barris", "Sant Andreu", "Sant Martí", "Poblenou", "Zona Franca"]

ZONES = [
    dict(slug="grua-hospitalet-de-llobregat", name="L'Hospitalet de Llobregat",
         roads="la Gran Via, la Ronda Litoral, la B-10 y la C-31",
         places="Bellvitge, Collblanc, La Torrassa, Santa Eulàlia, Can Serra y la Fira Gran Via",
         intro="L'Hospitalet está pegada a Barcelona y una de las zonas con más tráfico del área metropolitana. Por eso tenemos grúa disponible para llegar en muy poco tiempo a cualquier barrio."),
    dict(slug="grua-badalona", name="Badalona",
         roads="la C-31, la B-20 (Ronda de Dalt), la Ronda Litoral y la autopista C-32",
         places="el Centre, Llefià, Sant Roc, Montigalà, Pomar, Bufalà y el Port de Badalona",
         intro="Damos servicio de grúa y asistencia en carretera en todo Badalona, desde el puerto hasta los barrios altos, de día y de noche."),
    dict(slug="grua-cornella-de-llobregat", name="Cornellà de Llobregat",
         roads="la B-23, la A-2, la Ronda de Dalt y la C-245",
         places="Almeda, Sant Ildefons, Fontsanta, Gavarra y la zona del RCDE Stadium",
         intro="En Cornellà atendemos averías y accidentes tanto en el casco urbano como en los accesos a la A-2 y la B-23."),
    dict(slug="grua-el-prat-de-llobregat", name="El Prat de Llobregat",
         roads="la C-31, la autovía de Castelldefels, la B-22 y los accesos al Aeropuerto",
         places="el centro del Prat, Sant Cosme, el polígono Mas Blau y el Aeropuerto Josep Tarradellas Barcelona-El Prat (T1 y T2)",
         intro="¿Tu coche te ha dejado tirado de camino al aeropuerto o en los polígonos del Prat? Llámanos y vamos a por ti."),
    dict(slug="grua-santa-coloma-de-gramenet", name="Santa Coloma de Gramenet",
         roads="la B-20, la C-31 y la C-58",
         places="Singuerlín, Fondo, Can Mariner, Santa Rosa, Riu Nord y Riu Sud",
         intro="Ofrecemos grúa 24 horas en Santa Coloma de Gramenet con salida inmediata hacia cualquier barrio de la ciudad."),
    dict(slug="grua-sant-adria-de-besos", name="Sant Adrià de Besòs",
         roads="la Ronda Litoral, la C-31 y la B-10",
         places="La Mina, Sant Joan Baptista, Besòs y el Port Fòrum",
         intro="Desde el Fòrum hasta La Mina, recogemos tu vehículo averiado o accidentado en Sant Adrià de Besòs a cualquier hora."),
    dict(slug="grua-esplugues-de-llobregat", name="Esplugues de Llobregat",
         roads="la B-23, la Ronda de Dalt y la N-340",
         places="Can Vidalet, La Plana, Ciutat Diagonal y El Gall",
         intro="En Esplugues y Ciutat Diagonal te ofrecemos asistencia en carretera rápida, también en los accesos a la Diagonal y la B-23."),
    dict(slug="grua-sant-cugat-del-valles", name="Sant Cugat del Vallès",
         roads="la AP-7, la C-16 (túneles de Vallvidrera) y la B-30",
         places="el centro, Valldoreix, Mira-sol, Les Planes, La Floresta y el Parc Tecnològic del Vallès",
         intro="Cubrimos Sant Cugat y su entorno, incluidos los túneles de Vallvidrera, la AP-7 y las urbanizaciones de la zona."),
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


# ---------------- PLANTILLAS ----------------
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


def head(title, desc, path, extra_ld=(), robots="index, follow, max-image-preview:large"):
    url = f"{SITE}{path}"
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
<link rel="preload" as="image" href="/img/logo-oscuro.webp" type="image/webp">
<link rel="stylesheet" href="/css/styles.css">
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
   <div><h3>Servicios</h3><ul>{"".join(f'<li><a href="/#servicios">{s[1]}</a></li>' for s in SERVICES[:6])}</ul></div>
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


def services_html(h="h3"):
    return "".join(f'<article class="card"><div class="ic">{SICON[i]}</div><{h}>{t}</{h}><p>{d}</p></article>' for i, t, d in SERVICES)


def faq_html():
    return "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)


FAQ_LD = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}

STEPS = f"""<ol class="steps">
 <li><h3>Llama o escribe</h3><p class="muted">Contacta al {PHONE_TXT} por teléfono o WhatsApp a cualquier hora.</p></li>
 <li><h3>Envía tu ubicación</h3><p class="muted">Compártela por WhatsApp y dinos qué le pasa al vehículo y a dónde va.</p></li>
 <li><h3>Presupuesto al momento</h3><p class="muted">Te damos precio y hora estimada de llegada antes de salir. Sin sorpresas.</p></li>
 <li><h3>Llegamos y lo resolvemos</h3><p class="muted">Reparamos en el sitio si es posible o llevamos tu coche donde necesites.</p></li>
</ol>"""


# ---------------- PÁGINAS ----------------
def index():
    title = "Grúa 24 Horas Barcelona | Asistencia en Carretera ☎ 671 44 86 39"
    desc = ("Grúa 24h en Barcelona y área metropolitana. Remolque de coches y motos, rescate tras accidente, batería y pinchazos. "
            "Llegada rápida y presupuesto al momento. Llama o WhatsApp: 671 44 86 39.")
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

<section id="preguntas" class="alt">
 <div class="wrap prose">
  <span class="kicker">Preguntas frecuentes</span>
  <h2>Dudas sobre nuestro servicio de grúa</h2>
  {faq_html()}
 </div>
</section>
"""
    return head(title, desc, "/", [website, FAQ_LD]) + body + foot()


def zone(z):
    n = z["name"]
    path = f"/{z['slug']}/"
    title = f"Grúa en {n} 24 Horas | Asistencia en Carretera ☎ {PHONE_TXT}"
    desc = f"Grúa 24h en {n}: remolque de coches y motos, accidentes, batería y pinchazos. Salida inmediata y presupuesto al momento. Llama o WhatsApp {PHONE_TXT}."
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": f"Grúa en {n}", "item": f"{SITE}{path}"}]}
    svc = {"@context": "https://schema.org", "@type": "Service", "serviceType": "Servicio de grúa y asistencia en carretera",
           "name": f"Grúa 24 horas en {n}", "provider": {"@id": f"{SITE}/#negocio"},
           "areaServed": {"@type": "City", "name": n}, "availableChannel": {"@type": "ServiceChannel", "servicePhone": {"@type": "ContactPoint", "telephone": PHONE_FULL}}}
    others = "".join(f'<li><a href="/{o["slug"]}/">{o["name"]}</a></li>' for o in ZONES if o is not z)
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
  <p class="muted">Atendemos averías y accidentes en todo {n}: {z["places"]}. También en vías como {z["roads"]}.</p>
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
 <div class="wrap">
  <h2>Otras zonas donde trabajamos</h2>
  <ul class="zones"><li><a href="/">Barcelona</a></li>{others}</ul>
 </div>
</section>
"""
    return head(title, desc, path, [crumbs, svc]) + body + foot()


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


def write(rel, txt):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(txt, encoding="utf-8")
    print("✓", rel)


def main():
    write("index.html", index())
    for z in ZONES:
        write(f"{z['slug']}/index.html", zone(z))
    for slug, (t, h) in LEGAL.items():
        write(f"{slug}/index.html", legal_page(slug, t, h))
    write("404.html", page_404())

    urls = [("/", "1.0", "weekly")] + [(f"/{z['slug']}/", "0.8", "monthly") for z in ZONES]
    sm = "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{c}</changefreq><priority>{p}</priority>"
                 + (f"<image:image><image:loc>{SITE}/img/logo-claro.png</image:loc></image:image>" if u == "/" else "") + "</url>\n"
                 for u, p, c in urls)
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
          'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + sm + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /404.html\n\nSitemap: {SITE}/sitemap.xml\n")
    write("site.webmanifest", json.dumps({
        "name": NAME, "short_name": "Grúa 24H BCN", "description": "Grúa y asistencia en carretera 24h en Barcelona",
        "start_url": "/", "display": "standalone", "background_color": "#0f0f10", "theme_color": "#0f0f10", "lang": "es",
        "icons": [{"src": "/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/img/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]},
        ensure_ascii=False, indent=2))
    write("llms.txt", f"# {NAME}\n\n> Servicio de grúa y asistencia en carretera 24 horas en Barcelona y área metropolitana.\n\n"
          f"- Teléfono y WhatsApp: {PHONE_FULL}\n- Horario: 24 horas, 365 días\n- Zonas: Barcelona, " + ", ".join(z["name"] for z in ZONES) +
          "\n- Servicios: " + ", ".join(s[1] for s in SERVICES) + f"\n- Web: {SITE}/\n")


if __name__ == "__main__":
    main()
