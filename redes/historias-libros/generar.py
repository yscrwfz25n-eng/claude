"""Una historia 9:16 por libro: The Dating List, Álbum de vinos y Álbum de alfajores.

Uso:  python3 redes/historias-libros/generar.py  ->  dating-list.png, vinos.png, alfajores.png

Cada una usa la identidad de su libro, muestra el libro (y una página de adentro cuando la tenemos)
y cierra con «Pedilo por MD» y la firma de Oficina Gráfica. Textos entre y = 250 y y = 1580.
Las páginas de The Dating List salen de citas/the-dating-list-interior.pdf (pdftoppm, ver README del
repo); se guardan como _dl-4.png y _dl-8.png, que no se versionan.
"""
import os
import subprocess

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

CSS = """<style>
  @font-face{font-family:DMSerif;src:url('../../fuentes/DMSerifDisplay-Regular.ttf');}
  @font-face{font-family:DMSerifIt;src:url('../../fuentes/DMSerifDisplay-Italic.ttf');}
  @font-face{font-family:Bebas;src:url('../../fuentes/BebasNeue-Regular.ttf');}
  @font-face{font-family:Sacramento;src:url('../../fuentes/Sacramento-Regular.ttf');}
  @font-face{font-family:Bungee;src:url('../../fuentes/Bungee-Regular.ttf');}
  @font-face{font-family:Archivo;src:url('../../fuentes/ArchivoBlack-Regular.ttf');}
  @font-face{font-family:Pop;src:url('../../fuentes/Poppins-Medium.ttf');font-weight:500;}
  @font-face{font-family:Pop;src:url('../../fuentes/Poppins-Bold.ttf');font-weight:700;}
  @font-face{font-family:Pop;src:url('../../fuentes/Poppins-Black.ttf');font-weight:900;}
  @font-face{font-family:Marker;src:url('../../fuentes/PermanentMarker-Regular.ttf');}
  html,body{margin:0;width:1080px;height:1920px;overflow:hidden;}
  body{position:relative;font-family:Pop;}
  .abs{position:absolute;}
  .sombra{filter:drop-shadow(0 26px 30px rgba(0,0,0,.3));}
  .pill{display:inline-block;border-radius:50px;padding:20px 56px;font-weight:700;font-size:38px;}
</style>"""


def firma(color, top=250):
    return f"""<div class="abs" style="left:0;right:0;top:{top}px;display:flex;justify-content:center;align-items:center;gap:10px;
  font-family:Marker;font-size:28px;color:{color};"><svg width="34" height="34" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="34" fill="none" stroke="currentColor" stroke-width="10"/>
  <line x1="50" y1="2" x2="50" y2="98" stroke="currentColor" stroke-width="10"/>
  <line x1="2" y1="50" x2="98" y2="50" stroke="currentColor" stroke-width="10"/>
  <circle cx="50" cy="50" r="12" fill="#1C82D9"/></svg>Oficina Gráfica</div>"""


def cta(fondo, texto):
    return f"""<div class="abs" style="left:0;right:0;top:1490px;text-align:center;">
  <span class="pill" style="background:{fondo};color:{texto};">Pedilo por MD</span></div>"""


def bebas(texto, size, color):
    """Bebas con las O redondas, como en la tapa del álbum de vinos."""
    o, b = size * 0.69, size * 0.11
    html = "".join(f'<span style="display:inline-block;width:{o}px;height:{o}px;border:{b}px solid {color};border-radius:50%;'
                   f'box-sizing:border-box;margin:0 {size * .02}px;"></span>' if ch == "O" else ("&nbsp;" if ch == " " else ch)
                   for ch in texto)
    return (f'<div style="font-family:Bebas;font-size:{size}px;line-height:1;color:{color};display:flex;'
            f'justify-content:center;align-items:center;">{html}</div>')


def recortes(texto):
    """Letras recortadas de distintos papeles, como el título de la tapa del álbum de alfajores."""
    estilos = [("Bungee", "#F5C518", "#2B2B2B", -6), ("DMSerif", "#E9447A", "#FFFFFF", 4), ("Archivo", "#2F6FED", "#FFF6D5", -3),
               ("Pop", "#3BB273", "#FFFFFF", 5), ("DMSerifIt", "#F08A24", "#2B2B2B", -4), ("Bungee", "#7B4FD6", "#FFFFFF", 3),
               ("Archivo", "#D7263D", "#FFFFFF", -5)]
    html = ""
    for i, ch in enumerate(texto):
        if ch == " ":
            html += '<span style="display:inline-block;width:26px;"></span>'
            continue
        fuente, fondo, color, ang = estilos[i % len(estilos)]
        peso = "900" if fuente == "Pop" else "400"
        html += (f'<span style="display:inline-block;font-family:{fuente};font-weight:{peso};font-size:86px;line-height:1;'
                 f'background:{fondo};color:{color};padding:10px 12px 6px;margin:4px 3px;transform:rotate({ang}deg);'
                 f'box-shadow:0 6px 10px rgba(0,0,0,.15);">{ch}</span>')
    return html


