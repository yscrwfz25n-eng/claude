"""Genera la tapa del ÁLBUM DE VINOS a partir de tapa.html.

Uso:  python3 vinos/generar_tapa.py
  -> vinos/album-de-vinos-tapa.pdf   A5 con 3 mm de sangrado (TrimBox/BleedBox), texto vectorial
  -> vinos/tapa.png                  maqueta del libro anillado
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "citas"))

from portadas_personalizadas import PH, PW  # noqa: E402
from reportlab.lib.colors import HexColor  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
SALIDA = os.path.join(AQUI, "album-de-vinos-tapa.pdf")
S = 3 * mm


def pdf_de_imprenta(html="tapa.html", salida=SALIDA, titulo="Álbum de vinos – tapa"):
    """HTML de A5 + sangrado -> PDF con TrimBox y BleedBox."""
    crudo = os.path.join(tempfile.mkdtemp(), "crudo.pdf")
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=3000", f"--print-to-pdf={crudo}",
                    "file://" + os.path.join(AQUI, html)], check=True, capture_output=True)
    escritor = PdfWriter()
    for hoja in PdfReader(crudo).pages:
        w, h = float(hoja.mediabox.width), float(hoja.mediabox.height)
        hoja.trimbox = RectangleObject((S, S, w - S, h - S))
        hoja.bleedbox = RectangleObject((0, 0, w, h))
        escritor.add_page(hoja)
    escritor.add_metadata({"/Title": titulo, "/Author": "@oficina.grafica_"})
    with open(salida, "wb") as f:
        escritor.write(f)
    print("ok", os.path.basename(salida), f"{len(escritor.pages)} pág. de {w / mm:.1f} x {h / mm:.1f} mm")


PASO_ESPIRAL = 8.47 * mm  # anillado doble alambre 3:1


def bloque_y_sombra(cv, x, y):
    """Sombra y canto de hojas que asoma por abajo y por el borde libre."""
    cv.setFillColor(HexColor("#000000"), alpha=0.16)
    cv.roundRect(x + 2.5 * mm, y - 3 * mm, PW, PH, 2 * mm, stroke=0, fill=1)
    for i, tono in enumerate(("#D9D2C6", "#E8E2D7", "#F3EFE8")):
        d = (3 - i) * 0.55 * mm
        cv.setFillColor(HexColor(tono), alpha=1)
        cv.roundRect(x + d, y - d, PW, PH, 1.5 * mm, stroke=0, fill=1)


def espiral(cv, x, y):
    """Anillos metálicos del lado del lomo (izquierdo): agujeros en la tapa y lazos que la abrazan."""
    n = int((PH - 8 * mm) // PASO_ESPIRAL)
    y0 = y + (PH - (n - 1) * PASO_ESPIRAL) / 2
    for i in range(n):
        cy = y0 + i * PASO_ESPIRAL
        for dy in (-1.3 * mm, 1.3 * mm):
            cv.setFillColor(HexColor("#2A2523"), alpha=1)
            cv.roundRect(x + 4.2 * mm, cy + dy - 0.75 * mm, 2.4 * mm, 1.5 * mm, 0.7 * mm, stroke=0, fill=1)
            # lazo: sale del agujero, rodea el lomo y vuelve por detrás
            for ancho, color in ((1.05 * mm, "#6E6A66"), (0.75 * mm, "#B9B5B0"), (0.28 * mm, "#F2F0EC")):
                cv.setStrokeColor(HexColor(color))
                cv.setLineWidth(ancho)
                cv.setLineCap(1)
                p = cv.beginPath()
                p.moveTo(x + 5.6 * mm, cy + dy)
                p.curveTo(x + 2 * mm, cy + dy + 1.4 * mm, x - 4.2 * mm, cy + dy + 1.2 * mm, x - 4.6 * mm, cy + dy - 0.4 * mm)
                cv.drawPath(p, stroke=1, fill=0)


def maqueta(pdf_arte=SALIDA, png=os.path.join(AQUI, "tapa.png"), espejo=False, transparente=False):
    """Libro anillado con la tapa puesta. espejo=True: contratapa (el espiral queda a la derecha).
    transparente=True: sin fondo (PNG con alfa, para montar en posteos)."""
    tmp = tempfile.mkdtemp()
    base = os.path.join(tmp, "arte")
    subprocess.run(["pdftoppm", "-r", "200", "-png", "-singlefile", pdf_arte, base], check=True)
    arte = Image.open(base + ".png")
    s = round(3 / 25.4 * 200)
    arte.crop((s, s, arte.width - s, arte.height - s)).save(base + "-corte.png")
    m = 16 * mm
    pdf = os.path.join(tmp, "maqueta.pdf")
    cv = canvas.Canvas(pdf, pagesize=(PW + 2 * m, PH + 2 * m))
    if not transparente:
        cv.setFillColor(HexColor("#E6DED1"))
        cv.rect(0, 0, PW + 2 * m, PH + 2 * m, stroke=0, fill=1)
    x, y = m, m + 2 * mm

    def espejado(dibujo):
        cv.saveState()
        if espejo:
            cv.translate(2 * x + PW, 0)
            cv.scale(-1, 1)
        dibujo(cv, x, y)
        cv.restoreState()

    espejado(bloque_y_sombra)
    cv.saveState()
    p = cv.beginPath()
    p.roundRect(x, y, PW, PH, 1.5 * mm)
    cv.clipPath(p, stroke=0, fill=0)
    cv.drawImage(base + "-corte.png", x, y, PW, PH)
    cv.restoreState()
    espejado(espiral)
    cv.showPage()
    cv.save()
    if transparente:
        subprocess.run(["pdftocairo", "-r", "200", "-png", "-transp", "-singlefile", pdf, png[:-4]], check=True)
    else:
        subprocess.run(["pdftoppm", "-r", "150", "-png", "-singlefile", pdf, png[:-4]], check=True)
    print("ok", os.path.basename(png))


if __name__ == "__main__":
    pdf_de_imprenta()
    maqueta()
