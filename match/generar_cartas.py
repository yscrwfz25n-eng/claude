"""Genera el PDF imprimible de MATCH (juego para parejas).

Uso:  python3 match/generar_cartas.py  ->  match/match-cartas.pdf

Mismo formato que Opinólogos: cartas de 63 x 88 mm, 9 por hoja A4, frentes y
dorsos intercalados para imprimir doble faz por el borde largo.
Reutiliza la tipografía y las herramientas de armado de ../generar_pdf.py.
"""
import importlib.util
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, RAIZ)

import generar_pdf as base  # noqa: E402  (fuentes Poppins, armado de hojas, marcas)
from reportlab.lib.colors import HexColor, white  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.pdfbase import pdfmetrics  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402

_spec = importlib.util.spec_from_file_location("contenido_match", os.path.join(AQUI, "contenido.py"))
c = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(c)

SALIDA = os.path.join(AQUI, "match-cartas.pdf")
NOMBRE = "match"
LEMA = "¿cuánto se conocen?"

CW, CH, M = base.CW, base.CH, base.M
TINTA, GRIS, OSCURO = base.TINTA, base.GRIS, base.OSCURO
GRIS_OSCURO = base.GRIS_OSCURO
VERDE, ROJO = base.VERDE, base.ROJO
ROSA = HexColor("#E8265E")   # color de marca
TURQUESA = HexColor("#1FB5A3")

NIVELES = {
    "SUAVE": ("suave", TURQUESA),
    "PICANTE": ("picante", HexColor("#F08A24")),
    "HOT": ("hot +18", ROSA),
}


def logo(cv, x, y, size, color=TINTA, centrado=False):
    """«match» con dos círculos que se cruzan: el match."""
    ancho = pdfmetrics.stringWidth(NOMBRE, "PopB", size)
    r = size * 0.13
    total = ancho + size * 0.12 + r * 3.4
    x0 = x - total / 2 if centrado else x
    cv.setFillColor(color)
    cv.setFont("PopB", size)
    cv.drawString(x0, y, NOMBRE)
    cy = y + size * 0.3
    cx = x0 + ancho + size * 0.12 + r
    cv.setLineWidth(max(0.6, size * 0.045))
    cv.setStrokeColor(TURQUESA)
    cv.circle(cx, cy, r, stroke=1, fill=0)
    cv.setStrokeColor(ROSA)
    cv.circle(cx + r * 1.4, cy, r, stroke=1, fill=0)


def pie(cv, x, y, color=TINTA):
    logo(cv, x + M, y + 5.5 * mm, 6.5, color)


def etiqueta(cv, x, y, izquierda, color, derecha=""):
    cv.setFont("PopM", 6.3)
    cv.setFillColor(color)
    cv.drawString(x + M, y + CH - 10 * mm, izquierda)
    if derecha:
        cv.setFillColor(GRIS)
        cv.drawRightString(x + CW - M, y + CH - 10 * mm, derecha)


def dorso(palabra, color_palabra):
    def dibujar(cv, x, y):
        base.fondo(cv, x, y, OSCURO)
        logo(cv, x + CW / 2, y + CH / 2, 22, white, centrado=True)
        cv.setFillColor(GRIS_OSCURO)
        cv.setFont("PopR", 7)
        cv.drawCentredString(x + CW / 2, y + CH / 2 - 7 * mm, LEMA)
        cv.setFillColor(color_palabra)
        cv.setFont("PopM", 6.8)
        cv.drawCentredString(x + CW / 2, y + 8 * mm, palabra)
    return dibujar


# ---------- frentes ----------

def cara_tema(nivel, numero, texto, lado):
    nombre, color = NIVELES[nivel]

    def dibujar(cv, x, y):
        cv.setFillColor(color)
        cv.rect(x, y + CH - 2.5 * mm, CW, 2.5 * mm, stroke=0, fill=1)
        etiqueta(cv, x, y, nombre, color, f"{numero:02d}{lado}")
        base.parrafo(cv, texto, x + M, y + 22 * mm, CW - 2 * M, CH - 36 * mm, "PopSB", 15.5, 10)
        cv.setFont("PopR", 6.5)
        cv.setFillColor(TINTA)
        cv.drawString(x + M, y + 13 * mm, "a favor")
        cv.drawRightString(x + CW - M, y + 13 * mm, "en contra")
        cv.setStrokeColor(base.LINEA)
        cv.setLineWidth(0.5)
        cv.line(x + 17 * mm, y + 14.1 * mm, x + CW - 20 * mm, y + 14.1 * mm)
        pie(cv, x, y)
    return dibujar


