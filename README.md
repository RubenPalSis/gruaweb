# PL Grúas — web

Web estática (HTML + CSS, sin dependencias) para el servicio de grúa 24h en Barcelona.
Publicada con GitHub Pages desde la rama `main`.

## Editar y regenerar
1. Cambia la CONFIGURACIÓN en `build.py` (dominio, teléfono, servicios, zonas…).
2. Ejecuta `python3 build.py` y sube los cambios (`git add -A && git commit && git push`).

No edites los `.html` a mano: `build.py` los sobrescribe.

## Dominio propio
1. En `build.py`, pon tu dominio en `SITE` y ejecuta `python3 build.py`.
2. GitHub → Settings → Pages → Custom domain: escribe tu dominio y activa "Enforce HTTPS".
3. En tu proveedor de DNS: registro `CNAME` de `www` → `rubenpalsis.github.io`, y registros `A` del dominio raíz →
   185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153.
