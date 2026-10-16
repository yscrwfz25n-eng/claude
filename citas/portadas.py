"""Tres conceptos de portada para THE DATING LIST (más trabajados que la tapa básica).

Uso:  python3 citas/portadas.py  ->  citas/portadas.png
  1 · Grilla de 100: las 100 citas como 100 casillas, algunas ya tildadas.
  2 · Etiqueta: fondo tejido con los nombres de las citas y una etiqueta oval al centro.
  3 · Entrada: la tapa es un ticket «admit two» con talón troquelado.
"""
import os
import random
import subprocess

from maquetas import AUTORIA, BAJADA, NOMBRE, PH, PW, c, casilla  # registra fuentes
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

AQUI = os.path.dirname(os.path.abspath(__file__))
BORDO = HexColor("#5C0F1E")
BORDO_CLARO = HexColor("#74202F")
BEIGE = HexColor("#E6D5B8")
CREMA = HexColor("#F6EEE3")
ROJO = HexColor("#C8102E")
GAP = 12 * mm
CITAS = [t for _, l in c.CATEGORIAS for t in l]


def recortar(cv, x, y):
    p = cv.beginPath()
    p.rect(x, y, PW, PH)
    cv.clipPath(p, stroke=0, fill=0)


def grilla(cv, x, y):
    cv.setFillColor(BORDO)
    cv.rect(x, y, PW, PH, stroke=0, fill=1)
    m = 14 * mm
    cv.setFillColor(BEIGE)
    cv.setFont("PopM", 7.5)
    cv.drawString(x + m, y + PH - 18 * mm, "100 CITAS PARA HACER JUNTOS")
    cv.setFont("DMSerif", 44)
    cv.drawString(x + m - 1 * mm, y + PH - 36 * mm, NOMBRE[0])
    cv.setFont("DMSerifIt", 50)
    cv.drawString(x + m - 1 * mm, y + PH - 54 * mm, NOMBRE[1])
    ancho = pdfmetrics.stringWidth(NOMBRE[1], "DMSerifIt", 50)
    cv.setFillColor(ROJO)
    cv.circle(x + m + ancho + 2 * mm, y + PH - 53.6 * mm, 1.6 * mm, stroke=0, fill=1)
    # 10 x 10 casillas: una por cita; algunas ya tildadas en rojo
    random.seed(7)
    tildadas = set(random.sample(range(100), 14))
    celda = (PW - 2 * m) / 10
    lado = celda * 0.62
    top = y + PH - 66 * mm
    for i in range(100):
        col, fila = i % 10, i // 10
        cx = x + m + col * celda + (celda - lado) / 2
        cy = top - (fila + 1) * celda + (celda - lado) / 2
        casilla(cv, cx, cy, lado, BEIGE, tildada=i in tildadas, acento=ROJO, grosor=0.7)
        if i not in tildadas:
            cv.setFillColor(BEIGE)
            cv.setFont("PopR", 4.2)
            cv.drawCentredString(cx + lado / 2, cy + lado / 2 - 1.4, f"{i + 1}")
    cv.setFillColor(BEIGE)
    cv.setFont("PopSB", 7)
    cv.drawString(x + m, y + 12 * mm, AUTORIA)
    cv.setFont("PopR", 7)
    cv.drawRightString(x + PW - m, y + 12 * mm, "14 de 100")


def etiqueta(cv, x, y):
    cv.saveState()
    recortar(cv, x, y)
    cv.setFillColor(BORDO)
    cv.rect(x, y, PW, PH, stroke=0, fill=1)
    # fondo tejido con las 100 citas, en tono sobre tono
    texto = "  ·  ".join(t.rstrip(".") for t in CITAS)
    cv.setFillColor(BORDO_CLARO)
    cv.setFont("DMSerifIt", 9)
    paso, desplaz = 5.2 * mm, 0
    fila = 0
    yy = y + PH - 4 * mm
    while yy > y - 5 * mm:
        inicio = (fila * 37) % len(texto)
        cv.drawString(x - 2 * mm, yy, (texto[inicio:] + "  ·  " + texto)[:160])
        yy -= paso
        fila += 1
    # etiqueta oval
    cx, cy = x + PW / 2, y + PH / 2 + 4 * mm
    rx, ry = 52 * mm, 72 * mm
    cv.setFillColor(BEIGE)
    cv.ellipse(cx - rx, cy - ry, cx + rx, cy + ry, stroke=0, fill=1)
    cv.setStrokeColor(BORDO)
    cv.setLineWidth(0.6)
    cv.ellipse(cx - rx + 3 * mm, cy - ry + 3 * mm, cx + rx - 3 * mm, cy + ry - 3 * mm, stroke=1, fill=0)
    cv.setLineWidth(0.3)
    cv.ellipse(cx - rx + 4.4 * mm, cy - ry + 4.4 * mm, cx + rx - 4.4 * mm, cy + ry - 4.4 * mm, stroke=1, fill=0)
    cv.setFillColor(ROJO)
    cv.setFont("PopSB", 7.5)
    cv.drawCentredString(cx, cy + 42 * mm, "· 100 CITAS ·")
    casilla(cv, cx - 5 * mm, cy + 24 * mm, 10 * mm, BORDO, True, ROJO, 1.1)
    cv.setFillColor(BORDO)
    cv.setFont("DMSerif", 31)
    cv.drawCentredString(cx, cy + 4 * mm, NOMBRE[0])
    cv.setFont("DMSerifIt", 38)
    cv.drawCentredString(cx, cy - 10 * mm, NOMBRE[1])
    cv.setStrokeColor(ROJO)
    cv.setLineWidth(1)
    cv.line(cx - 7 * mm, cy - 16 * mm, cx + 7 * mm, cy - 16 * mm)
    cv.setFont("PopR", 7.5)
    cv.drawCentredString(cx, cy - 23 * mm, "para hacer juntos")
    cv.setFont("PopSB", 6.5)
    cv.drawCentredString(cx, cy - 52 * mm, AUTORIA)
    cv.restoreState()


