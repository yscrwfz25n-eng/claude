"""Historias (9:16) para los dos juegos: 3 de Match y 3 de Opinólogos.

Uso:  python3 redes/historias-juegos/generar.py  ->  match-1..3.png, opinologos-1..3.png (1080 x 1920)

1 · presentación con la foto del producto · 2 · una carta para interactuar (queda lugar para el sticker
de preguntas o de encuesta) · 3 · qué trae y «Pedilo por MD».
Cada juego usa su propia identidad (Match: negro, bordó y beige con DM Serif; Opinólogos: blanco y los
colores de los niveles con Poppins) y lleva la firma de Oficina Gráfica.
Los textos quedan entre y = 250 y y = 1580: arriba y abajo Instagram pone su interfaz.
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageOps

AQUI = os.path.dirname(os.path.abspath(__file__))
REDES = os.path.dirname(AQUI)
RAIZ = os.path.dirname(REDES)
sys.path.insert(0, REDES)
import foto_producto as fp  # noqa: E402

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
W, H = 1080, 1920

CSS = """<style>
  @font-face{font-family:DMSerif;src:url('../../fuentes/DMSerifDisplay-Regular.ttf');}
  @font-face{font-family:DMSerifIt;src:url('../../fuentes/DMSerifDisplay-Italic.ttf');}
  @font-face{font-family:Pop;src:url('../../fuentes/Poppins-Regular.ttf');font-weight:400;}
  @font-face{font-family:Pop;src:url('../../fuentes/Poppins-Medium.ttf');font-weight:500;}
  @font-face{font-family:Pop;src:url('../../fuentes/Poppins-Bold.ttf');font-weight:700;}
  @font-face{font-family:Pop;src:url('../../fuentes/Poppins-Black.ttf');font-weight:900;}
  @font-face{font-family:Marker;src:url('../../fuentes/PermanentMarker-Regular.ttf');}
  html,body{margin:0;width:1080px;height:1920px;overflow:hidden;}
  body{position:relative;font-family:Pop;}
  .abs{position:absolute;}
  .firma{position:absolute;left:0;right:0;top:250px;display:flex;justify-content:center;align-items:center;gap:10px;
         font-family:Marker;font-size:28px;}
  .pill{display:inline-block;border-radius:50px;padding:20px 54px;font-weight:700;font-size:38px;}
  .carta{position:absolute;filter:drop-shadow(0 30px 34px rgba(0,0,0,.35));}
</style>"""


def firma(color, top=250):
    return f"""<div class="firma" style="color:{color};top:{top}px;"><svg width="34" height="34" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="34" fill="none" stroke="currentColor" stroke-width="10"/>
  <line x1="50" y1="2" x2="50" y2="98" stroke="currentColor" stroke-width="10"/>
  <line x1="2" y1="50" x2="98" y2="50" stroke="currentColor" stroke-width="10"/>
  <circle cx="50" cy="50" r="12" fill="#1C82D9"/></svg>Oficina Gráfica</div>"""


def foto_vertical(ruta, salida, arriba=20):
    """Foto 4:5 entera, a todo el ancho: arriba se estira la pared lisa y abajo la mesa, hasta llenar el 9:16."""
    img = Image.open(ruta).convert("RGB")
    img = img.resize((W, round(img.height * W / img.width)), Image.LANCZOS)
    lienzo = Image.new("RGB", (W, H))
    lienzo.paste(img.crop((0, 0, W, 1)).resize((W, arriba)), (0, 0))
    lienzo.paste(img, (0, arriba))
    resto = H - arriba - img.height
    if resto > 0:
        lienzo.paste(img.crop((0, img.height - 1, W, img.height)).resize((W, resto)), (0, arriba + img.height))
    lienzo.save(salida, quality=94)


HISTORIAS = {
    # ---------- MATCH ----------
    "match-1": lambda: f"""<body style="background:url('_match-foto.jpg') center/cover;">
<div class="abs" style="left:0;right:0;bottom:0;height:720px;background:linear-gradient(rgba(15,13,13,0),rgba(15,13,13,.94) 45%);"></div>
{firma('#E6D5B8', 1650)}
<div class="abs" style="left:90px;right:90px;top:1270px;color:#E6D5B8;">
  <div style="font-family:DMSerifIt;font-size:150px;line-height:1;">match<span style="color:#C8102E;font-size:90px;"> oo</span></div>
  <div style="font-size:44px;margin-top:18px;">preguntas y retos para parejas</div>
  <div style="font-size:32px;letter-spacing:4px;margin-top:36px;color:#C8102E;font-weight:700;">2 JUGADORES · +18</div>
</div></body>""",
    "match-2": lambda: """<body style="background:#5C0F1E;">
""" + firma('#E6D5B8') + """
<div class="abs" style="left:90px;right:90px;top:360px;color:#E6D5B8;text-align:center;font-family:DMSerif;font-size:84px;line-height:1.08;">
  ¿Cuánto te conoce<br>tu pareja?</div>
<img class="carta" src="_match-pregunta.png" style="left:250px;top:640px;width:580px;transform:rotate(-4deg);">
<div class="abs" style="left:0;right:0;top:1460px;text-align:center;color:#E6D5B8;font-size:40px;font-weight:500;">
  Mandale esta historia y que responda ↓</div>
</body>""",
    "match-3": lambda: """<body style="background:#0F0D0D;">
""" + firma('#E6D5B8') + """
<div class="abs" style="left:90px;right:90px;top:360px;color:#E6D5B8;text-align:center;">
  <div style="font-family:DMSerif;font-size:96px;line-height:1.02;">Una noche<br>distinta</div>
  <div style="font-size:38px;margin-top:26px;opacity:.85;">90 preguntas · 30 retos · nada de pantallas</div>
