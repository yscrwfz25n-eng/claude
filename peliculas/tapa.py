"""Tapa de THE WATCH LIST: dos personas en una sala de cine; en la pantalla, «100 películas».

Uso:  python3 peliculas/tapa.py  ->  peliculas/tapa.png (maqueta del cuaderno con elástico y cinta)

Ilustración vectorial propia, estilo retro plano con textura de impresión.
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
NEGRO = HexColor("#15120F")
ROJO = HexColor("#B9483E")
ROJO_OSC = HexColor("#8E3029")
CREMA = HexColor("#F1E4C3")
TINTA = HexColor("#2B2520")
SALVIA = HexColor("#8DA38A")
PIEL = HexColor("#E9B49A")
SALA = Tapa("#15120F", "#F1E4C3", "#15120F", "#0B0A09", "#15120F")


def cortina(cv, x0, ancho, abajo, espejo):
    """Cortina roja recogida hacia el costado, con pliegues."""
    cv.saveState()
    if espejo:
        cv.translate(PW, 0)
        cv.scale(-1, 1)
    p = cv.beginPath()
    p.moveTo(0, PH)
    p.lineTo(ancho, PH)
    p.curveTo(ancho * 0.75, PH - 30 * mm, ancho * 0.25, abajo + 25 * mm, 0, abajo)
    p.close()
    cv.setFillColor(ROJO)
    cv.drawPath(p, stroke=0, fill=1)
    cv.saveState()
    cv.clipPath(p, stroke=0, fill=0)
    cv.setStrokeColor(ROJO_OSC)
    cv.setLineCap(1)
    for k in range(4):  # pliegues
        f = 0.18 + k * 0.2
        cv.setLineWidth(2.2 - k * 0.3)
        q = cv.beginPath()
        q.moveTo(ancho * f, PH)
        q.curveTo(ancho * f * 0.8, PH - 40 * mm, ancho * f * 0.3, abajo + 40 * mm, 0, abajo + 8 * mm * k)
        cv.drawPath(q, stroke=1, fill=0)
    cv.restoreState()
    cv.restoreState()


def ornamento(cv, x, y, sx, sy):
    """Rulo de esquina para el marco de la pantalla."""
    cv.saveState()
    cv.translate(x, y)
    cv.scale(sx, sy)
    cv.setStrokeColor(TINTA)
    cv.setLineWidth(0.7)
    p = cv.beginPath()
    p.moveTo(0, 7 * mm)
    p.curveTo(0, 2 * mm, 2 * mm, 0, 7 * mm, 0)
    cv.drawPath(p, stroke=1, fill=0)
    cv.circle(3.6 * mm, 3.6 * mm, 1.4 * mm, stroke=1, fill=0)
    cv.setFillColor(TINTA)
    cv.circle(3.6 * mm, 3.6 * mm, 0.45 * mm, stroke=0, fill=1)
    cv.circle(8.5 * mm, 0, 0.5 * mm, stroke=0, fill=1)
    cv.circle(0, 8.5 * mm, 0.5 * mm, stroke=0, fill=1)
    cv.restoreState()


def pantalla(cv, x1, y1, w, h):
    cv.setFillColor(CREMA)
    cv.rect(x1, y1, w, h, stroke=0, fill=1)
    # manchas y rayas suaves de proyección vieja
    rnd = random.Random(5)
    for _ in range(60):
        cv.setFillColor(HexColor("#C9B98F"), alpha=rnd.uniform(0.05, 0.16))
        cv.rect(x1 + rnd.uniform(0, w), y1 + rnd.uniform(0, h), rnd.uniform(0.2, 0.6) * mm,
                rnd.uniform(3, 14) * mm, stroke=0, fill=1)
    cv.setFillColor(HexColor("#000000"), alpha=1)
    m = 3.5 * mm
    cv.setStrokeColor(TINTA)
    cv.setLineWidth(0.9)
    cv.rect(x1 + m, y1 + m, w - 2 * m, h - 2 * m, stroke=1, fill=0)
    cv.setLineWidth(0.4)
    cv.rect(x1 + m + 1.3 * mm, y1 + m + 1.3 * mm, w - 2 * m - 2.6 * mm, h - 2 * m - 2.6 * mm, stroke=1, fill=0)
    d = m + 2.5 * mm
    ornamento(cv, x1 + d, y1 + d, 1, 1)
    ornamento(cv, x1 + w - d, y1 + d, -1, 1)
    ornamento(cv, x1 + d, y1 + h - d, 1, -1)
    ornamento(cv, x1 + w - d, y1 + h - d, -1, -1)
    # «100 películas», escalonado como un cartel de final de película
    cx, cy = x1 + w / 2, y1 + h / 2
    for dx, dy, color in ((0.7, -0.7, HexColor("#B7A47C")), (0, 0, TINTA)):
        cv.setFillColor(color)
        cv.setFont("Script", 64)
        cv.drawCentredString(cx - 14 * mm + dx * mm, cy + 1 * mm + dy * mm, "100")
        cv.setFont("Script", 44)
        cv.drawCentredString(cx + 12 * mm + dx * mm, cy - 13 * mm + dy * mm, "películas")


def butaca(cv, cx, base, w, h):
    cv.setFillColor(NEGRO)
    cv.setStrokeColor(ROJO)
    cv.setLineWidth(1.3)
    cv.roundRect(cx - w / 2, base, w, h, w * 0.18, stroke=1, fill=1)
    cv.setStrokeColor(HexColor("#2A211D"))
    cv.setLineWidth(0.6)
    cv.line(cx - w / 2 + 2 * mm, base + h - 3 * mm, cx + w / 2 - 2 * mm, base + h - 3 * mm)


def fila(cv, base, w, h, paso, desfase):
    x = -w / 2 + desfase
    while x < PW + w:
        butaca(cv, x, base, w, h)
        x += paso


def persona(cv, cx, base, pelo, remera, inclinacion, largo):
    """Persona de espaldas, sentada; la cabeza se inclina hacia la otra."""
    cv.saveState()
    cv.translate(cx, base)
    # torso y hombros
    p = cv.beginPath()
    p.moveTo(-12 * mm, 0)
    p.curveTo(-12.5 * mm, 12 * mm, -10 * mm, 17 * mm, -4 * mm, 18 * mm)
    p.lineTo(4 * mm, 18 * mm)
    p.curveTo(10 * mm, 17 * mm, 12.5 * mm, 12 * mm, 12 * mm, 0)
    p.close()
    cv.setFillColor(remera)
    cv.drawPath(p, stroke=0, fill=1)
    # cuello
    cv.setFillColor(PIEL)
    cv.rect(-2.2 * mm, 16 * mm, 4.4 * mm, 4.5 * mm, stroke=0, fill=1)
    # cabeza inclinada
    cv.translate(0, 21 * mm)
    cv.rotate(inclinacion)
    cv.setFillColor(PIEL)
    cv.circle(-6.2 * mm if inclinacion < 0 else 6.2 * mm, 3.2 * mm, 1.4 * mm, stroke=0, fill=1)  # oreja
    cv.setFillColor(pelo)
    cv.ellipse(-6 * mm, -1 * mm, 6 * mm, 12.5 * mm, stroke=0, fill=1)
    if largo:  # pelo largo que cae sobre los hombros
        q = cv.beginPath()
        q.moveTo(-6 * mm, 5 * mm)
        q.curveTo(-7.5 * mm, -2 * mm, -6.5 * mm, -6 * mm, -4 * mm, -7 * mm)
        q.lineTo(4 * mm, -7 * mm)
        q.curveTo(6.5 * mm, -6 * mm, 7.5 * mm, -2 * mm, 6 * mm, 5 * mm)
        q.close()
        cv.drawPath(q, stroke=0, fill=1)
    cv.restoreState()


def pochoclos(cv, cx, base):
    w1, w2, h = 7 * mm, 9.5 * mm, 9 * mm
    for dx, dy in ((-3, 0.5), (0, 1.6), (3, 0.6), (-1.5, -0.4), (1.6, -0.3)):
        cv.setFillColor(CREMA)
        cv.circle(cx + dx * mm, base + h + dy * mm, 2 * mm, stroke=0, fill=1)
    p = cv.beginPath()
    p.moveTo(cx - w1 / 2, base)
    p.lineTo(cx + w1 / 2, base)
    p.lineTo(cx + w2 / 2, base + h)
    p.lineTo(cx - w2 / 2, base + h)
    p.close()
    cv.saveState()
    cv.clipPath(p, stroke=0, fill=0)
    for i in range(5):
        cv.setFillColor(ROJO if i % 2 == 0 else CREMA)
        cv.rect(cx - w2 / 2 + i * w2 / 5, base, w2 / 5 + 0.1, h, stroke=0, fill=1)
    cv.restoreState()


def textura(cv, x, y):
    """Grano de impresión: puntitos claros y oscuros muy suaves."""
    rnd = random.Random(11)
    for _ in range(2600):
        claro = rnd.random() < 0.5
        cv.setFillColor(HexColor("#FFFFFF" if claro else "#000000"), alpha=0.05 if claro else 0.08)
        s = rnd.uniform(0.15, 0.45) * mm
        cv.rect(x + rnd.uniform(0, PW), y + rnd.uniform(0, PH), s, s, stroke=0, fill=1)
    cv.setFillColor(HexColor("#000000"), alpha=1)


def tapa(cv, x, y, t=SALA):
    cuaderno(cv, x, y, t)
    cv.saveState()
    p = cv.beginPath()
    p.roundRect(x, y, PW, PH, 3 * mm)
    cv.clipPath(p, stroke=0, fill=0)
    cv.translate(x, y)
    pantalla(cv, 17 * mm, 128 * mm, 106 * mm, 58 * mm)
    cortina(cv, 0, 30 * mm, 112 * mm, espejo=False)
    cortina(cv, 0, 30 * mm, 112 * mm, espejo=True)
    # bambalina con el nombre de la colección
    cv.setFillColor(ROJO)
    cv.rect(0, PH - 13 * mm, PW, 13 * mm, stroke=0, fill=1)
    for i in range(12):
        cv.circle(i * 13 * mm + 6.5 * mm, PH - 13 * mm, 6.5 * mm, stroke=0, fill=1)
    cv.setFillColor(CREMA)
    cv.setFont("DMSerif", 9)
    cv.drawCentredString(68 * mm, PH - 9 * mm, "T H E   W A T C H   L I S T")
    # escenario y filas de butacas, de atrás hacia adelante
    cv.setFillColor(SALVIA)
    cv.rect(0, 116 * mm, PW, 7 * mm, stroke=0, fill=1)
    fila(cv, 104 * mm, 19 * mm, 15 * mm, 21.5 * mm, 4 * mm)
    fila(cv, 85 * mm, 24 * mm, 20 * mm, 27 * mm, 14 * mm)
    fila(cv, 60 * mm, 30 * mm, 27 * mm, 33.5 * mm, 2 * mm)
    persona(cv, 58.5 * mm, 58 * mm, HexColor("#3B2A22"), SALVIA, -19, largo=False)
    persona(cv, 80.5 * mm, 58 * mm, HexColor("#7A3B24"), HexColor("#D9B65E"), 18, largo=True)
    pochoclos(cv, 69.5 * mm, 66 * mm)
    fila(cv, 28 * mm, 38 * mm, 36 * mm, 42 * mm, 22 * mm)
    fila(cv, -8 * mm, 46 * mm, 38 * mm, 51 * mm, -6 * mm)
    textura(cv, 0, 0)
    cv.setFillColor(CREMA)
    cv.setFont("DMSerif", 8.5)
    cv.drawCentredString(68 * mm, 6 * mm, INSTAGRAM)
    cv.restoreState()
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
