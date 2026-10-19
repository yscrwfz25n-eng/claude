"""Genera la tapa del ÁLBUM DE VINOS a partir de tapa.html.

Uso:  python3 vinos/generar_tapa.py
  -> vinos/album-de-vinos-tapa.pdf   A5 con 3 mm de sangrado (TrimBox/BleedBox), texto vectorial
  -> vinos/tapa.png                  maqueta del cuaderno con elástico y cinta
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

from portadas_personalizadas import PH, PW, Tapa, cuaderno, elastico  # noqa: E402
from reportlab.lib.colors import HexColor  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
SALIDA = os.path.join(AQUI, "album-de-vinos-tapa.pdf")
VINOS = Tapa("#F7F2EA", "#1B1716", "#E9E1D3", "#7A1832", "#7A1832")
S = 3 * mm


def pdf_de_imprenta(html="tapa.html", salida=SALIDA, titulo="Álbum de vinos – tapa"):
    """HTML de A5 + sangrado -> PDF con TrimBox y BleedBox."""
    crudo = os.path.join(tempfile.mkdtemp(), "crudo.pdf")
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=3000", f"--print-to-pdf={crudo}",
                    "file://" + os.path.join(AQUI, html)], check=True, capture_output=True)
    lector = PdfReader(crudo)
    hoja = lector.pages[0]
    w, h = float(hoja.mediabox.width), float(hoja.mediabox.height)
    hoja.trimbox = RectangleObject((S, S, w - S, h - S))
    hoja.bleedbox = RectangleObject((0, 0, w, h))
    escritor = PdfWriter()
    escritor.add_page(hoja)
    escritor.add_metadata({"/Title": titulo, "/Author": "@oficina.grafica_"})
    with open(salida, "wb") as f:
        escritor.write(f)
    print("ok", os.path.basename(salida), f"{w / mm:.1f} x {h / mm:.1f} mm")


def maqueta():
    tmp = tempfile.mkdtemp()
    base = os.path.join(tmp, "arte")
    subprocess.run(["pdftoppm", "-r", "200", "-png", "-singlefile", SALIDA, base], check=True)
    arte = Image.open(base + ".png")
    s = round(3 / 25.4 * 200)
    arte.crop((s, s, arte.width - s, arte.height - s)).save(base + "-corte.png")
    m = 16 * mm
    pdf = os.path.join(tmp, "maqueta.pdf")
    cv = canvas.Canvas(pdf, pagesize=(PW + 2 * m, PH + 2 * m))
    cv.setFillColor(HexColor("#E6DED1"))
    cv.rect(0, 0, PW + 2 * m, PH + 2 * m, stroke=0, fill=1)
    x, y = m, m + 4 * mm
    cuaderno(cv, x, y, VINOS)
    cv.saveState()
    p = cv.beginPath()
    p.roundRect(x, y, PW, PH, 3 * mm)
    cv.clipPath(p, stroke=0, fill=0)
    cv.drawImage(base + "-corte.png", x, y, PW, PH)
    cv.restoreState()
    elastico(cv, x, y, VINOS)
    cv.showPage()
    cv.save()
    subprocess.run(["pdftoppm", "-r", "150", "-png", "-singlefile", pdf, os.path.join(AQUI, "tapa")], check=True)
    print("ok tapa.png")


if __name__ == "__main__":
    pdf_de_imprenta()
    maqueta()
