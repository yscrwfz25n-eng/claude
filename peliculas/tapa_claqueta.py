"""Tapa de THE WATCH LIST: claqueta gigante en diagonal, estilo afiche minimalista.

Uso:  python3 peliculas/tapa_claqueta.py
  -> peliculas/tapa-claqueta.png                  maqueta del cuaderno con elástico y cinta
  -> peliculas/the-watch-list-tapa-claqueta.pdf   arte A5 con 3 mm de sangrado, para imprenta

Las formas se definen sobre una grilla de 720 x 960 (la proporción del boceto) y se
escalan al A5.
"""
import math
import os
import random
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "citas"))

from portadas_personalizadas import PH, PW, Tapa, cuaderno, elastico  # noqa: E402  (registra fuentes)
from reportlab.lib.colors import HexColor  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402

INSTAGRAM = "@oficina.grafica_"
CREMA = HexColor("#F8EFDF")
NEGRO = HexColor("#1E1E1E")
GRIS = HexColor("#E9E9E9")
NARANJA = HexColor("#F2A33A")
BLANCO = HexColor("#FFFFFF")
CLAQUETA = Tapa("#1E1E1E", "#FFFFFF", "#1E1E1E", "#111111", "#1E1E1E")


def P(px, py):
    """Punto de la grilla 720 x 960 (origen arriba a la izquierda) a coordenadas de la tapa."""
    return px * PW / 720, (960 - py) * PH / 960


def poligono(cv, puntos, color):
    p = cv.beginPath()
    p.moveTo(*P(*puntos[0]))
    for pt in puntos[1:]:
        p.lineTo(*P(*pt))
    p.close()
    cv.setFillColor(color)
    cv.drawPath(p, stroke=0, fill=1)


def claqueta(cv):
    # cuerpo: todo lo que queda debajo del borde superior inclinado
    poligono(cv, [(-20, 428), (70, 444), (708, 272), (740, 290), (740, 980), (-20, 980)], NEGRO)
    for dx, dy in ((0, 0), (215, -56), (430, -112)):
        poligono(cv, [(115 + dx, 532 + dy), (226 + dx, 505 + dy), (282 + dx, 400 + dy), (171 + dx, 427 + dy)],
                 GRIS)
    # barra superior abierta
    poligono(cv, [(-20, 306), (604, -20), (632, 30), (628, 62), (30, 412), (-20, 398)], NEGRO)
    for dx, dy in ((0, 0), (194, -110), (388, -220)):
        poligono(cv, [(20 + dx, 302 + dy), (136 + dx, 334 + dy), (232 + dx, 278 + dy), (118 + dx, 248 + dy)],
                 GRIS)


def texto_en_diagonal(cv):
    x0, y0 = P(150, 406)  # paralelo al borde de la barra, dentro del hueco crema
    x1, y1 = P(600, 143)
    cv.saveState()
    cv.translate(x0, y0)
    cv.rotate(math.degrees(math.atan2(y1 - y0, x1 - x0)))
    cv.setFillColor(NEGRO)
    cv.setFont("PopM", 13)
    cv.drawString(0, 0, "toma 1 de 100")
    cv.restoreState()


