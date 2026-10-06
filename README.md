# Asistencia 24H Barcelona — web

Web estática (HTML + CSS, sin dependencias) para el servicio de grúa 24h en Barcelona.

## Editar y regenerar
1. Abre `build.py` y cambia la CONFIGURACIÓN (dominio, teléfono, datos legales, Google Analytics, Search Console).
2. Ejecuta `python3 build.py` → regenera todas las páginas, `sitemap.xml`, `robots.txt` y el manifest.

## Publicar
Sube todo el contenido de la carpeta (excepto `logo.png`, `logo2.png` y `build.py`) a tu hosting.
`.htaccess` fuerza HTTPS + www, activa caché/compresión y la página 404 (hosting Apache).
