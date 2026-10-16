"""Genera el PDF imprimible de OPINÓLOGOS (estilo C · Minimal).

Uso:  python3 generar_pdf.py  ->  opinologos-muestra-imprenta.pdf (solo cartas)

Cartas de 63 x 88 mm (tamaño póker), 9 por hoja A4.
Cada hoja de frentes va seguida de su hoja de dorsos, espejada para
imprimir doble faz girando por el borde largo.
Tipografías: Poppins (OFL, carpeta fuentes/) y DejaVu Sans para ✔ ✖.
"""
import os

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

import contenido as c

SALIDA = "opinologos-muestra-imprenta.pdf"
NOMBRE = "opinólogos"
LEMA = "todos opinan. pocos convencen."

CW, CH = 63 * mm, 88 * mm
COLS, ROWS = 3, 3
PW, PH = A4
MX, MY = (PW - COLS * CW) / 2, (PH - ROWS * CH) / 2
M = 6 * mm  # margen interno de las cartas
SANGRADO = 3 * mm  # color extra hacia afuera en las cartas de fondo pleno

AQUI = os.path.dirname(os.path.abspath(__file__))
FUENTES = {
    "PopR": os.path.join(AQUI, "fuentes", "Poppins-Regular.ttf"),
    "PopM": os.path.join(AQUI, "fuentes", "Poppins-Medium.ttf"),
    "PopSB": os.path.join(AQUI, "fuentes", "Poppins-SemiBold.ttf"),
    "PopB": os.path.join(AQUI, "fuentes", "Poppins-Bold.ttf"),
    "Sym": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
}
for alias, ruta in FUENTES.items():
    if not os.path.exists(ruta):
        raise SystemExit(f"Falta la fuente {ruta}")
    pdfmetrics.registerFont(TTFont(alias, ruta))

TINTA = HexColor("#111111")
GRIS = HexColor("#8C8C8C")
LINEA = HexColor("#DADADA")
OSCURO = HexColor("#111111")
GRIS_OSCURO = HexColor("#9A9A9A")
VIOLETA = HexColor("#6B4EE6")
VERDE = HexColor("#1F9D5C")
ROJO = HexColor("#D93A3A")

NIVELES = [
    ("calentamiento", HexColor("#2F6FED")),
    ("picante", HexColor("#F08A24")),
    ("profundo", HexColor("#D7263D")),
]


def parrafo(cv, html, x, y, w, h, fuente, maximo, minimo, color=TINTA, interlineado=1.22,
            vertical="arriba"):
    """Dibuja un párrafo alineado a la izquierda con la letra más grande que entra en la caja."""
    size = maximo
    while True:
        estilo = ParagraphStyle("p", fontName=fuente, fontSize=size, leading=size * interlineado,
                                textColor=color, alignment=TA_LEFT)
        p = Paragraph(html, estilo)
        _, alto = p.wrap(w, h)
        if alto <= h or size <= minimo:
            break
        size -= 0.5
    oy = y + h - alto if vertical == "arriba" else y + (h - alto) / 2
    p.drawOn(cv, x, oy)


def fondo(cv, x, y, color):
    """Fondo pleno con sangrado solo hacia el borde exterior de la grilla.

    Entre cartas vecinas no hay sangrado: el corte es exacto y así una carta de
    otro color al lado no queda manchada.
    """
    def en(a, b):
        return abs(a - b) < 0.01
    izq = SANGRADO if en(x, MX) else 0
    der = SANGRADO if en(x + CW, MX + COLS * CW) else 0
    aba = SANGRADO if en(y, MY) else 0
    arr = SANGRADO if en(y + CH, PH - MY) else 0
    cv.setFillColor(color)
    cv.rect(x - izq, y - aba, CW + izq + der, CH + aba + arr, stroke=0, fill=1)


