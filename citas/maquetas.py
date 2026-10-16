"""Maquetas de estilo para THE DATING LIST: tres propuestas sobre las mismas 3 páginas A5.

Uso:  python3 citas/maquetas.py  ->  citas/estilo-a-crema.png, estilo-b-rosa.png, estilo-c-noche.png

Cada lámina muestra la tapa, la primera página de la lista (checklist) y una
página interior con dos citas para completar.
"""
import importlib.util
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, RAIZ)

import generar_pdf as base  # noqa: E402  (registra Poppins y Sym)
from reportlab.lib.colors import HexColor  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.pdfbase import pdfmetrics  # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402

F = os.path.join(RAIZ, "fuentes")
pdfmetrics.registerFont(TTFont("DMSerif", os.path.join(F, "DMSerifDisplay-Regular.ttf")))
pdfmetrics.registerFont(TTFont("DMSerifIt", os.path.join(F, "DMSerifDisplay-Italic.ttf")))

_spec = importlib.util.spec_from_file_location("contenido_citas", os.path.join(AQUI, "contenido.py"))
c = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(c)

NOMBRE = ("The Dating", "List")
BAJADA = "100 citas para hacer juntos"
AUTORIA = "de @oficina.grafica_"
PW, PH = 148 * mm, 210 * mm  # A5
GAP = 12 * mm
MG = 14 * mm  # margen de las páginas interiores


class Estilo:
    def __init__(self, nombre, bajada, papel, tinta, acento, linea, tapa, tapa_tinta, tapa_acento):
        self.nombre, self.bajada = nombre, bajada
        self.papel, self.tinta, self.acento, self.linea = map(HexColor, (papel, tinta, acento, linea))
        self.tapa, self.tapa_tinta, self.tapa_acento = map(HexColor, (tapa, tapa_tinta, tapa_acento))


ESTILOS = [
    ("estilo-a-crema", Estilo("A · Crema", "Tapa bordó y papel crema con rojo. Combina con Match en un combo, sin ser igual.",
                              "#F6EEE3", "#5C0F1E", "#C8102E", "#D9C7B0", "#5C0F1E", "#E6D5B8", "#C8102E")),
    ("estilo-b-rosa", Estilo("B · Rosa", "Rosa empolvado con bordó y terracota. Más romántico, ideal para regalar.",
                             "#FBF4F1", "#4A1A22", "#C9776E", "#E5CFC8", "#E9C9C1", "#5C0F1E", "#C9776E")),
    ("estilo-c-noche", Estilo("C · Noche", "Tapa azul noche con beige y rojo; interior blanco papel. Sobrio y elegante.",
                              "#FAF7F2", "#1C1F2E", "#C8102E", "#D8D4CC", "#1C1F2E", "#E6D5B8", "#C8102E")),
]


def casilla(cv, x, y, lado, color, tildada=False, acento=None, grosor=0.8):
    cv.setStrokeColor(color)
    cv.setLineWidth(grosor)
    cv.roundRect(x, y, lado, lado, lado * 0.18, stroke=1, fill=0)
    if tildada:
        cv.setStrokeColor(acento or color)
        cv.setLineWidth(grosor * 1.8)
        cv.setLineCap(1)
        p = cv.beginPath()
        p.moveTo(x + lado * 0.2, y + lado * 0.52)
        p.lineTo(x + lado * 0.42, y + lado * 0.28)
        p.lineTo(x + lado * 0.95, y + lado * 0.95)
        cv.drawPath(p, stroke=1, fill=0)
        cv.setLineCap(0)


