"""Maqueta de THE WATCH LIST con la ilustración de referencia (sala de cine de papel) a sangre.

Uso:  python3 peliculas/tapa_foto.py  ->  peliculas/tapa-foto.png

OJO: la ilustración es de otro autor. Sirve para la maqueta; para vender hace falta
licencia del autor o una ilustración propia.
"""
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "citas"))

from portadas_personalizadas import PH, PW, Tapa, cuaderno, elastico  # noqa: E402  (registra fuentes)
from reportlab.lib.colors import HexColor  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402

IMAGEN = os.path.join(AQUI, "referencia-sala-papel.jpg")
IMG_W, IMG_H = 1000, 1138
INSTAGRAM = "@oficina.grafica_"
CREMA = HexColor("#FFF3E2")
SOMBRA = HexColor("#7E0F1C")
ROJO = Tapa("#C8202F", "#FFF3E2", "#C8202F", "#141414", "#C8202F")


def texto_con_sombra(cv, x, y, texto, fuente, size, centrado=True):
    for dx, dy, color in ((0.6, -0.6, SOMBRA), (0, 0, CREMA)):
        cv.setFillColor(color)
        cv.setFont(fuente, size)
        (cv.drawCentredString if centrado else cv.drawString)(x + dx * mm, y + dy * mm, texto)


def tapa(cv, x, y):
    cuaderno(cv, x, y, ROJO)
    cv.saveState()
    p = cv.beginPath()
    p.roundRect(x, y, PW, PH, 3 * mm)
    cv.clipPath(p, stroke=0, fill=0)
    alto = PH
    ancho = alto * IMG_W / IMG_H
    cv.drawImage(IMAGEN, x - 18 * mm, y, ancho, alto)  # recorte: 18 mm afuera a la izquierda
    # texto en la zona de butacas vacías (abajo a la derecha), a la izquierda del elástico
    cx = x + 101 * mm
    cv.setFillColor(CREMA)
    cv.setFont("PopSB", 7.5)
    texto_con_sombra(cv, cx, y + 64 * mm, "C H E C K   L I S T", "PopSB", 7.5)
    texto_con_sombra(cv, cx, y + 37 * mm, "100", "DMSerif", 62)
    texto_con_sombra(cv, cx + 1 * mm, y + 22 * mm, "películas", "Script", 34)
    texto_con_sombra(cv, cx, y + 8 * mm, INSTAGRAM, "DMSerif", 8)
    cv.restoreState()
    elastico(cv, x, y, ROJO)


def main():
    m = 16 * mm
    pdf = os.path.join(AQUI, "tapa-foto.pdf")
    cv = canvas.Canvas(pdf, pagesize=(PW + 2 * m, PH + 2 * m))
    cv.setFillColor(HexColor("#F3ECE2"))
    cv.rect(0, 0, PW + 2 * m, PH + 2 * m, stroke=0, fill=1)
    tapa(cv, m, m + 4 * mm)
    cv.showPage()
    cv.save()
    subprocess.run(["pdftoppm", "-r", "150", "-png", "-singlefile", pdf, os.path.join(AQUI, "tapa-foto")], check=True)
    os.remove(pdf)
    print("ok tapa-foto.png")


if __name__ == "__main__":
    main()
