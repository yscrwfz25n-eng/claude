"""Genera el PDF imprimible de OPINÓLOGOS.

Uso:  python3 generar_pdf.py  ->  opinologos-imprimible.pdf

Cartas de 63 x 88 mm (tamaño póker), 9 por hoja A4.
Cada hoja de frentes va seguida de su hoja de dorsos, espejada para
imprimir doble faz girando por el borde largo.
"""
import os

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

import contenido as c

SALIDA = "opinologos-imprimible.pdf"
NOMBRE = "OPINÓLOGOS"
LEMA = "Todos opinan. Pocos convencen."

CW, CH = 63 * mm, 88 * mm
COLS, ROWS = 3, 3
PW, PH = A4
MX, MY = (PW - COLS * CW) / 2, (PH - ROWS * CH) / 2
PAD = 5 * mm
BANDA = 12 * mm

FUENTES = {
    "Reg": ["/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"],
    "Bold": ["/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"],
    "Sym": ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
}
for alias, rutas in FUENTES.items():
    ruta = next((r for r in rutas if os.path.exists(r)), None)
    if ruta is None:
        raise SystemExit(f"Falta la fuente para {alias}: instalá fonts-liberation y fonts-dejavu")
    pdfmetrics.registerFont(TTFont(alias, ruta))

TINTA = HexColor("#1E1E24")
GRIS = HexColor("#8A8A93")
CORTE = HexColor("#C9C9CF")
VERDE = HexColor("#2E9E5B")
ROJO = HexColor("#D64545")

NIVELES = [
    ("CALENTAMIENTO", HexColor("#2F80ED")),
    ("PICANTE", HexColor("#E67E22")),
    ("PROFUNDO", HexColor("#B3261E")),
]

MAZOS = {
    "tema": ("TEMA", TINTA, "3 NIVELES POR CARTA"),
    "accion": ("ACCIÓN", HexColor("#6C3FB5"), "CARTA DE ACCIÓN"),
    "ayuda": ("AYUDA", HexColor("#4A4A55"), "RESUMEN DE LA RONDA"),
}


def texto_ajustado(cv, html, x, y, w, h, fuente="Bold", maximo=17, minimo=8,
                   color=TINTA, alineado=TA_CENTER, vcentro=True):
    """Dibuja un párrafo con el tamaño de letra más grande que entra en la caja."""
    size = maximo
    while True:
        estilo = ParagraphStyle("p", fontName=fuente, fontSize=size, leading=size * 1.22,
                                textColor=color, alignment=alineado)
        p = Paragraph(html, estilo)
        _, alto = p.wrap(w, h)
        if alto <= h or size <= minimo:
            break
        size -= 0.5
    oy = y + (h - alto) / 2 if vcentro else y + h - alto
    p.drawOn(cv, x, oy)


def marco(cv, x, y):
    cv.setStrokeColor(CORTE)
    cv.setLineWidth(0.4)
    cv.roundRect(x, y, CW, CH, 3 * mm, stroke=1, fill=0)


def marcas_de_corte(cv):
    cv.setStrokeColor(GRIS)
    cv.setLineWidth(0.3)
    largo = 4 * mm
    for i in range(COLS + 1):
        x = MX + i * CW
        cv.line(x, MY - 1 * mm, x, MY - 1 * mm - largo)
        cv.line(x, PH - MY + 1 * mm, x, PH - MY + 1 * mm + largo)
    for j in range(ROWS + 1):
        y = MY + j * CH
        cv.line(MX - 1 * mm, y, MX - 1 * mm - largo, y)
        cv.line(PW - MX + 1 * mm, y, PW - MX + 1 * mm + largo, y)


def banda(cv, x, y, color, izquierda, derecha=""):
    p = cv.beginPath()
    r = 3 * mm
    top = y + CH
    p.moveTo(x, top - BANDA)
    p.lineTo(x, top - r)
    p.arcTo(x, top - 2 * r, x + 2 * r, top, 180, -90)
    p.lineTo(x + CW - r, top)
    p.arcTo(x + CW - 2 * r, top - 2 * r, x + CW, top, 90, -90)
    p.lineTo(x + CW, top - BANDA)
    p.close()
    cv.setFillColor(color)
    cv.drawPath(p, stroke=0, fill=1)
    cv.setFillColor(white)
    cv.setFont("Bold", 8.5)
    cv.drawString(x + PAD, top - BANDA + 4.3 * mm, izquierda)
    if derecha:
        cv.setFont("Reg", 7.5)
        cv.drawRightString(x + CW - PAD, top - BANDA + 4.3 * mm, derecha)


def pie(cv, x, y, texto=NOMBRE):
    cv.setFillColor(GRIS)
    cv.setFont("Bold", 6.5)
    cv.drawCentredString(x + CW / 2, y + 4 * mm, texto)