ASTERISCO = '<path d="M0 -30L6 -8L28 -14L12 2L26 22L4 12L-6 32L-8 10L-30 6L-10 -6Z"/>'

HISTORIAS = {
    "dating-list": lambda: f"""<body style="background:#5C0F1E;color:#EFE3D0;">
{firma('#EFE3D0')}
<div class="abs" style="left:0;right:0;top:340px;text-align:center;">
  <div style="font-family:DMSerif;font-size:112px;line-height:1;">100 citas</div>
  <div style="font-family:DMSerifIt;font-size:58px;margin-top:14px;">para hacer juntos</div>
</div>
<img class="abs sombra" src="../regalito/libro-dating-list.png" style="left:110px;top:650px;height:600px;transform:rotate(-7deg);">
<img class="abs sombra" src="_dl-4.png" style="left:560px;top:690px;width:410px;transform:rotate(6deg);">
<div class="abs" style="left:0;right:0;top:1385px;text-align:center;font-size:40px;font-weight:500;">
  Tildá cada una y anotá cómo les fue ✓</div>
{cta('#EFE3D0', '#5C0F1E')}
</body>""",
    "vinos": lambda: f"""<body style="background:#F7F2EA;color:#1B1716;">
{firma('#1B1716')}
<div class="abs" style="left:0;right:0;top:330px;text-align:center;">
  {bebas('UNA BOTELLA,', 128, '#1B1716')}{bebas('UNA PÁGINA', 128, '#7A1832')}
  <div style="font-family:Sacramento;font-size:62px;color:#7A1832;margin-top:4px;">para cada vino que valga la pena</div>
</div>
<img class="abs sombra" src="../vinos/libro-tapa.png" style="left:95px;top:700px;height:590px;transform:rotate(-6deg);">
<img class="abs sombra" src="../../vinos/pagina-muestra.png" style="left:570px;top:735px;width:400px;transform:rotate(5deg);">
<div class="abs" style="left:0;right:0;top:1395px;text-align:center;font-size:38px;font-weight:500;">
  Fecha, cepa, estrellas y la etiqueta pegada</div>
{cta('#7A1832', '#F7F2EA')}
</body>""",
    "alfajores": lambda: f"""<body style="background:#FFFDF7;color:#2B2B2B;">
{firma('#2B2B2B')}
<div class="abs" style="left:60px;right:60px;top:330px;text-align:center;">{recortes('ÁLBUM DE')}<br>{recortes('ALFAJORES')}</div>
<svg class="abs" style="left:0;top:0;" width="1080" height="1920">
  <g fill="#E9447A"><g transform="translate(130 760) scale(1.3)">{ASTERISCO}</g><g transform="translate(960 1310) scale(1.1)">{ASTERISCO}</g></g>
  <g fill="#D7263D"><g transform="translate(940 720) scale(.8)">{ASTERISCO}</g><g transform="translate(150 1330) scale(.7)">{ASTERISCO}</g></g>
</svg>
<img class="abs sombra" src="../regalito/album-alfajores.png" style="left:190px;top:700px;width:700px;transform:rotate(-3deg);">
<div class="abs" style="left:0;right:0;top:1390px;text-align:center;font-size:42px;font-weight:700;">
  Probalos todos. Anotalos todos.</div>
{cta('#2B2B2B', '#FFFDF7')}
</body>""",
}


def main():
    for nombre, cuerpo in HISTORIAS.items():
        ruta = os.path.join(AQUI, f"_{nombre}.html")
        png = os.path.join(AQUI, f"{nombre}.png")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write('<!doctype html><html lang="es"><head><meta charset="utf-8">' + CSS + "</head>" + cuerpo() + "</html>")
        subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", "--window-size=1080,2100", "--virtual-time-budget=3000",
                        f"--screenshot={png}", "file://" + ruta], check=True, capture_output=True)
        Image.open(png).convert("RGB").crop((0, 0, 1080, 1920)).save(png)
        os.remove(ruta)
    print("ok", len(HISTORIAS), "historias")


if __name__ == "__main__":
    main()