def tapa(cv, x, y, e):
    cv.setFillColor(e.tapa)
    cv.rect(x, y, PW, PH, stroke=0, fill=1)
    cv.setStrokeColor(e.tapa_tinta)
    cv.setLineWidth(0.6)
    cv.rect(x + 8 * mm, y + 8 * mm, PW - 16 * mm, PH - 16 * mm, stroke=1, fill=0)
    cx = x + PW / 2
    cv.setFillColor(e.tapa_tinta)
    cv.setFont("PopM", 8)
    cv.drawCentredString(cx, y + PH - 30 * mm, "· 100 ·")
    casilla(cv, cx - 7 * mm, y + PH / 2 + 30 * mm, 14 * mm, e.tapa_tinta, True, e.tapa_acento, 1.4)
    cv.setFont("DMSerif", 40)
    cv.drawCentredString(cx, y + PH / 2 + 2 * mm, NOMBRE[0])
    cv.setFont("DMSerifIt", 46)
    cv.drawCentredString(cx, y + PH / 2 - 15 * mm, NOMBRE[1])
    cv.setStrokeColor(e.tapa_acento)
    cv.setLineWidth(1.2)
    cv.line(cx - 8 * mm, y + PH / 2 - 23 * mm, cx + 8 * mm, y + PH / 2 - 23 * mm)
    cv.setFont("PopR", 9)
    cv.drawCentredString(cx, y + PH / 2 - 31 * mm, BAJADA)
    cv.setFont("PopSB", 7.5)
    cv.drawCentredString(cx, y + 16 * mm, AUTORIA)


def fondo_papel(cv, x, y, e):
    cv.setFillColor(e.papel)
    cv.rect(x, y, PW, PH, stroke=0, fill=1)


def folio(cv, x, y, e, n):
    cv.setFillColor(e.acento)
    cv.setFont("PopM", 7)
    cv.drawCentredString(x + PW / 2, y + 8 * mm, str(n))


def lista(cv, x, y, e):
    fondo_papel(cv, x, y, e)
    cv.setFillColor(e.tinta)
    cv.setFont("DMSerifIt", 26)
    cv.drawString(x + MG, y + PH - 26 * mm, "la lista")
    cv.setStrokeColor(e.acento)
    cv.setLineWidth(1)
    cv.line(x + MG, y + PH - 29 * mm, x + MG + 10 * mm, y + PH - 29 * mm)
    cv.setFont("PopR", 7.5)
    cv.drawString(x + MG, y + PH - 35 * mm, "Tilden cada cita cuando la hagan.")
    cy = y + PH - 45 * mm
    n = 0
    for categoria, citas in c.CATEGORIAS:
        if cy < y + 20 * mm:
            break
        cv.setFillColor(e.acento)
        cv.setFont("PopSB", 7)
        cv.drawString(x + MG, cy, categoria.upper())
        cy -= 6 * mm
        for cita in citas:
            n += 1
            if cy < y + 18 * mm:
                break
            casilla(cv, x + MG, cy - 0.6 * mm, 3.4 * mm, e.tinta, tildada=n in (1, 4, 7), acento=e.acento,
                    grosor=0.6)
            cv.setFillColor(e.acento)
            cv.setFont("PopM", 6.5)
            cv.drawRightString(x + MG + 11 * mm, cy, f"{n:02d}")
            cv.setFillColor(e.tinta)
            cv.setFont("PopR", 7.5)
            cv.drawString(x + MG + 13 * mm, cy, cita)
            cy -= 5.6 * mm
        cy -= 2 * mm
    folio(cv, x, y, e, 3)


def campo(cv, x, y, ancho, etiqueta, e, renglones=1):
    cv.setFillColor(e.acento)
    cv.setFont("PopSB", 6.3)
    cv.drawString(x, y + 1.2 * mm, etiqueta.upper())
    cv.setStrokeColor(e.linea)
    cv.setLineWidth(0.5)
    w = pdfmetrics.stringWidth(etiqueta.upper(), "PopSB", 6.3) + 2 * mm
    cv.line(x + w, y, x + ancho, y)
    for i in range(1, renglones):
        cv.line(x, y - i * 7 * mm, x + ancho, y - i * 7 * mm)


