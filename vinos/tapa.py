"""Tapa del ÁLBUM DE VINOS: papel crema con manchas de copa de vino tinto.

Uso:  python3 vinos/tapa.py
  -> vinos/tapa.png                     maqueta del cuaderno con elástico y cinta
  -> vinos/album-de-vinos-tapa.pdf      arte A5 con 3 mm de sangrado, para imprenta

Las manchas son anillos irregulares con el borde más oscuro, como queda el vino
cuando se seca alrededor de la base de la copa.
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
from reportlab.pdfbase import pdfmetrics  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402

INSTAGRAM = "@oficina.grafica_"
CREMA = HexColor("#F3EADB")
VINO = HexColor("#6E1630")
MANCHA = HexColor("#8A2140")
VINOS = Tapa("#F3EADB", "#6E1630", "#E6DAC6", "#6E1630", "#6E1630")
CX = PW / 2 - 3 * mm  # centro óptico: el elástico ocupa el borde derecho


def ruido(rnd, armonicos=9):
    """Función periódica suave de 0..2π: suma de senos con fase al azar."""
    coef = [(k, rnd.uniform(0, 1) / k, rnd.uniform(0, 2 * math.pi)) for k in range(2, 2 + armonicos)]
    return lambda t: sum(a * math.sin(k * t + f) for k, a, f in coef)


def anillo(cv, cx, cy, r, ancho, semilla, opacidad=1.0, desde=0.0, hasta=2 * math.pi):
    """Mancha de copa: anillo de ancho variable, relleno translúcido y borde exterior marcado."""
    rnd = random.Random(semilla)
    n_ext, n_int, n_borde = ruido(rnd), ruido(rnd), ruido(rnd)
    pasos = 240
    ts = [desde + (hasta - desde) * i / pasos for i in range(pasos + 1)]
    abierto = hasta - desde < 2 * math.pi - 1e-6

    def punta(i):  # en un anillo cortado, el ancho se afina hacia las puntas
        if not abierto:
            return 1.0
        u = i / pasos
        return min(1.0, u / 0.12, (1 - u) / 0.12)

    radio = [r + 1.5 * mm * n_ext(t) for t in ts]
    ext = [(cx + rr * math.cos(t), cy + rr * math.sin(t)) for t, rr in zip(ts, radio)]
    anchos = [max(0.3 * mm, ancho * (0.75 + 0.6 * n_int(t))) * punta(i) for i, t in enumerate(ts)]
    inn = [(cx + (rr - w) * math.cos(t), cy + (rr - w) * math.sin(t)) for t, rr, w in zip(ts, radio, anchos)]
    if not abierto:  # lavado muy suave dentro del anillo
        q = cv.beginPath()
        q.moveTo(*inn[0])
        for pt in inn[1:]:
            q.lineTo(*pt)
        q.close()
        cv.setFillColor(MANCHA, alpha=0.035 * opacidad)
        cv.drawPath(q, stroke=0, fill=1)
    p = cv.beginPath()
    p.moveTo(*ext[0])
    for pt in ext[1:]:
        p.lineTo(*pt)
    for pt in reversed(inn):
        p.lineTo(*pt)
    p.close()
    cv.setFillColor(MANCHA, alpha=0.22 * opacidad)
    cv.drawPath(p, stroke=0, fill=1)
    # borde exterior más oscuro, con grosor que va y viene
    for i in range(pasos):
        g = (0.2 * mm + 0.45 * mm * max(0.0, 0.5 + 0.6 * n_borde(ts[i])) ) * punta(i)
        cv.setStrokeColor(MANCHA, alpha=0.55 * opacidad)
        cv.setLineWidth(g)
        cv.line(*ext[i], *ext[i + 1])


def gotas(cv, semilla):
    rnd = random.Random(semilla)
    for cx, cy, r in ((CX + 44 * mm, 150 * mm, 1.6 * mm), (CX + 48 * mm, 146 * mm, 0.7 * mm),
                      (CX - 50 * mm, 74 * mm, 1.1 * mm), (CX - 46 * mm, 70 * mm, 0.5 * mm)):
        p = cv.beginPath()
        for i in range(37):
            t = 2 * math.pi * i / 36
            rr = r * (1 + 0.12 * math.sin(3 * t + rnd.uniform(0, 1)))
            (p.moveTo if i == 0 else p.lineTo)(cx + rr * math.cos(t), cy + rr * math.sin(t))
        p.close()
        cv.setFillColor(MANCHA, alpha=0.45)
        cv.drawPath(p, stroke=0, fill=1)


def estrella(cv, cx, cy, r, llena):
    p = cv.beginPath()
    for i in range(10):
        a = math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        (p.moveTo if i == 0 else p.lineTo)(cx + rr * math.cos(a), cy + rr * math.sin(a))
    p.close()
    cv.setStrokeColor(VINO)
    cv.setFillColor(VINO)
    cv.setLineWidth(0.7)
    cv.setLineJoin(1)
    cv.drawPath(p, stroke=1, fill=1 if llena else 0)


def espaciado(cv, texto, cx, y, fuente, size, espacio, color):
    ancho = sum(pdfmetrics.stringWidth(ch, fuente, size) for ch in texto) + espacio * (len(texto) - 1)
    x = cx - ancho / 2
    cv.setFillColor(color)
    cv.setFont(fuente, size)
    for ch in texto:
        cv.drawString(x, y, ch)
        x += pdfmetrics.stringWidth(ch, fuente, size) + espacio


def textura(cv):
    rnd = random.Random(17)
    for _ in range(1800):
        claro = rnd.random() < 0.5
        cv.setFillColor(HexColor("#FFFFFF" if claro else "#5A3A2A"), alpha=0.05 if claro else 0.05)
        s = rnd.uniform(0.15, 0.4) * mm
        cv.rect(rnd.uniform(-3 * mm, PW + 3 * mm), rnd.uniform(-3 * mm, PH + 3 * mm), s, s, stroke=0, fill=1)
    cv.setFillColor(HexColor("#000000"), alpha=1)


def contenido(cv, x, y, s=0):
    cv.saveState()
    cv.translate(x, y)
    cv.setFillColor(CREMA)
    cv.rect(-s, -s, PW + 2 * s, PH + 2 * s, stroke=0, fill=1)
    cy = 112 * mm
    # la copa se apoyó dos veces: un anillo entero y otro corrido, más tenue y cortado
    anillo(cv, CX + 13 * mm, cy - 9 * mm, 45 * mm, 2.6 * mm, 5, opacidad=0.55, desde=-0.4, hasta=4.3)
    anillo(cv, CX, cy, 47 * mm, 3.2 * mm, 2)
    gotas(cv, 9)
    # título dentro del anillo
    cv.setFillColor(VINO)
    cv.setFont("Script", 34)
    cv.drawCentredString(CX, cy + 13 * mm, "álbum de")
    espaciado(cv, "VINOS", CX, cy - 10 * mm, "DMSerif", 56, 1.4 * mm, VINO)
    for i in range(5):
        estrella(cv, CX + (i - 2) * 7 * mm, cy - 21 * mm, 2.4 * mm, i < 4)
    # pie: qué se anota en cada página
    espaciado(cv, "FECHA · CEPA · BODEGA · PUNTAJE", CX, 30 * mm, "PopM", 7.5, 0.55 * mm, VINO)
    cv.setFont("DMSerifIt", 11)
    cv.drawCentredString(CX, 21 * mm, "para cada botella que valga la pena")
    espaciado(cv, INSTAGRAM, CX, PH - 12 * mm, "DMSerif", 9, 0.2 * mm, VINO)
    textura(cv)
    cv.restoreState()


def tapa(cv, x, y):
    cuaderno(cv, x, y, VINOS)
    cv.saveState()
    p = cv.beginPath()
    p.roundRect(x, y, PW, PH, 3 * mm)
    cv.clipPath(p, stroke=0, fill=0)
    contenido(cv, x, y)
    cv.restoreState()
    elastico(cv, x, y, VINOS)


def maqueta():
    m = 16 * mm
    pdf = os.path.join(AQUI, "tapa.pdf")
    cv = canvas.Canvas(pdf, pagesize=(PW + 2 * m, PH + 2 * m))
    cv.setFillColor(HexColor("#E9E1D3"))
    cv.rect(0, 0, PW + 2 * m, PH + 2 * m, stroke=0, fill=1)
    tapa(cv, m, m + 4 * mm)
    cv.showPage()
    cv.save()
    subprocess.run(["pdftoppm", "-r", "150", "-png", "-singlefile", pdf, os.path.join(AQUI, "tapa")], check=True)
    os.remove(pdf)
    print("ok tapa.png")


def imprimir():
    s = 3 * mm
    salida = os.path.join(AQUI, "album-de-vinos-tapa.pdf")
    cv = canvas.Canvas(salida, pagesize=(PW + 2 * s, PH + 2 * s))
    cv.setTitle("Álbum de vinos – tapa")
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
