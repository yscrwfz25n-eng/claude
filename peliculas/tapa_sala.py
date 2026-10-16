"""Tapa de THE WATCH LIST: sala de cine vacía en perspectiva, toda en azules.

Uso:  python3 peliculas/tapa_sala.py
  -> peliculas/tapa-sala.png                  maqueta del cuaderno con elástico y cinta
  -> peliculas/the-watch-list-tapa-sala.pdf   arte A5 con 3 mm de sangrado, para imprenta

Ilustración vectorial propia; en la pantalla: «CHECK LIST · 100 PELÍCULAS».
"""
import os
import random
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "citas"))

from portadas_personalizadas import PH, PW, Tapa, cuaderno, elastico  # noqa: E402  (registra fuentes)
from reportlab.lib.colors import HexColor  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.pdfbase import pdfmetrics  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402

INSTAGRAM = "@oficina.grafica_"
NOCHE = HexColor("#0F2440")      # techo, fondo y huecos entre butacas
PARED = HexColor("#4A7FB0")      # paredes laterales
TELON = HexColor("#1E3D63")      # telón y bambalina
TELON_PLIEGUE = HexColor("#16304F")
BUTACA = HexColor("#22476F")
BUTACA_LUZ = HexColor("#6FA3CF")
PANTALLA = HexColor("#F3EADB")
LETRA = HexColor("#0F2440")
SALA = Tapa("#0F2440", "#F3EADB", "#0F2440", "#0A0A0C", "#0F2440")
CX = PW / 2


def poligono(cv, puntos, color):
    p = cv.beginPath()
    p.moveTo(*puntos[0])
    for pt in puntos[1:]:
        p.lineTo(*pt)
    p.close()
    cv.setFillColor(color)
    cv.drawPath(p, stroke=0, fill=1)


def texto_espaciado(cv, texto, cx, y, fuente, size, espacio, color):
    ancho = sum(pdfmetrics.stringWidth(ch, fuente, size) for ch in texto) + espacio * (len(texto) - 1)
    x = cx - ancho / 2
    cv.setFillColor(color)
    cv.setFont(fuente, size)
    for ch in texto:
        cv.drawString(x, y, ch)
        x += pdfmetrics.stringWidth(ch, fuente, size) + espacio


def sala(cv):
    # paredes laterales en perspectiva
    poligono(cv, [(-5 * mm, 200 * mm), (17 * mm, 178 * mm), (17 * mm, 86 * mm), (-5 * mm, 64 * mm)], PARED)
    poligono(cv, [(PW + 5 * mm, 200 * mm), (PW - 17 * mm, 178 * mm), (PW - 17 * mm, 86 * mm),
                  (PW + 5 * mm, 64 * mm)], PARED)
    # telones a los costados de la pantalla, con pliegues
    for x0 in (19 * mm, PW - 28 * mm):
        cv.setFillColor(TELON)
        cv.rect(x0, 90 * mm, 9 * mm, 82 * mm, stroke=0, fill=1)
        cv.setStrokeColor(TELON_PLIEGUE)
        cv.setLineWidth(0.8)
        for k in range(1, 4):
            cv.line(x0 + k * 2.25 * mm, 90 * mm, x0 + k * 2.25 * mm, 172 * mm)
    # bambalina con ondas
    cv.setFillColor(TELON)
    cv.rect(19 * mm, 166 * mm, PW - 38 * mm, 9 * mm, stroke=0, fill=1)
    n = 13
    paso = (PW - 38 * mm) / n
    for i in range(n):
        cv.circle(19 * mm + paso * (i + 0.5), 166 * mm, paso / 2, stroke=0, fill=1)
    cv.setStrokeColor(TELON_PLIEGUE)
    cv.setLineWidth(0.6)
    for i in range(1, n):
        cv.line(19 * mm + paso * i, 162 * mm, 19 * mm + paso * i, 175 * mm)
    # pantalla
    sx, sy, sw, sh = 30 * mm, 98 * mm, PW - 60 * mm, 60 * mm
    cv.setFillColor(PANTALLA)
    cv.rect(sx, sy, sw, sh, stroke=0, fill=1)
    texto_espaciado(cv, "CHECK LIST", CX, sy + sh - 13 * mm, "PopM", 9.5, 2 * mm, LETRA)
    texto_espaciado(cv, "100", CX, sy + sh / 2 - 8 * mm, "PopM", 42, 2 * mm, LETRA)
    texto_espaciado(cv, "PELÍCULAS", CX, sy + 9 * mm, "PopM", 17, 2 * mm, LETRA)