def entrada(cv, x, y):
    cv.setFillColor(BORDO)
    cv.rect(x, y, PW, PH, stroke=0, fill=1)
    tw, th = 104 * mm, 166 * mm
    tx, ty = x + (PW - tw) / 2, y + 22 * mm
    talon = ty + 40 * mm  # línea de troquel del talón
    r = 5 * mm
    cv.saveState()
    cv.translate(tx, ty)
    cv.rotate(-3)
    cv.translate(-tx, -ty)
    # sombra
    cv.setFillColor(HexColor("#000000"), alpha=0.25)
    cv.roundRect(tx + 1.5 * mm, ty - 1.5 * mm, tw, th, 3 * mm, stroke=0, fill=1)
    # ticket con muescas semicirculares a la altura del talón
    p = cv.beginPath()
    p.roundRect(tx, ty, tw, th, 3 * mm)
    cv.setFillColor(CREMA)
    cv.drawPath(p, stroke=0, fill=1)
    cv.setFillColor(BORDO)
    cv.circle(tx, talon, r, stroke=0, fill=1)
    cv.circle(tx + tw, talon, r, stroke=0, fill=1)
    cv.setStrokeColor(BORDO)
    cv.setLineWidth(0.6)
    cv.setDash(2, 2)
    cv.line(tx + r + 2 * mm, talon, tx + tw - r - 2 * mm, talon)
    cv.setDash()
    cv.roundRect(tx + 4 * mm, talon + 4 * mm, tw - 8 * mm, th - (talon - ty) - 8 * mm, 2 * mm, stroke=1, fill=0)
    cx = tx + tw / 2
    cv.setFillColor(ROJO)
    cv.setFont("PopSB", 8)
    cv.drawCentredString(cx, ty + th - 18 * mm, "A D M I T   T W O")
    cv.setFillColor(BORDO)
    cv.setFont("PopR", 6.5)
    cv.drawCentredString(cx, ty + th - 24 * mm, "válida para 100 citas")
    cv.setFont("DMSerif", 32)
    cv.drawCentredString(cx, ty + th - 52 * mm, NOMBRE[0])
    cv.setFont("DMSerifIt", 40)
    cv.drawCentredString(cx, ty + th - 67 * mm, NOMBRE[1])
    cv.setStrokeColor(ROJO)
    cv.setLineWidth(1)
    cv.line(cx - 8 * mm, ty + th - 73 * mm, cx + 8 * mm, ty + th - 73 * mm)
    cv.setFont("PopR", 8)
    cv.drawCentredString(cx, ty + th - 81 * mm, BAJADA)
    # fila de 10 casillas, 3 tildadas
    lado, sep = 6 * mm, 2.4 * mm
    x0 = cx - (10 * lado + 9 * sep) / 2
    for i in range(10):
        casilla(cv, x0 + i * (lado + sep), talon + 16 * mm, lado, BORDO, i < 3, ROJO, 0.7)
    # talón: número de serie y código de barras decorativo
    cv.setFillColor(BORDO)
    cv.setFont("PopSB", 7)
    cv.drawString(tx + 9 * mm, ty + 27 * mm, "Nº 001 — 100")
    cv.setFont("PopR", 6.5)
    cv.drawString(tx + 9 * mm, ty + 21 * mm, "FECHA ______________")
    cv.drawString(tx + 9 * mm, ty + 13 * mm, AUTORIA)
    random.seed(3)
    bx = tx + tw - 40 * mm
    while bx < tx + tw - 9 * mm:
        w = random.choice((0.3, 0.6, 0.9, 1.3)) * mm
        cv.rect(bx, ty + 11 * mm, w, 18 * mm, stroke=0, fill=1)
        bx += w + random.choice((0.5, 0.8, 1.2)) * mm
    cv.restoreState()


def main():
    W = 3 * PW + 4 * GAP
    H = PH + 34 * mm
    pdf = os.path.join(AQUI, "portadas.pdf")
    cv = canvas.Canvas(pdf, pagesize=(W, H))
    cv.setFillColor(HexColor("#ECECEC"))
    cv.rect(0, 0, W, H, stroke=0, fill=1)
    cv.setFillColor(HexColor("#111111"))
    cv.setFont("PopB", 22)
    cv.drawString(GAP, H - 14 * mm, "The Dating List · portadas")
    for i, (dibujar, et) in enumerate(((grilla, "1 · Grilla de 100"), (etiqueta, "2 · Etiqueta"),
                                       (entrada, "3 · Entrada"))):
        x = GAP + i * (PW + GAP)
        dibujar(cv, x, 8 * mm)
        cv.setFont("PopM", 10)
        cv.setFillColor(HexColor("#444444"))
        cv.drawString(x, 8 * mm + PH + 3.5 * mm, et)
    cv.showPage()
    cv.save()
    subprocess.run(["pdftoppm", "-r", "90", "-png", "-singlefile", pdf, os.path.join(AQUI, "portadas")], check=True)
    os.remove(pdf)
    print("ok portadas.png")


if __name__ == "__main__":
    main()
