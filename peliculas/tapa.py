"""Tapa de THE WATCH LIST: mismo sistema que The Dating List, en azul noche.

Uso:  python3 peliculas/tapa.py  ->  peliculas/tapa.png (maqueta del cuaderno con elástico y cinta)
"""
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "citas"))

from portadas_personalizadas import PH, PW, Tapa, cien, cuaderno, elastico, logotipo  # noqa: E402
from reportlab.lib.colors import HexColor  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402

INSTAGRAM = "@oficina.grafica_"
# fondo, tinta, sombra, elástico, «100»
NOCHE = Tapa("#1B2033", "#EFE3D0", "#242A40", "#0E0E12", "#39415E")


def tapa(cv, x, y, t=NOCHE):
    cuaderno(cv, x, y, t)
    cv.saveState()
    p = cv.beginPath()
    p.roundRect(x, y, PW, PH, 3 * mm)
    cv.clipPath(p, stroke=0, fill=0)
    cien(cv, x + 38 * mm, y - 12 * mm, t)
    cv.restoreState()
    cx = x + PW / 2 - 4 * mm  # centrado en el área libre a la izquierda del elástico
    cv.setFillColor(t.tinta)
    cv.setFont("DMSerif", 11)
    cv.drawCentredString(cx, y + PH - 24 * mm, INSTAGRAM)
    logotipo(cv, cx, y + PH / 2 + 6 * mm, t, palabra="Watch")
    cv.setFillColor(t.tinta)
    cv.setFont("PopR", 7.5)
    cv.drawCentredString(cx, y + 50 * mm, "100 películas y series para ver")
    elastico(cv, x, y, t)


def main():
    m = 16 * mm
    pdf = os.path.join(AQUI, "tapa.pdf")
    cv = canvas.Canvas(pdf, pagesize=(PW + 2 * m, PH + 2 * m))
    cv.setFillColor(HexColor("#F3ECE2"))
    cv.rect(0, 0, PW + 2 * m, PH + 2 * m, stroke=0, fill=1)
    tapa(cv, m, m + 4 * mm)
    cv.showPage()
    cv.save()
    subprocess.run(["pdftoppm", "-r", "150", "-png", "-singlefile", pdf, os.path.join(AQUI, "tapa")], check=True)
    os.remove(pdf)
    print("ok tapa.png")


if __name__ == "__main__":
    main()
