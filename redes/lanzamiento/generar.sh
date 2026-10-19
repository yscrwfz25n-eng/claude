#!/bin/sh
# Renderiza panorama.html con Chromium y lo corta en 3 posteos de 1080 x 1350.
set -e
cd "$(dirname "$0")"
/opt/pw-browsers/chromium-1194/chrome-linux/chrome --headless=new --no-sandbox --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=3240,1500 --virtual-time-budget=3000 \
  --screenshot=_captura.png "file://$PWD/panorama.html" 2>/dev/null
python3 - <<'PY'
from PIL import Image, ImageDraw
im = Image.open("_captura.png").convert("RGB").crop((0, 0, 3240, 1350))
im.save("panorama.png")
for i in range(3):
    # Instagram publica de derecha a izquierda: el posteo 1 es el que se sube último.
    im.crop((i * 1080, 0, (i + 1) * 1080, 1350)).save(f"posteo-{i + 1}.png")
# vista previa de la grilla del perfil (Instagram recorta cada posteo a 3:4 en la grilla)
recorte = (1080 - 1012) // 2
g = Image.new("RGB", (3 * 1012 + 2 * 8, 1350), "white")
for i in range(3):
    g.paste(im.crop((i * 1080 + recorte, 0, i * 1080 + recorte + 1012, 1350)), (i * (1012 + 8), 0))
g.resize((g.width // 2, g.height // 2)).save("vista-grilla.png")
print("ok: posteo-1/2/3.png, panorama.png, vista-grilla.png")
PY
rm -f _captura.png