def bloque_cita(cv, x, top, ancho, e, numero, texto, completa=False):
    casilla(cv, x, top - 7 * mm, 6 * mm, e.tinta, tildada=completa, acento=e.acento, grosor=0.9)
    cv.setFillColor(e.acento)
    cv.setFont("PopSB", 7)
    cv.drawString(x + 9 * mm, top - 2.5 * mm, f"CITA Nº {numero:02d}")
    base.parrafo(cv, texto, x + 9 * mm, top - 17 * mm, ancho - 9 * mm, 13 * mm, "DMSerif", 15, 11,
                 color=e.tinta, interlineado=1.1)
    fila = top - 26 * mm
    mitad = ancho / 2
    campo(cv, x, fila, mitad - 4 * mm, "Fecha", e)
    campo(cv, x + mitad + 2 * mm, fila, mitad - 2 * mm, "Lugar", e)
    fila -= 9 * mm
    campo(cv, x, fila, mitad - 4 * mm, "La organizó", e)
    cv.setFillColor(e.acento)
    cv.setFont("PopSB", 6.3)
    cv.drawString(x + mitad + 2 * mm, fila + 1.2 * mm, "PUNTAJE")
    cv.setFillColor(e.tinta)
    cv.setFont("Sym", 10)
    cv.drawString(x + mitad + 16 * mm, fila + 0.6 * mm, "♡ ♡ ♡ ♡ ♡")
    fila -= 9 * mm
    campo(cv, x, fila, ancho, "Lo mejor", e, renglones=2)
    fila -= 16 * mm
    campo(cv, x, fila, ancho, "Una anécdota", e, renglones=3)
    fila -= 23 * mm
    cv.setFillColor(e.acento)
    cv.setFont("PopSB", 6.3)
    cv.drawString(x, fila + 1.2 * mm, "¿LA REPETIRÍAN?")
    cv.setFillColor(e.tinta)
    cv.setFont("PopR", 7.5)
    for i, op in enumerate(("sí", "no")):
        ox = x + 26 * mm + i * 14 * mm
        cv.setStrokeColor(e.tinta)
        cv.setLineWidth(0.6)
        cv.circle(ox, fila + 2 * mm, 1.5 * mm, stroke=1, fill=0)
        cv.drawString(ox + 2.8 * mm, fila + 1 * mm, op)


def interior(cv, x, y, e):
    fondo_papel(cv, x, y, e)
    ancho = PW - 2 * MG
    citas = [t for _, l in c.CATEGORIAS for t in l]
    bloque_cita(cv, x + MG, y + PH - MG, ancho, e, 1, citas[0])
    cv.setStrokeColor(e.acento)
    cv.setLineWidth(0.5)
    cv.setDash(1, 2)
    cv.line(x + MG, y + PH / 2 + 2 * mm, x + PW - MG, y + PH / 2 + 2 * mm)
    cv.setDash()
    bloque_cita(cv, x + MG, y + PH / 2 - 4 * mm, ancho, e, 2, citas[1])
    folio(cv, x, y, e, 7)


def lamina(e, salida_pdf):
    W = 3 * PW + 4 * GAP
    H = PH + 48 * mm
    cv = canvas.Canvas(salida_pdf, pagesize=(W, H))
    cv.setFillColor(HexColor("#ECECEC"))
    cv.rect(0, 0, W, H, stroke=0, fill=1)
    cv.setFillColor(HexColor("#111111"))
    cv.setFont("PopB", 22)
    cv.drawString(GAP, H - 15 * mm, e.nombre)
    cv.setFont("PopR", 11)
    cv.setFillColor(HexColor("#444444"))
    cv.drawString(GAP, H - 23 * mm, e.bajada)
    y = 8 * mm
    for i, (pagina, et) in enumerate(((tapa, "Tapa"), (lista, "La lista (checklist)"), (interior, "Interior: 2 citas por página"))):
        x = GAP + i * (PW + GAP)
        pagina(cv, x, y, e)
        cv.setFont("PopM", 9)
        cv.setFillColor(HexColor("#666666"))
        cv.drawString(x, y + PH + 3 * mm, et)
    cv.showPage()
    cv.save()


if __name__ == "__main__":
    for archivo, e in ESTILOS:
        pdf = os.path.join(AQUI, archivo + ".pdf")
        lamina(e, pdf)
        subprocess.run(["pdftoppm", "-r", "90", "-png", "-singlefile", pdf, os.path.join(AQUI, archivo)], check=True)
        os.remove(pdf)
        print("ok", archivo + ".png")
