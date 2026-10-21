"""Tendencia «cosas que le diría a mi yo de antes», en formato collage desprolijo (notas, cinta, garabatos).

Uso:  python3 redes/tendencias/mi-yo/generar.py  ->  slide-1.png … slide-6.png (1080 x 1350)

Cinco aprendizajes reales de imprenta: sirven como contenido útil y muestran el oficio.
"""
import importlib.util
import os
import subprocess

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("tu_mes", os.path.join(os.path.dirname(AQUI), "tu-mes", "generar.py"))
tu_mes = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tu_mes)
PAPEL = ("#EEE7D8", "#142A40", "#142A40", "#1C82D9")

ESTILO = """<style>
  .nota{position:absolute;background:#FBF8F1;box-shadow:0 14px 26px rgba(20,42,64,.18);padding:56px 60px;box-sizing:border-box;}
  .cinta{position:absolute;width:170px;height:46px;background:rgba(155,208,239,.75);}
  .num{font-family:Bungee;font-size:120px;line-height:1;color:#1C82D9;}
  .tit{font-family:Bungee;font-size:62px;line-height:1.08;color:#142A40;margin-top:18px;}
  .txt{font-size:36px;line-height:1.38;font-weight:500;color:#142A40;margin-top:26px;}
  .garabato{position:absolute;fill:none;stroke:#1C82D9;stroke-width:7;stroke-linecap:round;stroke-linejoin:round;}
</style>"""


def nota(numero, titulo, texto, angulo, extra=""):
    return f"""{ESTILO}
<div class="nota" style="left:120px;top:250px;width:840px;transform:rotate({angulo}deg);">
  <div class="cinta" style="left:-40px;top:-18px;transform:rotate(-24deg);"></div>
  <div class="cinta" style="right:-40px;top:-18px;transform:rotate(22deg);"></div>
  <div class="num">{numero}</div>
  <div class="tit">{titulo}</div>
  <div class="txt">{texto}</div>
</div>
{extra}"""


PORTADA = ESTILO + """
<div class="nota" style="left:130px;top:330px;width:820px;transform:rotate(-2.5deg);text-align:left;">
  <div class="cinta" style="left:320px;top:-22px;transform:rotate(3deg);"></div>
  <div class="tit" style="font-size:84px;margin-top:0;">COSAS QUE LE DIRÍA A MI YO DEL PRIMER PEDIDO</div>
  <div class="txt" style="font-size:38px;">5 cosas de imprenta que nadie te cuenta</div>
</div>
<svg class="garabato" style="left:610px;top:900px;" width="300" height="120"><path d="M10 60C60 20 120 100 180 50S260 30 290 70"/><path d="M262 52l30 18-34 10"/></svg>
<div style="position:absolute;left:700px;top:1010px;font-family:Brico;font-weight:700;font-size:34px;color:#142A40;">deslizá</div>
"""

LECCIONES = [
    ("01", "IMPRIMÍ UNA PRUEBA ANTES DE IMPRIMIR CIEN",
     "Un error en la pantalla se arregla con un clic. En cien hojas impresas, se paga cien veces.", -1.5,
     """<div style="position:absolute;left:170px;top:930px;font-family:Bungee;font-size:96px;color:#142A40;opacity:.35;text-decoration:line-through;text-decoration-color:#1C82D9;">×100</div>
<div style="position:absolute;left:560px;top:920px;font-family:Bungee;font-size:110px;color:#142A40;">×1</div>
<svg class="garabato" style="left:520px;top:880px;" width="230" height="200"><ellipse cx="115" cy="100" rx="100" ry="80" transform="rotate(-8 115 100)"/></svg>"""),
    ("02", "LA PANTALLA MIENTE",
     "La pantalla arma los colores con luz (RGB) y la impresora con tinta (CMYK). El mismo azul sale más apagado en papel.", 1.2,
     """<div style="position:absolute;left:190px;top:1000px;display:flex;gap:60px;font-family:Brico;font-weight:700;font-size:28px;color:#142A40;text-align:center;">
  <div><div style="width:300px;height:170px;border-radius:16px;background:#1C82D9;"></div><div style="margin-top:14px;">en pantalla</div></div>
  <div><div style="width:300px;height:170px;border-radius:16px;background:#3A79AE;"></div><div style="margin-top:14px;">en papel</div></div>
</div>"""),
    ("03", "3 MM DE SANGRADO. SIEMPRE.",
     "Si el color llega al borde, estiralo 3 mm más allá del corte. La guillotina nunca corta perfecto.", -1,
     """<svg style="position:absolute;left:330px;top:900px;" width="420" height="380" viewBox="0 0 420 380">
  <text x="40" y="30" font-family="Bungee" font-size="26" fill="#142A40">3 MM</text>
  <path d="M40 44V64M70 44V64M40 54H70" stroke="#1C82D9" stroke-width="4" fill="none"/>
  <rect x="40" y="70" width="320" height="290" fill="#9BD0EF"/>
  <rect x="70" y="100" width="260" height="230" fill="none" stroke="#142A40" stroke-width="4" stroke-dasharray="14 10"/>
  <text x="200" y="222" font-family="Brico" font-weight="700" font-size="24" fill="#142A40" text-anchor="middle">corte</text>
</svg>"""),
    ("04", "LA CAJA TAMBIÉN VENDE",
     "Antes de abrir el juego, la gente ve la caja. Por eso la diseñamos con el mismo cuidado que las cartas.", 1.5,
     """<img src="../../regalito/caja-match.png" style="position:absolute;left:400px;top:900px;height:360px;transform:rotate(-5deg);filter:drop-shadow(0 18px 18px rgba(0,0,0,.3));">"""),
    ("05", "HACÉ LO QUE VOS REGALARÍAS",
     "Si no te dan ganas de regalarlo, no lo hagas. Esa es nuestra única regla antes de lanzar algo.", -1.2,
     """<svg class="garabato" style="left:430px;top:930px;" width="240" height="220" viewBox="0 0 240 220">
  <path d="M120 70C95 20 20 30 30 95C40 150 110 185 120 200C130 185 200 150 210 95C220 30 145 20 120 70Z"/></svg>"""),
]


def render(html, png):
    ruta = png[:-4] + ".html"
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(html)
    subprocess.run([tu_mes.CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=1080,1500", "--virtual-time-budget=3000",
                    f"--screenshot={png}", "file://" + ruta], check=True, capture_output=True)
    Image.open(png).convert("RGB").crop((0, 0, 1080, 1350)).save(png)
    os.remove(ruta)


def main():
    total = len(LECCIONES) + 1
    render(tu_mes.pagina(1, total, PAPEL, PORTADA), os.path.join(AQUI, "slide-1.png"))
    for i, (num, tit, txt, ang, extra) in enumerate(LECCIONES, 2):
        render(tu_mes.pagina(i, total, PAPEL, nota(num, tit, txt, ang, extra)), os.path.join(AQUI, f"slide-{i}.png"))
    print("ok", total, "slides")


if __name__ == "__main__":
    main()