def butacas(cv):
    filas = 10
    for k in range(filas):
        t = k / (filas - 1)
        base = 89 * mm - (t ** 1.35) * 96 * mm
        h = (4 + t * 15) * mm
        w = (6 + t * 18) * mm
        sep = w * 0.14
        curva = (3 + t * 9) * mm
        x = CX - (w + sep) * 0.5 * (k % 2) - (w + sep) * 12
        while x < PW + w:
            if x + w > -w:
                dy = curva * ((x + w / 2 - CX) / CX) ** 2
                r = w * 0.22
                p = cv.beginPath()
                p.roundRect(x, base + dy, w, h, r)
                cv.setFillColor(BUTACA)
                cv.drawPath(p, stroke=0, fill=1)
                cv.saveState()  # luz de la pantalla sobre el borde superior, recortada a la butaca
                cv.clipPath(p, stroke=0, fill=0)
                luz = max(0.9 * mm, h * 0.13)
                cv.setFillColor(BUTACA_LUZ)
                cv.rect(x, base + dy + h - luz, w, luz, stroke=0, fill=1)
                cv.restoreState()
            x += w + sep


def textura(cv, ancho, alto):
    rnd = random.Random(21)
    for _ in range(2200):
        claro = rnd.random() < 0.5
        cv.setFillColor(HexColor("#FFFFFF" if claro else "#000000"), alpha=0.04 if claro else 0.07)
        s = rnd.uniform(0.15, 0.4) * mm
        cv.rect(rnd.uniform(-3 * mm, ancho), rnd.uniform(-3 * mm, alto), s, s, stroke=0, fill=1)
    cv.setFillColor(HexColor("#000000"), alpha=1)


def contenido(cv, x, y, s=0):
    """Ilustración con origen en el corte (x, y); s = sangrado alrededor."""
    cv.saveState()
    cv.translate(x, y)
    cv.setFillColor(NOCHE)
    cv.rect(-s, -s, PW + 2 * s, PH + 2 * s, stroke=0, fill=1)
    sala(cv)
    butacas(cv)
    textura(cv, PW + 3 * mm, PH + 3 * mm)
    texto_espaciado(cv, INSTAGRAM, CX, PH - 11 * mm, "DMSerif", 9, 0.2 * mm, BUTACA_LUZ)
    cv.restoreState()


def tapa(cv, x, y):
    cuaderno(cv, x, y, SALA)
    cv.saveState()
    p = cv.beginPath()
    p.roundRect(x, y, PW, PH, 3 * mm)
    cv.clipPath(p, stroke=0, fill=0)
    contenido(cv, x, y)
    cv.restoreState()
    elastico(cv, x, y, SALA)


def maqueta():
    m = 16 * mm
    pdf = os.path.join(AQUI, "tapa-sala.pdf")
    cv = canvas.Canvas(pdf, pagesize=(PW + 2 * m, PH + 2 * m))
    cv.setFillColor(HexColor("#F3ECE2"))
    cv.rect(0, 0, PW + 2 * m, PH + 2 * m, stroke=0, fill=1)
    tapa(cv, m, m + 4 * mm)
    cv.showPage()
    cv.save()
    subprocess.run(["pdftoppm", "-r", "150", "-png", "-singlefile", pdf, os.path.join(AQUI, "tapa-sala")],
                   check=True)
    os.remove(pdf)
    print("ok tapa-sala.png")


def imprimir():
    s = 3 * mm
    salida = os.path.join(AQUI, "the-watch-list-tapa-sala.pdf")
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
