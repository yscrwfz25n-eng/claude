"""Genera el PDF imprimible de MATCH (estilo C · Pasión).

Uso:  python3 match/generar_cartas.py  ->  match/match-cartas.pdf

90 Preguntas + 30 Retos + 1 carta de instrucciones = 121 cartas de 63 x 88 mm,
9 por hoja A4. Cada hoja de frentes va seguida de su hoja de dorsos, espejada
para imprimir doble faz girando por el borde largo.
"""
import importlib.util
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))

import generar_pdf as base  # noqa: E402  (Poppins, grilla, sangrado y marcas)
from maquetas import Pasion, pastilla  # noqa: E402  (registra DM Serif)
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402
from reportlab.platypus import Paragraph  # noqa: E402

_spec = importlib.util.spec_from_file_location("contenido_match", os.path.join(AQUI, "contenido.py"))
c = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(c)

SALIDA = os.path.join(AQUI, "match-cartas.pdf")
CW, CH, M = base.CW, base.CH, base.M
P = Pasion()


OCUPADAS = set()  # (col, fila) con carta en la cara que se está dibujando


def fondo(cv, x, y, color):
    """Fondo pleno con sangrado hacia todo borde que no toca otra carta.

    Como base.fondo, pero en hojas incompletas también sangra hacia los
    huecos vacíos, así un corte corrido no deja un filo blanco.
    """
    col = round((x - base.MX) / CW)
    fila = round((base.PH - base.MY - y) / CH) - 1
    s = base.SANGRADO
    izq = 0 if (col - 1, fila) in OCUPADAS else s
    der = 0 if (col + 1, fila) in OCUPADAS else s
    arr = 0 if (col, fila - 1) in OCUPADAS else s
    aba = 0 if (col, fila + 1) in OCUPADAS else s
    cv.setFillColor(color)
    cv.rect(x - izq, y - aba, CW + izq + der, CH + aba + arr, stroke=0, fill=1)


def cara(cv, cartas, espejo):
    OCUPADAS.clear()
    for i in range(len(cartas)):
        col = i % base.COLS
        OCUPADAS.add((base.COLS - 1 - col if espejo else col, i // base.COLS))
    for i, dibujar in enumerate(cartas):
        dibujar(cv, *base.posicion(i, espejo))
    base.marcas_de_corte(cv)
    cv.showPage()


def marco(cv, x, y):
    cv.setStrokeColor(P.beige)
    cv.setLineWidth(0.5)
    cv.roundRect(x + 3 * mm, y + 3 * mm, CW - 6 * mm, CH - 6 * mm, 2 * mm, stroke=1, fill=0)


def pregunta(texto, quien, hot):
    def dibujar(cv, x, y):
        fondo(cv, x, y, P.negro)
        marco(cv, x, y)
        if quien == "pareja":
            pastilla(cv, x + M, y + CH - 13 * mm, "responde tu pareja", P.beige, P.negro)
        if hot:
            pastilla(cv, x + CW - M - 10 * mm, y + CH - 13 * mm, "+18", P.rojo, P.beige)
        base.parrafo(cv, texto, x + M, y + 15 * mm, CW - 2 * M, CH - 37 * mm, "DMSerif", 17, 10,
                     color=P.beige, vertical="centro", interlineado=1.15)
        P.logo(cv, x + M, y + 7.5 * mm, 9)
    return dibujar


def reto(texto, hot):
    def dibujar(cv, x, y):
        fondo(cv, x, y, P.bordo)
        marco(cv, x, y)
        cv.setFillColor(P.beige)
        cv.setFont("DMSerifIt", 24)
        cv.drawString(x + M, y + CH - 19 * mm, "reto")
        cv.setStrokeColor(P.rojo)
        cv.setLineWidth(1.2)
        cv.line(x + M, y + CH - 21.5 * mm, x + M + 12 * mm, y + CH - 21.5 * mm)
        if hot:
            pastilla(cv, x + CW - M - 10 * mm, y + CH - 13 * mm, "+18", P.rojo, P.beige)
        base.parrafo(cv, texto, x + M, y + 15 * mm, CW - 2 * M, CH - 41 * mm, "DMSerif", 17, 10,
                     color=P.beige, vertical="centro", interlineado=1.15)
        P.logo(cv, x + M, y + 7.5 * mm, 9)
    return dibujar


def instrucciones(cv, x, y):
    fondo(cv, x, y, P.negro)
    marco(cv, x, y)
    cv.setFillColor(P.beige)
    cv.setFont("DMSerifIt", 17)
    cv.drawString(x + M, y + CH - 14 * mm, "cómo jugar")
    cv.setStrokeColor(P.rojo)
    cv.setLineWidth(1)
    cv.line(x + M, y + CH - 16 * mm, x + M + 10 * mm, y + CH - 16 * mm)
    items = [f'<font name="PopSB">{titulo}{"" if titulo[-1] in "?!" else "."}</font> {texto}'
             for titulo, texto in c.INSTRUCCIONES]
    ancho, alto, sep = CW - 2 * M, CH - 31 * mm, 1.4 * mm
    size = 8
    while True:  # la letra más grande con la que entran todos los puntos
        estilo = ParagraphStyle("i", fontName="PopR", fontSize=size, leading=size * 1.25,
                                textColor=P.beige)
        ps = [Paragraph(h, estilo) for h in items]
        altos = [p.wrap(ancho, alto)[1] for p in ps]
        if sum(altos) + sep * (len(ps) - 1) <= alto or size <= 5.5:
            break
        size -= 0.25
    cy = y + CH - 18 * mm
    for p, h in zip(ps, altos):
        cy -= h
        p.drawOn(cv, x + M, cy)
        cy -= sep
    P.logo(cv, x + M, y + 7.5 * mm, 9)


def dorso(nombre, color):
    def dibujar(cv, x, y):
        fondo(cv, x, y, color)
        marco(cv, x, y)
        P.logo(cv, x + CW / 2, y + CH / 2, 30, centrado=True)
        cv.setFillColor(P.rojo)
        cv.circle(x + CW / 2, y + 15 * mm, 0.9 * mm, stroke=0, fill=1)
        cv.setFillColor(P.beige)
        cv.setFont("PopM", 7.5)
        cv.drawCentredString(x + CW / 2, y + 10 * mm, nombre.upper())
    return dibujar


def main():
    fr = [pregunta(t, q, h) for t, q, h in c.PREGUNTAS]
    plan = base.hojas(fr, [dorso("preguntas", P.negro)] * len(fr))

    fr = [reto(t, h) for t, h in c.RETOS] + [instrucciones]
    ds = [dorso("retos", P.bordo)] * len(c.RETOS) + [dorso("cómo jugar", P.negro)]
    plan += base.hojas(fr, ds)

    cv = canvas.Canvas(SALIDA, pagesize=A4)
    cv.setTitle("Match – cartas imprimibles")
    cv.setAuthor("@oficina.grafica_")
    total = 0
    for frentes, dorsos in plan:
        cara(cv, frentes, espejo=False)
        cara(cv, dorsos, espejo=True)
        total += len(frentes)
    cv.save()
    print(f"{os.path.relpath(SALIDA)}: {total} cartas en {len(plan) * 2} páginas")


if __name__ == "__main__":
    main()