def dorso(cv, x, y, color, titulo, subtitulo):
    cv.setFillColor(color)
    cv.rect(x, y, CW, CH, stroke=0, fill=1)
    cv.setStrokeColor(white)
    cv.setLineWidth(1.2)
    cv.roundRect(x + 4 * mm, y + 4 * mm, CW - 8 * mm, CH - 8 * mm, 2 * mm, stroke=1, fill=0)
    cv.setFillColor(white)
    cv.setFont("Bold", 18)
    cv.drawCentredString(x + CW / 2, y + CH / 2 + 4 * mm, NOMBRE)
    cv.setFont("Reg", 7.5)
    cv.drawCentredString(x + CW / 2, y + CH / 2 - 2 * mm, LEMA)
    cv.setFont("Bold", 8.5)
    cv.drawCentredString(x + CW / 2, y + CH / 2 - 14 * mm, titulo)
    cv.setFont("Reg", 7)
    cv.drawCentredString(x + CW / 2, y + CH / 2 - 19 * mm, subtitulo)


# ---------- frentes ----------

def frente_tema(numero, temas):
    """Una carta con un tema por nivel: se lee solo el del nivel de la partida."""
    titulo, color, _ = MAZOS["tema"]

    def dibujar(cv, x, y):
        marco(cv, x, y)
        banda(cv, x, y, color, titulo, f"#{numero:02d}")
        alto = (CH - BANDA - 10 * mm) / 3
        tope = y + CH - BANDA - 1.5 * mm
        for i, ((nivel, col), texto) in enumerate(zip(NIVELES, temas)):
            sy = tope - (i + 1) * alto
            cv.setFillColor(col)
            cv.rect(x + 3 * mm, sy + 1.5 * mm, 1.6 * mm, alto - 3 * mm, stroke=0, fill=1)
            cv.setFont("Bold", 6.5)
            cv.drawString(x + 6.5 * mm, sy + alto - 4.2 * mm, nivel)
            texto_ajustado(cv, texto, x + 6.5 * mm, sy + 1.5 * mm, CW - 10.5 * mm, alto - 6.5 * mm,
                           maximo=11, minimo=8, alineado=0)
            if i < 2:
                cv.setStrokeColor(CORTE)
                cv.setLineWidth(0.4)
                cv.line(x + 3 * mm, sy, x + CW - 3 * mm, sy)
        pie(cv, x, y)
    return dibujar


def frente_accion(nombre, quien, texto):
    _, color, _ = MAZOS["accion"]

    def dibujar(cv, x, y):
        marco(cv, x, y)
        banda(cv, x, y, color, "ACCIÓN", quien)
        texto_ajustado(cv, nombre, x + PAD, y + CH - BANDA - 22 * mm, CW - 2 * PAD, 18 * mm,
                       maximo=16, minimo=11, color=color)
        texto_ajustado(cv, texto, x + PAD, y + 12 * mm, CW - 2 * PAD, CH - BANDA - 38 * mm,
                       fuente="Reg", maximo=11, minimo=8)
        pie(cv, x, y)
    return dibujar


def cara_voto(a_favor):
    color = VERDE if a_favor else ROJO
    simbolo = "✔" if a_favor else "✖"
    etiqueta = "A FAVOR" if a_favor else "EN CONTRA"

    def dibujar(cv, x, y):
        cv.setFillColor(color)
        cv.rect(x, y, CW, CH, stroke=0, fill=1)
        cv.setFillColor(white)
        cv.setFont("Sym", 60)
        cv.drawCentredString(x + CW / 2, y + CH / 2 + 4 * mm, simbolo)
        cv.setFont("Bold", 21)
        cv.drawCentredString(x + CW / 2, y + CH / 2 - 14 * mm, etiqueta)
        cv.setFont("Bold", 6.5)
        cv.drawCentredString(x + CW / 2, y + 6 * mm, "VOTO · " + NOMBRE)
    return dibujar


def frente_ayuda():
    def dibujar(cv, x, y):
        marco(cv, x, y)
        banda(cv, x, y, MAZOS["ayuda"][1], "CÓMO SE JUEGA", "1 RONDA")
        html = "<br/>".join(f"<font name='Bold'>{t}</font> {d}" for t, d in c.AYUDA)
        texto_ajustado(cv, html, x + 4 * mm, y + 9 * mm, CW - 8 * mm, CH - BANDA - 12 * mm,
                       fuente="Reg", maximo=8.5, minimo=6, alineado=0, vcentro=False)
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

    titulo, color, sub = MAZOS["tema"]
    fr = [frente_tema(i + 1, t) for i, t in enumerate(zip(c.CALENTAMIENTO, c.PICANTE, c.PROFUNDO))]
    plan += hojas(fr, [lambda cv, x, y: dorso(cv, x, y, color, titulo, sub)] * len(fr))

    at, ac, asub = MAZOS["accion"]
    fr = [frente_accion(n, q, t) for n, q, t, k in c.ACCION for _ in range(k)]
    plan += hojas(fr, [lambda cv, x, y: dorso(cv, x, y, ac, at, asub)] * len(fr))

    # Votos: una carta doble faz por jugador (verde de un lado, roja del otro).
    plan += hojas([cara_voto(True)] * 8, [cara_voto(False)] * 8)

    yt, yc, ys = MAZOS["ayuda"]
    plan += hojas([frente_ayuda()] * 8, [lambda cv, x, y: dorso(cv, x, y, yc, yt, ys)] * 8)

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
