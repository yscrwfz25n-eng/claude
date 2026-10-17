"""Imagen 9:16 (1080 x 1920) con una frase de amor, para historias de Instagram.

Uso:  python3 redes/frase_amor.py  ->  redes/frase-amor.png
"""
import os
import random
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path[:0] = [RAIZ, os.path.join(RAIZ, "citas")]

import portadas_personalizadas  # noqa: E402,F401  (registra DM Serif, Poppins y Script)
from reportlab.lib.colors import HexColor  # noqa: E402
from reportlab.lib.enums import TA_CENTER  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402
from reportlab.platypus import Paragraph  # noqa: E402

W, H = 540, 960  # puntos; se exporta a 144 dpi -> 1080 x 1920 px
CREMA = HexColor("#F6EEE3")
BORDO = HexColor("#5C0F1E")
ROJO = HexColor("#C8102E")

FRASE = ("Soy fiel al pensamiento de que no hay tinta suficiente ni hoja lo bastante grande para "
         "los sentimientos de un enamorado. Pero voy a esforzarme para que, en unas pocas hojas, "
         "pueda explicarte todo lo que atraviesa mi cuerpo y mi mente cada vez que me besas, "
         "me abrazas o solo me miras a los ojos.")
CIERRE = "Casi como si fuera una cuestión religiosa."
INSTAGRAM = "@oficina.grafica_"


def corazon(cv, cx, cy, s, color):
    p = cv.beginPath()
    p.moveTo(cx, cy - s * 0.45)
    p.curveTo(cx - s * 0.55, cy - s * 0.05, cx - s * 0.5, cy + s * 0.45, cx, cy + s * 0.2)
    p.curveTo(cx + s * 0.5, cy + s * 0.45, cx + s * 0.55, cy - s * 0.05, cx, cy - s * 0.45)
    p.close()
    cv.setFillColor(color)
    cv.drawPath(p, stroke=0, fill=1)


def main():
    pdf = os.path.join(AQUI, "frase-amor.pdf")
    cv = canvas.Canvas(pdf, pagesize=(W, H))
    cv.setFillColor(CREMA)
    cv.rect(0, 0, W, H, stroke=0, fill=1)
    rnd = random.Random(4)  # grano de papel
    for _ in range(2500):
        cv.setFillColor(HexColor("#8A6B4E"), alpha=rnd.uniform(0.03, 0.08))
        s = rnd.uniform(0.3, 0.9)
        cv.rect(rnd.uniform(0, W), rnd.uniform(0, H), s, s, stroke=0, fill=1)
    cv.setFillColor(BORDO, alpha=1)
    # marco fino
    cv.setStrokeColor(BORDO)
    cv.setLineWidth(0.8)
    cv.rect(28, 28, W - 56, H - 56, stroke=1, fill=0)
    # comillas grandes
    cv.setFillColor(ROJO)
    cv.setFont("DMSerif", 120)
    cv.drawCentredString(W / 2, 655, "“")
    # frase
    estilo = ParagraphStyle("f", fontName="DMSerifIt", fontSize=25, leading=34, textColor=BORDO,
                            alignment=TA_CENTER)
    p = Paragraph(FRASE, estilo)
    ancho = W - 150
    _, alto = p.wrap(ancho, 600)
    top = 650
    p.drawOn(cv, (W - ancho) / 2, top - alto)
    y = top - alto - 62
    cv.setFillColor(ROJO)
    cv.setFont("Script", 36)
    cv.drawCentredString(W / 2, y, CIERRE)
    corazon(cv, W / 2, y - 42, 16, ROJO)
    cv.setFillColor(BORDO)
    cv.setFont("DMSerif", 11)
    cv.drawCentredString(W / 2, 160, INSTAGRAM)
    cv.showPage()
    cv.save()
    subprocess.run(["pdftoppm", "-r", "144", "-png", "-singlefile", pdf, os.path.join(AQUI, "frase-amor")],
                   check=True)
    os.remove(pdf)
    print("ok frase-amor.png", f"(alto del texto: {alto:.0f} pt)")


if __name__ == "__main__":
    main()