def marcas_de_corte(cv):
    cv.setStrokeColor(GRIS)
    cv.setLineWidth(0.3)
    largo, sep = 5 * mm, SANGRADO + 1 * mm  # las marcas empiezan afuera del sangrado
    for i in range(COLS + 1):
        x = MX + i * CW
        cv.line(x, MY - sep, x, MY - sep - largo)
        cv.line(x, PH - MY + sep, x, PH - MY + sep + largo)
    for j in range(ROWS + 1):
        y = MY + j * CH
        cv.line(MX - sep, y, MX - sep - largo, y)
        cv.line(PW - MX + sep, y, PW - MX + sep + largo, y)


def pie(cv, x, y, color_texto=TINTA, punto=None):
    """Logo chico abajo a la izquierda, con un punto del color del nivel si corresponde."""
    cv.setFont("PopB", 6.3)
    cv.setFillColor(color_texto)
    cv.drawString(x + M, y + 5.5 * mm, NOMBRE)
    if punto is not None:
        cv.setFillColor(punto)
        ancho = pdfmetrics.stringWidth(NOMBRE, "PopB", 6.3)
        cv.circle(x + M + ancho + 1.3 * mm, y + 6.1 * mm, 0.8 * mm, stroke=0, fill=1)


def etiqueta(cv, x, y, izquierda, color, derecha=""):
    cv.setFont("PopM", 6.3)
    cv.setFillColor(color)
    cv.drawString(x + M, y + CH - 10 * mm, izquierda)
    if derecha:
        cv.setFillColor(GRIS)
        cv.drawRightString(x + CW - M, y + CH - 10 * mm, derecha)


def dorso(palabra, color_palabra):
    """Dorso oscuro con el logo, los tres puntos de nivel y el nombre del mazo."""
    def dibujar(cv, x, y):
        fondo(cv, x, y, OSCURO)
        cv.setFillColor(white)
        cv.setFont("PopB", 17)
        ancho = pdfmetrics.stringWidth(NOMBRE, "PopB", 17)
        x0 = x + (CW - ancho - 8 * mm) / 2
        cv.drawString(x0, y + CH / 2, NOMBRE)
        for i, (_, col) in enumerate(NIVELES):
            cv.setFillColor(col)
            cv.circle(x0 + ancho + 1.8 * mm + i * 2.6 * mm, y + CH / 2 + 0.9 * mm, 0.9 * mm,
                      stroke=0, fill=1)
        cv.setFillColor(GRIS_OSCURO)
        cv.setFont("PopR", 7)
        cv.drawCentredString(x + CW / 2, y + CH / 2 - 7 * mm, LEMA)
        cv.setFillColor(color_palabra)
        cv.setFont("PopM", 6.8)
        cv.drawCentredString(x + CW / 2, y + 8 * mm, palabra)
    return dibujar


# ---------- frentes ----------

def cara_tema(nivel, numero, texto, lado):
    """Una cara de carta de Tema: franja y detalles del color del nivel."""
    nombre, color = NIVELES[nivel]

    def dibujar(cv, x, y):
        cv.setFillColor(color)
        cv.rect(x, y + CH - 2.5 * mm, CW, 2.5 * mm, stroke=0, fill=1)
        etiqueta(cv, x, y, nombre, color, f"{numero:02d}{lado}")
        parrafo(cv, texto, x + M, y + 22 * mm, CW - 2 * M, CH - 36 * mm, "PopSB", 15.5, 10)
        cv.setFont("PopR", 6.5)
        cv.setFillColor(TINTA)
        cv.drawString(x + M, y + 13 * mm, "a favor")
        cv.drawRightString(x + CW - M, y + 13 * mm, "en contra")
        cv.setStrokeColor(LINEA)
        cv.setLineWidth(0.5)
        cv.line(x + 17 * mm, y + 14.1 * mm, x + CW - 20 * mm, y + 14.1 * mm)
        pie(cv, x, y, punto=color)
    return dibujar