def frente_reto(nivel, texto):
    nombre, color = NIVELES[nivel]

    def dibujar(cv, x, y):
        etiqueta(cv, x, y, "reto · " + nombre, color)
        cv.setFont("PopB", 19)
        cv.setFillColor(TINTA)
        cv.drawString(x + M, y + CH - 21 * mm, "¡reto!")
        cv.setFillColor(color)
        cv.rect(x + M, y + CH - 25 * mm, 8 * mm, 0.9 * mm, stroke=0, fill=1)
        base.parrafo(cv, texto, x + M, y + 16 * mm, CW - 2 * M, CH - 45 * mm, "PopSB", 12, 8,
                     interlineado=1.3)
        cv.setFont("PopR", 5.5)
        cv.setFillColor(GRIS)
        cv.drawString(x + M, y + 11 * mm, "Si no te animás, sacá otro.")
        pie(cv, x, y)
    return dibujar


def cara_voto(tipo, a_favor):
    """Dos tipos por jugador: «mi opinión» (pleno) y «creo que pensás» (contorno)."""
    color = VERDE if a_favor else ROJO
    palabra = "a favor" if a_favor else "en contra"
    simbolo = "✔" if a_favor else "✖"

    def dibujar(cv, x, y):
        if tipo == "opinion":
            base.fondo(cv, x, y, color)
            tinta, titulo = white, "mi opinión"
        else:
            base.fondo(cv, x, y, white)
            cv.setStrokeColor(color)
            cv.setLineWidth(2.5)
            cv.roundRect(x + 3 * mm, y + 3 * mm, CW - 6 * mm, CH - 6 * mm, 3 * mm, stroke=1, fill=0)
            tinta, titulo = color, "creo que pensás"
        cv.setFillColor(tinta)
        cv.setFont("PopM", 8)
        cv.drawString(x + M, y + CH - 13 * mm, titulo)
        size = 28
        while pdfmetrics.stringWidth(palabra, "PopB", size) > CW - 2 * M:
            size -= 1
        cv.setFont("PopB", size)
        cv.drawString(x + M, y + CH - 25 * mm, palabra)
        cv.setFont("Sym", 62)
        cv.drawRightString(x + CW - 5 * mm, y + 9 * mm, simbolo)
        pie(cv, x, y, tinta)
    return dibujar


def frente_ayuda():
    def dibujar(cv, x, y):
        etiqueta(cv, x, y, "ayuda · 1 ronda", GRIS)
        cv.setFont("PopB", 14)
        cv.setFillColor(TINTA)
        cv.drawString(x + M, y + CH - 19 * mm, "cómo se juega")
        html = "<br/>".join(f"<font name='PopSB'>{t}</font> {d}" for t, d in c.AYUDA)
        base.parrafo(cv, html, x + M, y + 11 * mm, CW - 2 * M, CH - 33 * mm, "PopR", 7.5, 5.5,
                     interlineado=1.3)
        pie(cv, x, y)
    return dibujar


# ---------- armado ----------

def main():
    plan = []

    # Tema: doble faz, un tema por cara, las dos caras del mismo nivel.
    fr, ds, numero = [], [], 0
    for nivel, temas in (("SUAVE", c.SUAVE), ("PICANTE", c.PICANTE), ("HOT", c.HOT)):
        mitad = len(temas) // 2
        for i in range(mitad):
            numero += 1
            fr.append(cara_tema(nivel, numero, temas[i], "a"))
            ds.append(cara_tema(nivel, numero, temas[mitad + i], "b"))
    plan += base.hojas(fr, ds)

    # Retos: el dorso dice el nivel, así se separan en tres mazos.
    fr, ds = [], []
    for nivel, retos in c.RETOS.items():
        nombre, color = NIVELES[nivel]
        fr += [frente_reto(nivel, t) for t in retos]
        ds += [dorso("reto · " + nombre, color)] * len(retos)
    plan += base.hojas(fr, ds)

    # Votos (2 por jugador) y ayudas (1 por jugador) en la misma hoja.
    fr = [cara_voto("opinion", True)] * 2 + [cara_voto("adivina", True)] * 2 + [frente_ayuda()] * 2
    ds = [cara_voto("opinion", False)] * 2 + [cara_voto("adivina", False)] * 2 + \
         [dorso("ayuda", GRIS_OSCURO)] * 2
    plan += base.hojas(fr, ds)

    cv = canvas.Canvas(SALIDA, pagesize=A4)
    cv.setTitle("Match – cartas imprimibles")
    cv.setAuthor("@oficina.grafica_")
    total = 0
    for frentes, dorsos in plan:
        for i, dibujar in enumerate(frentes):
            dibujar(cv, *base.posicion(i))
        base.marcas_de_corte(cv)
        cv.showPage()
        for i, dibujar in enumerate(dorsos):
            dibujar(cv, *base.posicion(i, espejo=True))
        base.marcas_de_corte(cv)
        cv.showPage()
        total += len(frentes)
    cv.save()
    print(f"{os.path.relpath(SALIDA, RAIZ)}: {total} cartas en {len(plan) * 2} páginas")


if __name__ == "__main__":
    main()
