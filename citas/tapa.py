"""Tapa elegida de THE DATING LIST: bordó, logotipo serif + manuscrita y «100» tono sobre tono.

Uso:  python3 citas/tapa.py  ->  citas/tapa.png (maqueta del cuaderno con elástico y cinta)
"""
import os
import subprocess

from portadas_personalizadas import AQUI, BORDO, PH, PW, cuaderno, elastico, fondo_100, logotipo
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

INSTAGRAM = "@oficina.grafica_"


def tapa(cv, x, y, t=BORDO):
    cuaderno(cv, x, y, t)
    fondo_100(cv, x, y, t)
    cx = x + PW / 2 - 4 * mm  # centrado en el área libre a la izquierda del elástico
    cv.setFillColor(t.tinta)
    cv.setFont("DMSerif", 11)
    cv.drawCentredString(cx, y + PH - 24 * mm, INSTAGRAM)
    logotipo(cv, cx, y + PH / 2 + 6 * mm, t)
    cv.setFont("PopR", 7.5)
    cv.drawCentredString(cx, y + 50 * mm, "100 citas para hacer juntos")
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