</div>
<img class="carta" src="../regalito/caja-match.png" style="left:150px;top:760px;height:600px;transform:rotate(-6deg);">
<img class="carta" src="_match-reto.png" style="left:600px;top:860px;width:330px;transform:rotate(10deg);">
<div class="abs" style="left:0;right:0;top:1440px;text-align:center;">
  <span class="pill" style="background:#E6D5B8;color:#0F0D0D;">Pedilo por MD</span></div>
</body>""",
    # ---------- OPINÓLOGOS ----------
    "opinologos-1": lambda: f"""<body style="background:url('_opinologos-foto.jpg') center/cover;">
<div class="abs" style="left:0;right:0;bottom:0;height:720px;background:linear-gradient(rgba(17,17,17,0),rgba(17,17,17,.92) 45%);"></div>
{firma('#FFFFFF', 1650)}
<div class="abs" style="left:90px;right:90px;top:1290px;color:#FFFFFF;">
  <div style="font-weight:700;font-size:116px;line-height:1;letter-spacing:-3px;">opinólogos<span style="color:#2F6FED;">.</span><span style="color:#F08A24;">.</span><span style="color:#D7263D;">.</span></div>
  <div style="font-size:44px;margin-top:22px;">todos opinan, pocos convencen.</div>
  <div style="font-size:30px;letter-spacing:4px;margin-top:36px;font-weight:700;color:#F08A24;">4 A 8 JUGADORES · 14+ · 40–60 MIN</div>
</div></body>""",
    "opinologos-2": lambda: """<body style="background:#FFFFFF;">
<div class="abs" style="left:0;right:0;top:0;height:22px;display:flex;"><div style="flex:1;background:#2F6FED;"></div>
  <div style="flex:1;background:#F08A24;"></div><div style="flex:1;background:#D7263D;"></div></div>
""" + firma('#111111') + """
<div class="abs" style="left:90px;right:90px;top:360px;text-align:center;font-weight:900;font-size:96px;line-height:1;color:#111;letter-spacing:-2px;">
  ¿A FAVOR O<br>EN CONTRA?</div>
<img class="carta" src="_opinologos-tema.png" style="left:250px;top:620px;width:580px;transform:rotate(3deg);filter:drop-shadow(0 26px 30px rgba(0,0,0,.18));">
<div class="abs" style="left:0;right:0;top:1440px;text-align:center;color:#111;font-size:40px;font-weight:500;">
  Votá acá ↓ y defendé tu postura en comentarios</div>
</body>""",
    "opinologos-3": lambda: """<body style="background:#FFFFFF;">
<div class="abs" style="left:0;right:0;top:0;height:22px;display:flex;"><div style="flex:1;background:#2F6FED;"></div>
  <div style="flex:1;background:#F08A24;"></div><div style="flex:1;background:#D7263D;"></div></div>
""" + firma('#111111') + """
<div class="abs" style="left:90px;right:90px;top:360px;text-align:center;color:#111;">
  <div style="font-weight:900;font-size:92px;line-height:1;letter-spacing:-2px;">LA PREVIA<br>MÁS DISCUTIDA</div>
  <div style="font-size:36px;margin-top:28px;color:#555;">140 temas · 3 niveles · cartas de acción</div>
</div>
<img class="carta" src="../regalito/caja-opinologos.png" style="left:150px;top:760px;height:600px;transform:rotate(-5deg);filter:drop-shadow(0 26px 30px rgba(0,0,0,.2));">
<img class="carta" src="_opinologos-tema.png" style="left:610px;top:870px;width:320px;transform:rotate(9deg);filter:drop-shadow(0 20px 24px rgba(0,0,0,.2));">
<div class="abs" style="left:0;right:0;top:1440px;text-align:center;">
  <span class="pill" style="background:#111;color:#FFF;">Pedilo por MD</span></div>
</body>""",
}


def preparar_imagenes():
    with tempfile.TemporaryDirectory() as tmp:
        cartas = os.path.join(RAIZ, "match", "match-cartas.pdf")
        fp.carta(cartas, 1, 1, tmp).save(os.path.join(AQUI, "_match-pregunta.png"))
        fp.carta(cartas, 21, 0, tmp).save(os.path.join(AQUI, "_match-reto.png"))
        fp.carta(os.path.join(RAIZ, "opinologos-muestra-imprenta.pdf"), 1, 4, tmp).save(
            os.path.join(AQUI, "_opinologos-tema.png"))
    foto_vertical(os.path.join(REDES, "gemini", "match-foto-final.jpg"), os.path.join(AQUI, "_match-foto.jpg"))
    foto_vertical(os.path.join(REDES, "gemini", "opinologos-foto-final.jpg"), os.path.join(AQUI, "_opinologos-foto.jpg"))


def main():
    preparar_imagenes()
    for nombre, cuerpo in HISTORIAS.items():
        ruta = os.path.join(AQUI, f"_{nombre}.html")
        png = os.path.join(AQUI, f"{nombre}.png")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write('<!doctype html><html lang="es"><head><meta charset="utf-8">' + CSS + "</head>" + cuerpo() + "</html>")
        subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", "--window-size=1080,2100", "--virtual-time-budget=3000",
                        f"--screenshot={png}", "file://" + ruta], check=True, capture_output=True)
        Image.open(png).convert("RGB").crop((0, 0, W, H)).save(png)
        os.remove(ruta)
    print("ok", len(HISTORIAS), "historias")


if __name__ == "__main__":
    main()