def bloque_inferior(cv):
    x, _ = P(300, 0)
    cv.setFillColor(NARANJA)
    cv.setFont("PopM", 8.5)
    cv.drawString(x, P(0, 618)[1], "C H E C K   L I S T")
    # línea de película que atraviesa el número, con degradé de colores
    ly = P(0, 676)[1]
    cv.saveState()
    p = cv.beginPath()
    p.rect(P(400, 0)[0], ly - 0.5 * mm, PW + 5 * mm, 1 * mm)
    cv.clipPath(p, stroke=0, fill=0)
    cv.linearGradient(P(400, 0)[0], ly, PW, ly,
                      (HexColor("#E8572A"), HexColor("#F2C14E"), HexColor("#7CC29A"), HexColor("#F2A0A8"),
                       HexColor("#E8572A")), (0, 0.25, 0.5, 0.75, 1), extend=True)
    cv.restoreState()
    cv.setFillColor(BLANCO)
    cv.setFont("PopB", 64)
    cv.drawString(x - 1 * mm, P(0, 708)[1], "100")
    cv.setFont("PopM", 13.5)
    for i, linea in enumerate(("películas que hay que", "ver al menos una vez", "en la vida.")):
        cv.drawString(x, P(0, 770)[1] - i * 6.2 * mm, linea)
    # botón de play
    a, b, c = P(115, 650), P(115, 698), P(163, 674)
    cv.setStrokeColor(BLANCO)
    cv.setLineWidth(0.9)
    q = cv.beginPath()
    q.moveTo(*a)
    q.lineTo(*b)
    q.lineTo(*c)
    q.close()
    cv.drawPath(q, stroke=1, fill=0)
    cx = (a[0] + b[0] + c[0]) / 3
    cy = (a[1] + b[1] + c[1]) / 3
    r = cv.beginPath()
    r.moveTo(cx - 2.2 * mm, cy - 2.4 * mm)
    r.lineTo(cx - 2.2 * mm, cy + 2.4 * mm)
    r.lineTo(cx + 2.4 * mm, cy)
    r.close()
    cv.setFillColor(BLANCO)
    cv.drawPath(r, stroke=0, fill=1)


def textura(cv):
    rnd = random.Random(31)
    for _ in range(1800):
        claro = rnd.random() < 0.5
        cv.setFillColor(HexColor("#FFFFFF" if claro else "#000000"), alpha=0.04 if claro else 0.05)
        s = rnd.uniform(0.15, 0.4) * mm
        cv.rect(rnd.uniform(-3 * mm, PW + 3 * mm), rnd.uniform(-3 * mm, PH + 3 * mm), s, s, stroke=0, fill=1)
    cv.setFillColor(HexColor("#000000"), alpha=1)


def contenido(cv, x, y, s=0):
    cv.saveState()
    cv.translate(x, y)
    cv.setFillColor(CREMA)
    cv.rect(-s, -s, PW + 2 * s, PH + 2 * s, stroke=0, fill=1)
    claqueta(cv)
    texto_en_diagonal(cv)
    bloque_inferior(cv)
    textura(cv)
    cv.setFillColor(NEGRO)
    cv.setFont("DMSerif", 9)
    cv.drawString(10 * mm, PH - 13 * mm, INSTAGRAM)
    cv.restoreState()


def tapa(cv, x, y):
    cuaderno(cv, x, y, CLAQUETA)
    cv.saveState()
    p = cv.beginPath()
    p.roundRect(x, y, PW, PH, 3 * mm)
    cv.clipPath(p, stroke=0, fill=0)
    contenido(cv, x, y)
    cv.restoreState()
    elastico(cv, x, y, CLAQUETA)


def maqueta():
    m = 16 * mm
    pdf = os.path.join(AQUI, "tapa-claqueta.pdf")
    cv = canvas.Canvas(pdf, pagesize=(PW + 2 * m, PH + 2 * m))
    cv.setFillColor(HexColor("#F3ECE2"))
    cv.rect(0, 0, PW + 2 * m, PH + 2 * m, stroke=0, fill=1)
    tapa(cv, m, m + 4 * mm)
    cv.showPage()
    cv.save()
    subprocess.run(["pdftoppm", "-r", "150", "-png", "-singlefile", pdf, os.path.join(AQUI, "tapa-claqueta")],
                   check=True)
    os.remove(pdf)
    print("ok tapa-claqueta.png")


def imprimir():
    s = 3 * mm
    salida = os.path.join(AQUI, "the-watch-list-tapa-claqueta.pdf")
    cv = canvas.Canvas(salida, pagesize=(PW + 2 * s, PH + 2 * s))
    cv.setTitle("The Watch List – tapa")
    cv.setAuthor(INSTAGRAM)
    cv.setTrimBox((s, s, s + PW, s + PH))
    cv.setBleedBox((0, 0, PW + 2 * s, PH + 2 * s))
    contenido(cv, s, s, s)
    cv.showPage()
    cv.save()
    print("ok", os.path.basename(salida))


if __name__ == "__main__":
    maqueta()
    imprimir()
