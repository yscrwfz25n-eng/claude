#!/bin/sh
# Renderiza posteo.html (2160 x 1350) y lo corta en slide-1.png y slide-2.png de 1080 x 1350.
set -e
cd "$(dirname "$0")"
/opt/pw-browsers/chromium-1194/chrome-linux/chrome --headless=new --no-sandbox --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=2160,1500 --virtual-time-budget=3000 \
  --screenshot=_captura.png "file://$PWD/posteo.html" 2>/dev/null
python3 -c "
from PIL import Image
im = Image.open('_captura.png').convert('RGB').crop((0, 0, 2160, 1350))
im.crop((0, 0, 1080, 1350)).save('slide-1.png')
im.crop((1080, 0, 2160, 1350)).save('slide-2.png')
im.resize((1080, 675)).save('vista-continua.png')"
rm -f _captura.png
echo "ok: slide-1.png slide-2.png"
