"""Piezas para la página de Facebook de Oficina Gráfica.

Uso:  python3 redes/facebook/generar.py
  -> perfil.png           foto de perfil 1080 x 1080 (Facebook la recorta en círculo)
  -> logo.png             logo horizontal (mira + «Oficina Gráfica») con fondo transparente
  -> logo-mira.png        solo la mira, con fondo transparente
  -> portada.png          portada 1640 x 624 (lo importante va en el centro: en el celular se recortan los costados)
"""
import os
import subprocess

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
FUENTES = """
  @font-face{font-family:Bungee;src:url('../../fuentes/Bungee-Regular.ttf');}
  @font-face{font-family:Brico;src:url('../../fuentes/BricolageGrotesque[opsz,wdth,wght].ttf');font-weight:200 800;}
  @font-face{font-family:Karla;src:url('../../fuentes/Karla[wght].ttf');font-weight:200 800;}
  @font-face{font-family:Marker;src:url('../../fuentes/PermanentMarker-Regular.ttf');}
  html,body{margin:0;overflow:hidden;}
"""


def mira(tam, color="#142A40", trazo=10):
    """La mira de registro como está en el perfil de Instagram: trazo grueso e irregular, de marcador."""
    sid = f"rough{tam}"
    return f"""<svg width="{tam}" height="{tam}" viewBox="-4 -4 108 108">
  <defs><filter id="{sid}" x="-10%" y="-10%" width="120%" height="120%">
    <feTurbulence type="fractalNoise" baseFrequency="0.06 0.08" numOctaves="2" seed="7" result="t"/>
    <feDisplacementMap in="SourceGraphic" in2="t" scale="3.2" xChannelSelector="R" yChannelSelector="G"/></filter></defs>
  <g filter="url(#{sid})">
  <circle cx="50" cy="50" r="35.5" fill="none" stroke="{color}" stroke-width="{trazo}"/>
  <line x1="50" y1="1" x2="50" y2="99" stroke="{color}" stroke-width="{trazo}"/>
  <line x1="1" y1="50" x2="99" y2="50" stroke="{color}" stroke-width="{trazo}"/>
  <circle cx="50" cy="50" r="11" fill="#3B7FD0"/></g></svg>"""


PIEZAS = {
    "perfil": (1080, 1080, False, f"""<body style="background:#EEE7D8;width:1080px;height:1080px;display:flex;align-items:center;justify-content:center;">
{mira(600)}</body>"""),
    "logo-mira": (1000, 1000, True, f"""<body style="background:transparent;width:1000px;height:1000px;display:flex;align-items:center;justify-content:center;">
{mira(1000)}</body>"""),
    "logo": (2000, 500, True, f"""<body style="background:transparent;width:2000px;height:500px;display:flex;align-items:center;justify-content:center;gap:50px;">
{mira(340)}<span style="font-family:Marker;font-size:230px;color:#142A40;line-height:1;">Oficina Gráfica</span></body>"""),
    "portada": (1640, 624, False, f"""<body style="background:#EEE7D8;width:1640px;height:624px;position:relative;font-family:Karla;color:#142A40;">
<svg style="position:absolute;left:0;top:0" width="1640" height="624"><g stroke="#142A40" stroke-width="3" opacity=".35">
  <path d="M300 60H350M325 35V85M1340 60H1290M1315 35V85M300 564H350M325 589V539M1340 564H1290M1315 589V539"/></g></svg>
<div style="position:absolute;left:285px;top:150px;width:560px;">
  <div style="display:flex;align-items:center;gap:14px;font-family:Marker;font-size:44px;">{mira(58)}Oficina Gráfica</div>
  <div style="font-family:Bungee;font-size:58px;line-height:1.02;margin-top:26px;">DISEÑO PROPIO,<br><span style="color:#1C82D9;">DEL BOCETO<br>AL PAPEL</span></div>
  <div style="font-size:28px;font-weight:600;margin-top:22px;">Juegos, libros y papelería · Pedidos por MD</div>
</div>
<img src="../regalito/libro-dating-list.png" style="position:absolute;left:880px;top:62px;height:330px;transform:rotate(-7deg);filter:drop-shadow(0 18px 20px rgba(20,42,64,.28));">
<img src="../vinos/libro-tapa.png" style="position:absolute;left:1075px;top:55px;height:330px;transform:rotate(6deg);filter:drop-shadow(0 18px 20px rgba(20,42,64,.28));">
<img src="../gemini/match-foto-final.jpg" style="position:absolute;left:860px;top:330px;height:250px;border-radius:18px;transform:rotate(-5deg);box-shadow:0 18px 30px rgba(20,42,64,.3);border:8px solid #FBF8F1;">
<img src="../gemini/opinologos-foto-final.jpg" style="position:absolute;left:1080px;top:338px;height:250px;border-radius:18px;transform:rotate(4deg);box-shadow:0 18px 30px rgba(20,42,64,.3);border:8px solid #FBF8F1;">
<svg style="position:absolute;left:0;top:0;pointer-events:none" width="1640" height="624"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch"/>
<feColorMatrix values="0 0 0 0 0.08  0 0 0 0 0.16  0 0 0 0 0.25  0 0 0 0.5 0"/></filter><rect width="1640" height="624" filter="url(#g)" opacity=".25"/></svg>
</body>"""),
}


def main():
    for nombre, (w, h, transparente, cuerpo) in PIEZAS.items():
        ruta = os.path.join(AQUI, f"_{nombre}.html")
        png = os.path.join(AQUI, f"{nombre}.png")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(f'<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{FUENTES}</style></head>{cuerpo}</html>')
        extra = ["--default-background-color=00000000"] if transparente else []
        subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", f"--window-size={w},{h + 200}", "--virtual-time-budget=3000",
                        *extra, f"--screenshot={png}", "file://" + ruta], check=True, capture_output=True)
        img = Image.open(png).crop((0, 0, w, h))
        if transparente:
            img = img.convert("RGBA")
            img = img.crop(img.getbbox())
        else:
            img = img.convert("RGB")
        img.save(png)
        os.remove(ruta)
    print("ok", ", ".join(PIEZAS))


if __name__ == "__main__":
    main()
