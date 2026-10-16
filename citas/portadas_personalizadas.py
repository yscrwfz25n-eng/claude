"""Portadas personalizadas de THE DATING LIST: cuaderno A5 de tapa dura con elástico y cinta.

Uso:  python3 citas/portadas_personalizadas.py  ->  citas/portadas-personalizadas.png

Logotipo: «THE» y «LIST» en serif alta y angosta, cruzadas por «Dating» en
letra manuscrita. Los datos de cada pareja se cambian en PAREJA. En imprenta,
el beige de la tapa se puede reemplazar por foil dorado (hot stamping).
"""
import os
import subprocess

from maquetas import PH, PW  # registra DM Serif y Poppins
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

AQUI = os.path.dirname(os.path.abspath(__file__))
pdfmetrics.registerFont(TTFont("Script", os.path.join(os.path.dirname(AQUI), "fuentes", "GreatVibes-Regular.ttf")))

PAREJA = {"nombres": ("Cami", "Juli"), "iniciales": ("C", "J"), "desde": "14 · 02 · 2023"}

GAP = 14 * mm
ANGOSTA = 68  # % de ancho para la serif alta


class Tapa:
    def __init__(self, fondo, tinta, sombra, elastico):
        self.fondo, self.tinta, self.sombra, self.elastico = map(HexColor, (fondo, tinta, sombra, elastico))


BORDO = Tapa("#5C0F1E", "#EFE3D0", "#68192A", "#151515")
CREMA = Tapa("#EFE3D0", "#5C0F1E", "#E5D6BF", "#5C0F1E")


def serif_alta(cv, texto, cx, y, size, color):
    cv.saveState()  # la escala horizontal queda en el estado gráfico: se aísla
    t = cv.beginText()
    t.setFont("DMSerif", size)
    t.setHorizScale(ANGOSTA)
    t.setFillColor(color)
    ancho = pdfmetrics.stringWidth(texto, "DMSerif", size) * ANGOSTA / 100
    t.setTextOrigin(cx - ancho / 2, y)
    t.textOut(texto)
    cv.drawText(t)
    cv.restoreState()


def manuscrita(cv, texto, cx, y, size, color, recorte, angulo=-6):
    """Texto manuscrito con un contorno del color de fondo que «corta» lo que tiene abajo."""
    ancho = pdfmetrics.stringWidth(texto, "Script", size)
    cv.saveState()
    cv.translate(cx, y)
    cv.rotate(angulo)
    for modo, grosor in ((1, size * 0.09), (0, 0)):
        cv.saveState()  # el modo de trazo (Tr) persiste entre textos: cada pasada aislada
        t = cv.beginText()
        t.setFont("Script", size)
        t.setTextRenderMode(modo)
        cv.setStrokeColor(recorte)
        cv.setLineWidth(grosor)
        cv.setLineJoin(1)
        t.setFillColor(color)
        t.setTextOrigin(-ancho / 2, 0)
        t.textOut(texto)
        cv.drawText(t)
        cv.restoreState()
    cv.restoreState()


def logotipo(cv, cx, cy, tapa, escala=1.0):
    serif_alta(cv, "THE", cx, cy + 14 * mm * escala, 92 * escala, tapa.tinta)
    serif_alta(cv, "LIST", cx, cy - 34 * mm * escala, 92 * escala, tapa.tinta)
    manuscrita(cv, "Dating", cx + 2 * mm * escala, cy - 8 * mm * escala, 74 * escala, tapa.tinta, tapa.fondo)


def cuaderno(cv, x, y, tapa):
    """Cuaderno de tapa dura: sombra, tapa, lomo, cinta señaladora y elástico."""
    cv.setFillColor(HexColor("#000000"), alpha=0.18)
    cv.roundRect(x + 2 * mm, y - 2.5 * mm, PW, PH, 3 * mm, stroke=0, fill=1)
    cv.setFillColor(tapa.fondo)
    cv.roundRect(x, y, PW, PH, 3 * mm, stroke=0, fill=1)
    cv.setFillColor(HexColor("#000000"), alpha=0.10)
    cv.rect(x, y, 3 * mm, PH, stroke=0, fill=1)  # bisagra del lomo
    cv.setFillColor(tapa.elastico)
    cv.rect(x + 30 * mm, y - 9 * mm, 3.2 * mm, 11 * mm, stroke=0, fill=1)  # cinta señaladora
    p = cv.beginPath()
    p.moveTo(x + 30 * mm, y - 9 * mm)
    p.lineTo(x + 31.6 * mm, y - 7 * mm)
    p.lineTo(x + 33.2 * mm, y - 9 * mm)
    p.close()
    cv.setFillColor(HexColor("#ECE6DC"))
    cv.drawPath(p, stroke=0, fill=1)