def frente_accion(nombre, cuando, texto):
    def dibujar(cv, x, y):
        etiqueta(cv, x, y, "acción · " + cuando.lower(), VIOLETA)
        parrafo(cv, nombre, x + M, y + CH - 30 * mm, CW - 2 * M, 16 * mm, "PopB", 19, 12)
        cv.setFillColor(VIOLETA)
        cv.rect(x + M, y + CH - 33 * mm, 8 * mm, 0.9 * mm, stroke=0, fill=1)
        parrafo(cv, texto, x + M, y + 12 * mm, CW - 2 * M, CH - 48 * mm, "PopR", 9.5, 7,
                interlineado=1.4)
        pie(cv, x, y)
    return dibujar


def cara_voto(a_favor):
    color = VERDE if a_favor else ROJO
    palabra = "a favor" if a_favor else "en contra"
    simbolo = "✔" if a_favor else "✖"

    def dibujar(cv, x, y):
        fondo(cv, x, y, color)
        cv.setFillColor(white)
        size = 30
        while pdfmetrics.stringWidth(palabra, "PopB", size) > CW - 2 * M:
            size -= 1
        cv.setFont("PopB", size)
        cv.drawString(x + M, y + CH - 22 * mm, palabra)
        cv.setFont("Sym", 70)
        cv.drawRightString(x + CW - 5 * mm, y + 8 * mm, simbolo)
        pie(cv, x, y, color_texto=white)
    return dibujar


def frente_ayuda():
    def dibujar(cv, x, y):
        etiqueta(cv, x, y, "ayuda · 1 ronda", GRIS)
        cv.setFont("PopB", 14)
        cv.setFillColor(TINTA)
        cv.drawString(x + M, y + CH - 19 * mm, "cómo se juega")
        html = "<br/>".join(f"<font name='PopSB'>{t}</font> {d}" for t, d in c.AYUDA)
        parrafo(cv, html, x + M, y + 11 * mm, CW - 2 * M, CH - 33 * mm, "PopR", 7.5, 5.5,
                interlineado=1.3)
        pie(cv, x, y)
    return dibujar


# ---------- armado de hojas ----------

def hojas(frentes, dorsos):
    """Agrupa de a 9 cartas: devuelve lista de (frentes, dorsos)."""
    n = COLS * ROWS
    return [(frentes[i:i + n], dorsos[i:i + n]) for i in range(0, len(frentes), n)]


def posicion(idx, espejo=False):
    col, fila = idx % COLS, idx // COLS
    if espejo:
        col = COLS - 1 - col
    return MX + col * CW, PH - MY - (fila + 1) * CH


def main():
    plan = []

    # Cartas de Tema doble faz: un tema por cara, las dos caras del mismo nivel.
    fr, ds, numero = [], [], 0
    for nivel, temas in enumerate((c.CALENTAMIENTO, c.PICANTE, c.PROFUNDO)):
        mitad = len(temas) // 2
        for i in range(mitad):
            numero += 1
            fr.append(cara_tema(nivel, numero, temas[i], "a"))
            ds.append(cara_tema(nivel, numero, temas[mitad + i], "b"))
    plan += hojas(fr, ds)

    fr = [frente_accion(n, q, t) for n, q, t, k in c.ACCION for _ in range(k)]
    plan += hojas(fr, [dorso("acción", VIOLETA)] * len(fr))

    # Votos: una carta doble faz por jugador (verde de un lado, roja del otro).
    plan += hojas([cara_voto(True)] * 8, [cara_voto(False)] * 8)

    plan += hojas([frente_ayuda()] * 8, [dorso("ayuda", GRIS_OSCURO)] * 8)

    cv = canvas.Canvas(SALIDA, pagesize=A4)
    cv.setTitle("Opinólogos – cartas imprimibles")
    cv.setAuthor("Opinólogos")
    total = 0
    for frentes, dorsos in plan:
        for i, dibujar in enumerate(frentes):
            dibujar(cv, *posicion(i))
        marcas_de_corte(cv)
        cv.showPage()
        for i, dibujar in enumerate(dorsos):
            dibujar(cv, *posicion(i, espejo=True))
        marcas_de_corte(cv)
        cv.showPage()
        total += len(frentes)
    cv.save()
    print(f"{SALIDA}: {total} cartas en {len(plan) * 2} páginas")


if __name__ == "__main__":
    main()
