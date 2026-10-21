"""Tendencia «tu mes de cumpleaños»: cada mes recibe una cita de The Dating List.

Uso:  python3 redes/tendencias/tu-mes/generar.py  ->  slide-01.png … slide-14.png (1080 x 1350)

Portada + 12 meses + cierre con el libro. Los números son los reales de la cita en el libro.
"""
import os
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

MESES = [
    ("ENERO", 23, "Picnic en una plaza o un parque."),
    ("FEBRERO", 81, "Recrear su primera cita."),
    ("MARZO", 21, "Ir a un bodegón que nunca probaron."),
    ("ABRIL", 2, "Maratón de una saga completa."),
    ("MAYO", 7, "Noche de pizza casera: cada uno arma la suya."),
    ("JUNIO", 47, "Pasar un día en unas termas."),
    ("JULIO", 61, "Aprender a jugar al truco y jugar un mano a mano."),
    ("AGOSTO", 64, "Hacer pastas caseras desde cero."),
    ("SEPTIEMBRE", 22, "Recorrer una feria de antigüedades o de diseño."),
    ("OCTUBRE", 44, "Mirar las estrellas lejos de la ciudad."),
    ("NOVIEMBRE", 24, "Ir al cine y elegir la película al azar."),
    ("DICIEMBRE", 82, "Cita sorpresa: uno organiza todo y el otro no sabe nada."),
]
# fondo, título, texto, acento: se alternan los tres fondos de la marca
TEMAS = [("#EEE7D8", "#142A40", "#142A40", "#1C82D9"), ("#9BD0EF", "#142A40", "#142A40", "#FBF8F1"),
         ("#142A40", "#EEE7D8", "#EEE7D8", "#9BD0EF")]

HEAD = """<!doctype html><html lang="es"><head><meta charset="utf-8">
<style>
  @font-face{font-family:Bungee;src:url('../../../fuentes/Bungee-Regular.ttf');}
  @font-face{font-family:Brico;src:url('../../../fuentes/BricolageGrotesque[opsz,wdth,wght].ttf');font-weight:200 800;}
  @font-face{font-family:Karla;src:url('../../../fuentes/Karla[wght].ttf');font-weight:200 800;}
  @font-face{font-family:Marker;src:url('../../../fuentes/PermanentMarker-Regular.ttf');}
  html,body{margin:0;width:1080px;height:1350px;overflow:hidden;}
  body{position:relative;background:FONDO;color:TEXTO;font-family:Karla;}
  .grano{position:absolute;inset:0;pointer-events:none;}
  .marcas{position:absolute;inset:0;}
  .logo{position:absolute;left:112px;top:92px;display:flex;align-items:center;gap:12px;font-family:Marker;font-size:30px;color:TEXTO;}
  .pag{position:absolute;right:112px;top:96px;font-family:Bungee;font-size:30px;color:ACENTO;}
  .centro{position:absolute;left:110px;right:110px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;}
</style></head><body>
<svg class="marcas" viewBox="0 0 1080 1350"><g stroke="TEXTO" stroke-width="3" opacity=".45">
  <path d="M40 70H90M70 40V90M1040 70H990M1010 40V90M40 1280H90M70 1310V1260M1040 1280H990M1010 1310V1260"/></g></svg>
<div class="logo"><svg width="40" height="40" viewBox="0 0 100 100"><circle cx="50" cy="50" r="34" fill="none" stroke="currentColor" stroke-width="10"/>
  <line x1="50" y1="2" x2="50" y2="98" stroke="currentColor" stroke-width="10"/><line x1="2" y1="50" x2="98" y2="50" stroke="currentColor" stroke-width="10"/>
  <circle cx="50" cy="50" r="12" fill="#1C82D9"/></svg>Oficina Gráfica</div>
<div class="pag">PAGINA</div>
"""
GRANO = """<svg class="grano" viewBox="0 0 1080 1350"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch"/>
<feColorMatrix values="0 0 0 0 0.08  0 0 0 0 0.16  0 0 0 0 0.25  0 0 0 0.5 0"/></filter><rect width="1080" height="1350" filter="url(#g)" opacity=".25"/></svg>
</body></html>"""


def pagina(n, total, tema, cuerpo):
    fondo, titulo, texto, acento = tema
    head = HEAD.replace("FONDO", fondo).replace("TEXTO", texto).replace("ACENTO", acento).replace("PAGINA", f"{n}/{total}")
    return head + cuerpo + GRANO


def portada():
    return """<div class="centro" style="align-items:center;text-align:center;">
  <div style="font-family:Brico;font-size:40px;font-weight:600;color:#1C82D9;letter-spacing:4px;">THE DATING LIST</div>
  <div style="font-family:Bungee;font-size:104px;line-height:1.02;margin-top:28px;">ELEGÍ TU MES<br>DE CUMPLE</div>
  <div style="font-size:46px;font-weight:500;margin-top:34px;line-height:1.3;">y te decimos qué cita<br>tienen que hacer</div>
  <div style="margin-top:70px;background:#142A40;color:#EEE7D8;border-radius:40px;padding:16px 40px;font-family:Brico;font-weight:700;font-size:32px;">deslizá →</div>
</div>"""


def mes(nombre, numero, cita, tema):
    _, titulo, texto, acento = tema
    size = 150 if len(nombre) <= 7 else 118
    return f"""<div class="centro">
  <div style="font-family:Brico;font-size:38px;font-weight:600;letter-spacing:5px;color:{acento};">SI NACISTE EN</div>
  <div style="font-family:Bungee;font-size:{size}px;line-height:1;margin:14px 0 70px;color:{titulo};">{nombre}</div>
  <div style="font-family:Brico;font-size:32px;font-weight:700;letter-spacing:4px;opacity:.75;">TU CITA ES LA N.º {numero}</div>
  <div style="font-size:70px;font-weight:700;line-height:1.15;margin-top:18px;">{cita}</div>
</div>"""


def cierre():
    return """<div class="centro" style="align-items:center;text-align:center;">
  <div style="font-family:Bungee;font-size:76px;line-height:1.05;">LAS OTRAS 88<br>ESTÁN ACÁ</div>
  <img src="../../regalito/libro-dating-list.png" style="height:640px;margin:44px 0 40px;transform:rotate(-4deg);filter:drop-shadow(0 22px 22px rgba(0,0,0,.35));">
  <div style="font-size:38px;font-weight:500;">Contanos en comentarios cuál te tocó.</div>
  <div style="margin-top:30px;background:#EEE7D8;color:#142A40;border-radius:40px;padding:16px 46px;font-family:Brico;font-weight:700;font-size:34px;">Pedilo por MD</div>
</div>"""


def main():
    total = len(MESES) + 2
    slides = [pagina(1, total, TEMAS[0], portada())]
    for i, (nombre, numero, cita) in enumerate(MESES):
        tema = TEMAS[(i + 1) % 3]
        slides.append(pagina(i + 2, total, tema, mes(nombre, numero, cita, tema)))
    slides.append(pagina(total, total, TEMAS[2], cierre()))
    for i, html in enumerate(slides, 1):
        ruta = os.path.join(AQUI, f"_slide-{i:02d}.html")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(html)
        png = os.path.join(AQUI, f"slide-{i:02d}.png")
        subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", "--window-size=1080,1500", "--virtual-time-budget=3000",
                        f"--screenshot={png}", "file://" + ruta], check=True, capture_output=True)
        from PIL import Image
        Image.open(png).convert("RGB").crop((0, 0, 1080, 1350)).save(png)
        os.remove(ruta)
    print("ok", len(slides), "slides")


if __name__ == "__main__":
    main()