def elastico(cv, x, y, tapa):
    cv.setFillColor(tapa.elastico)
    cv.rect(x + PW - 16 * mm, y - 0.6 * mm, 4.2 * mm, PH + 1.2 * mm, stroke=0, fill=1)
    cv.setFillColor(HexColor("#FFFFFF"), alpha=0.08)
    cv.rect(x + PW - 16 * mm, y, 1.2 * mm, PH, stroke=0, fill=1)


def fondo_100(cv, x, y, tapa):
    """«100» gigante tono sobre tono, cortado por el borde: el detalle de fondo."""
    cv.saveState()
    p = cv.beginPath()
    p.roundRect(x, y, PW, PH, 3 * mm)
    cv.clipPath(p, stroke=0, fill=0)
    t = cv.beginText()
    t.setFont("DMSerif", 250)
    t.setHorizScale(ANGOSTA)
    t.setFillColor(tapa.sombra)
    t.setTextOrigin(x + 38 * mm, y - 12 * mm)
    t.textOut("100")
    cv.drawText(t)
    cv.restoreState()  # también deshace la escala horizontal


def edicion(cv, x, y, tapa):
    """1 · Los nombres van arriba, como una «edición» exclusiva."""
    cuaderno(cv, x, y, tapa)
    fondo_100(cv, x, y, tapa)
    cx = x + PW / 2 - 4 * mm
    a, b = PAREJA["nombres"]
    cv.setFillColor(tapa.tinta)
    cv.setFont("DMSerif", 11)
    cv.drawCentredString(cx, y + PH - 24 * mm, f"Edición {a} & {b}")
    logotipo(cv, cx, y + PH / 2 + 6 * mm, tapa)
    cv.setFont("PopR", 7.5)
    cv.drawCentredString(cx, y + 50 * mm, "100 citas para hacer juntos")
    cv.setFont("DMSerifIt", 10)
    cv.drawCentredString(cx, y + 20 * mm, f"desde {PAREJA['desde']}")
    elastico(cv, x, y, tapa)


def iniciales(cv, x, y, tapa):
    """2 · Año arriba y monograma con las iniciales abajo."""
    cuaderno(cv, x, y, tapa)
    cx = x + PW / 2 - 4 * mm
    cv.setFillColor(tapa.tinta)
    cv.setFont("DMSerif", 11)
    cv.drawCentredString(cx, y + PH - 24 * mm, "Edición 2026")
    logotipo(cv, cx, y + PH / 2 + 14 * mm, tapa)
    cv.setFont("PopR", 7.5)
    cv.drawCentredString(cx, y + 64 * mm, "100 citas para hacer juntos")
    a, b = PAREJA["iniciales"]
    cv.setStrokeColor(tapa.tinta)
    cv.setLineWidth(0.6)
    cv.line(cx - 30 * mm, y + 36 * mm, cx - 15 * mm, y + 36 * mm)
    cv.line(cx + 15 * mm, y + 36 * mm, cx + 30 * mm, y + 36 * mm)
    cv.setFont("Script", 34)
    cv.drawCentredString(cx, y + 32 * mm, f"{a}&{b}")
    cv.setFont("PopM", 7)
    cv.drawCentredString(cx, y + 20 * mm, PAREJA["desde"])
    elastico(cv, x, y, tapa)


def main():
    W = 3 * PW + 4 * GAP
    H = PH + 40 * mm
    pdf = os.path.join(AQUI, "portadas-personalizadas.pdf")
    cv = canvas.Canvas(pdf, pagesize=(W, H))
    cv.setFillColor(HexColor("#F3ECE2"))
    cv.rect(0, 0, W, H, stroke=0, fill=1)
    cv.setFillColor(HexColor("#2A1A1C"))
    cv.setFont("PopB", 22)
    cv.drawString(GAP, H - 14 * mm, "The Dating List · portadas personalizadas")
    piezas = ((edicion, BORDO, "1 · Edición con nombres"), (iniciales, BORDO, "2 · Monograma con iniciales"),
              (edicion, CREMA, "3 · Edición con nombres, en crema"))
    for i, (dibujar, tapa, et) in enumerate(piezas):
        x = GAP + i * (PW + GAP)
        dibujar(cv, x, 14 * mm, tapa)
        cv.setFont("PopM", 10)
        cv.setFillColor(HexColor("#5A4A4C"))
        cv.drawString(x, 14 * mm + PH + 4 * mm, et)
    cv.showPage()
    cv.save()
    subprocess.run(["pdftoppm", "-r", "90", "-png", "-singlefile", pdf,
                    os.path.join(AQUI, "portadas-personalizadas")], check=True)
    os.remove(pdf)
    print("ok portadas-personalizadas.png")


if __name__ == "__main__":
    main()
