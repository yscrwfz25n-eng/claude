#!/bin/sh
# Renderiza posteo.html con Chromium a 1080 x 1350.
set -e
cd "$(dirname "$0")"
/opt/pw-browsers/chromium-1194/chrome-linux/chrome --headless=new --no-sandbox --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=1080,1500 --virtual-time-budget=3000 \
  --screenshot=_captura.png "file://$PWD/posteo.html" 2>/dev/null
python3 -c "from PIL import Image; Image.open('_captura.png').convert('RGB').crop((0, 0, 1080, 1350)).save('posteo.png')"
rm -f _captura.png
echo "ok: posteo.png"
