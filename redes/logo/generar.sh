#!/bin/sh
# Renderiza el carrusel con Chromium a 1080 x 1350: slide-1.html, slide-2.html y slide-3.html.
set -e
cd "$(dirname "$0")"
for f in slide-1 slide-2 slide-3; do
  /opt/pw-browsers/chromium-1194/chrome-linux/chrome --headless=new --no-sandbox --disable-gpu --hide-scrollbars \
    --force-device-scale-factor=1 --window-size=1080,1500 --virtual-time-budget=3000 \
    --screenshot=_captura.png "file://$PWD/$f.html" 2>/dev/null
  python3 -c "from PIL import Image; Image.open('_captura.png').convert('RGB').crop((0, 0, 1080, 1350)).save('$f.png')"
  echo "ok: $f.png"
done
rm -f _captura.png
