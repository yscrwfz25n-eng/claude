"""Genera la caja de OPINÓLOGOS: caja con solapas (tuck box) en una hoja A3.

Uso:  python3 generar_caja.py  ->  opinologos-caja.pdf
  página 1: arte para imprimir (con 3 mm de sangrado y marcas de corte)
  página 2: arte + troquel (guía para cortar y doblar a mano)
  página 3: troquel solo (para plotter de corte)

Interior: ANCHO x ALTO x PROF mm. Si las cartas impresas quedan más gruesas o
más finas, cambiar PROF y volver a generar.
"""
import math

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A3
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

import generar_pdf as cartas  # fuentes, colores y nombre

SALIDA = "opinologos-caja.pdf"
AUTORIA = "un juego de @oficina.grafica_"

# Medidas interiores (mm): 63 x 88 de carta + holgura; profundidad para 110 cartas + librito.
ANCHO, ALTO, PROF = 65 * mm, 90 * mm, 42 * mm
SOLAPA = 15 * mm      # lengüeta que se mete adentro
GUARDAPOLVO = 18 * mm  # aletas laterales arriba y abajo
PESTANA = 10 * mm     # pestaña de pegado
MUESCA = 8 * mm       # radio de la muesca para el pulgar
RADIO = 5 * mm        # esquinas redondeadas de las lengüetas
SANGRADO = 3 * mm

TINTA = cartas.TINTA
GRIS = HexColor("#6E6E6E")
TROQUEL = HexColor("#E6007E")  # magenta: color de troquel habitual

W, H, D, T = ANCHO, ALTO, PROF, SOLAPA
ANCHO_TOTAL = 2 * W + 2 * D + PESTANA
ALTO_TOTAL = H + 2 * (D + T)
PW, PH = A3
X0 = (PW - ANCHO_TOTAL) / 2
Y0 = (PH - ALTO_TOTAL) / 2
YB = Y0 + T + D          # base del cuerpo
YT = YB + H              # tope del cuerpo
# columnas del cuerpo: dorso | lateral | frente | lateral | pestaña
X_DORSO, X_LAT1, X_FRENTE, X_LAT2, X_PEST = (X0, X0 + W, X0 + W + D, X0 + 2 * W + D, X0 + 2 * W + 2 * D)


# ---------- troquel ----------

def contorno(cv):
    """Línea de corte exterior, en sentido horario desde la base del dorso."""
    p = cv.beginPath()
    f, g = GUARDAPOLVO, PESTANA
    p.moveTo(X_DORSO, YB)
    p.lineTo(X_DORSO, YT + D + T - RADIO)
    p.arcTo(X_DORSO, YT + D + T - 2 * RADIO, X_DORSO + 2 * RADIO, YT + D + T, 180, -90)
    p.lineTo(X_LAT1 - RADIO, YT + D + T)
    p.arcTo(X_LAT1 - 2 * RADIO, YT + D + T - 2 * RADIO, X_LAT1, YT + D + T, 90, -90)
    p.lineTo(X_LAT1, YT)
    p.lineTo(X_LAT1 + 2 * mm, YT + f)
    p.lineTo(X_FRENTE - 4 * mm, YT + f)
    p.lineTo(X_FRENTE, YT)
    cx = X_FRENTE + W / 2  # muesca para el pulgar en el borde superior del frente
    p.lineTo(cx - MUESCA, YT)
    p.arcTo(cx - MUESCA, YT - MUESCA, cx + MUESCA, YT + MUESCA, 180, 180)
    p.lineTo(X_LAT2, YT)
    p.lineTo(X_LAT2 + 4 * mm, YT + f)
    p.lineTo(X_PEST - 2 * mm, YT + f)
    p.lineTo(X_PEST, YT)
    p.lineTo(X_PEST + g, YT - 5 * mm)
    p.lineTo(X_PEST + g, YB + 5 * mm)
    p.lineTo(X_PEST, YB)
    p.lineTo(X_PEST - 2 * mm, YB - f)
    p.lineTo(X_LAT2 + 4 * mm, YB - f)
    p.lineTo(X_LAT2, YB)
    p.lineTo(X_LAT2, Y0 + RADIO)
    p.arcTo(X_LAT2 - 2 * RADIO, Y0, X_LAT2, Y0 + 2 * RADIO, 0, -90)
    p.lineTo(X_FRENTE + RADIO, Y0)
    p.arcTo(X_FRENTE, Y0, X_FRENTE + 2 * RADIO, Y0 + 2 * RADIO, 270, -90)
    p.lineTo(X_FRENTE, YB)
    p.lineTo(X_FRENTE - 4 * mm, YB - f)
    p.lineTo(X_LAT1 + 2 * mm, YB - f)
    p.lineTo(X_LAT1, YB)
    cx = X_DORSO + W / 2  # muesca en el borde inferior del dorso
    p.lineTo(cx + MUESCA, YB)
    p.arcTo(cx - MUESCA, YB - MUESCA, cx + MUESCA, YB + MUESCA, 0, 180)
    p.lineTo(X_DORSO, YB)
    p.close()
    return p


def dobleces():
    """Líneas de doblez (punteadas)."""
    return [
        (X_LAT1, YB, X_LAT1, YT), (X_FRENTE, YB, X_FRENTE, YT),
        (X_LAT2, YB, X_LAT2, YT), (X_PEST, YB, X_PEST, YT),
        (X_DORSO, YT, X_LAT1, YT), (X_DORSO, YT + D, X_LAT1, YT + D),
        (X_LAT1, YT, X_FRENTE, YT), (X_LAT2, YT, X_PEST, YT),
        (X_LAT1, YB, X_FRENTE, YB), (X_LAT2, YB, X_PEST, YB),
        (X_FRENTE, YB, X_LAT2, YB), (X_FRENTE, Y0 + T, X_LAT2, Y0 + T),
    ]


def dibujar_troquel(cv):
    cv.setStrokeColor(TROQUEL)
    cv.setLineWidth(0.6)
    cv.drawPath(contorno(cv), stroke=1, fill=0)
    cv.setDash(3, 2)
    for x1, y1, x2, y2 in dobleces():
        cv.line(x1, y1, x2, y2)
    cv.setDash()
    cv.setFont("PopM", 6)
    cv.setFillColor(TROQUEL)
    cv.drawCentredString(X_PEST + PESTANA / 2, (YB + YT) / 2, "pegar")
    cv.setFont("PopR", 7)
    cv.drawString(X0, Y0 - 14 * mm, "— corte      - - - doblez      "
                  f"interior {ANCHO / mm:.0f} x {ALTO / mm:.0f} x {PROF / mm:.0f} mm")


def marcas_de_corte(cv):
    cv.setStrokeColor(cartas.GRIS)
    cv.setLineWidth(0.3)
    sep, largo = SANGRADO + 2 * mm, 6 * mm
    x1, y1, x2, y2 = X0, Y0, X0 + ANCHO_TOTAL, Y0 + ALTO_TOTAL
    for x in (x1, x2):
        cv.line(x, y1 - sep, x, y1 - sep - largo)
        cv.line(x, y2 + sep, x, y2 + sep + largo)
    for y in (y1, y2):
        cv.line(x1 - sep, y, x1 - sep - largo, y)
        cv.line(x2 + sep, y, x2 + sep + largo, y)


# ---------- elementos gráficos ----------

def logo(cv, cx, y, size, color=TINTA):
    ancho = pdfmetrics.stringWidth(cartas.NOMBRE, "PopB", size)
    x0 = cx - (ancho + size * 0.45) / 2
    cv.setFillColor(color)
    cv.setFont("PopB", size)
    cv.drawString(x0, y, cartas.NOMBRE)
    r = size * 0.055
    for i, (_, col) in enumerate(cartas.NIVELES):
        cv.setFillColor(col)
        cv.circle(x0 + ancho + size * 0.12 + i * r * 2.9, y + r * 1.1, r, stroke=0, fill=1)


def girado(cv, cx, cy, angulo, dibujar):
    cv.saveState()
    cv.translate(cx, cy)
    cv.rotate(angulo)
    dibujar()
    cv.restoreState()


def texto(cv, html, x, y, w, h, fuente="PopR", size=6.5, color=TINTA, interlineado=1.35):
    p = Paragraph(html, ParagraphStyle("t", fontName=fuente, fontSize=size, leading=size * interlineado,
                                       textColor=color, alignment=TA_LEFT))
    _, alto = p.wrap(w, h)
    p.drawOn(cv, x, y + h - alto)
    return alto


def mini_carta(cv, cx, cy, angulo, nivel, tema, escala=1.0):
    """Una carta de Tema en miniatura, para ilustrar el frente."""
    nombre, color = cartas.NIVELES[nivel]
    w, h = 30 * mm * escala, 42 * mm * escala

    def dib():
        cv.setFillColor(HexColor("#000000"), alpha=0.08)
        cv.roundRect(-w / 2 + 0.8 * mm, -h / 2 - 0.8 * mm, w, h, 1.5 * mm, stroke=0, fill=1)
        cv.setFillColor(white)
        cv.setStrokeColor(HexColor("#E2E2E2"))
        cv.setLineWidth(0.4)
        cv.roundRect(-w / 2, -h / 2, w, h, 1.5 * mm, stroke=1, fill=1)
        cv.setFillColor(color)
        cv.rect(-w / 2 + 0.2, h / 2 - 1.3 * mm, w - 0.4, 1.1 * mm, stroke=0, fill=1)
        m = 2.8 * mm * escala
        cv.setFont("PopM", 3.2 * escala)
        cv.drawString(-w / 2 + m, h / 2 - 5 * mm * escala, nombre)
        texto(cv, tema, -w / 2 + m, -h / 2 + 12 * mm * escala, w - 2 * m, h - 19 * mm * escala,
              fuente="PopSB", size=7.2 * escala, interlineado=1.2)
        cv.setFont("PopR", 3 * escala)
        cv.setFillColor(TINTA)
        cv.drawString(-w / 2 + m, -h / 2 + 6.5 * mm * escala, "a favor")
        cv.drawRightString(w / 2 - m, -h / 2 + 6.5 * mm * escala, "en contra")
        cv.setFont("PopB", 3 * escala)
        cv.drawString(-w / 2 + m, -h / 2 + 2.8 * mm * escala, cartas.NOMBRE)
    girado(cv, cx, cy, angulo, dib)


# ---------- caras de la caja ----------

def frente(cv):
    x, y = X_FRENTE, YB
    for i, (_, col) in enumerate(cartas.NIVELES):  # franja de los tres niveles, con sangrado arriba
        cv.setFillColor(col)
        cv.rect(x + i * W / 3, YT - 3.5 * mm, W / 3, 3.5 * mm + SANGRADO, stroke=0, fill=1)
    cv.setFillColor(GRIS)
    cv.setFont("PopM", 6)
    cv.drawCentredString(x + W / 2, YT - 12.5 * mm, "juego de debate")
    size = 24
    while pdfmetrics.stringWidth(cartas.NOMBRE, "PopB", size) > W - 16 * mm:
        size -= 0.5
    logo(cv, x + W / 2, YT - 23 * mm, size)
    cv.setFillColor(GRIS)
    cv.setFont("PopR", 6.3)
    cv.drawCentredString(x + W / 2, YT - 29 * mm, cartas.LEMA)
    mini_carta(cv, x + W / 2 - 6 * mm, y + 36 * mm, 8, 2,
               "Una verdad que duele vale más que una mentira que protege.", escala=0.8)
    mini_carta(cv, x + W / 2 + 5 * mm, y + 33 * mm, -6, 0, "El ananá en la pizza es una genialidad.",
               escala=0.8)
    cv.setFillColor(TINTA)
    cv.setFont("PopM", 5.8)
    cv.drawCentredString(x + W / 2, y + 10 * mm, "4 a 8 jugadores  ·  14+  ·  40–60 min")
    cv.setFont("PopSB", 5.8)
    cv.drawCentredString(x + W / 2, y + 5 * mm, AUTORIA)


def dorso_caja(cv):
    x, y, m = X_DORSO, YB, 6 * mm
    cv.setFillColor(TINTA)
    cv.setFont("PopB", 10.5)
    cv.drawString(x + m, YT - 14 * mm, "No gana quien tiene razón.")
    cv.drawString(x + m, YT - 19.5 * mm, "Gana quien convence.")
    texto(cv, "Elegí un tema, votá a favor o en contra y defendé tu postura. "
              "El primero que logra que alguien cambie de opinión se lleva la carta.",
          x + m, YT - 36 * mm, W - 2 * m, 14 * mm, size=6.3, color=GRIS)
    cv.setFillColor(TINTA)
    cv.setFont("PopSB", 7)
    cv.drawString(x + m, YT - 41 * mm, "cómo se juega")
    pasos = [("1", "Se lee un tema: «El que cocina no lava.»"),
             ("2", "¡Opinen! Todos votan a la vez: a favor o en contra."),
             ("3", "Debate libre de 4 minutos, todos contra todos."),
             ("4", "Si alguien dice «¡Me convenciste!», te llevás la carta. Gana quien junta 5.")]
    tope = YT - 43 * mm  # cada paso ocupa solo lo que necesita
    for num, paso in pasos:
        alto = texto(cv, paso, x + m + 3.5 * mm, tope - 20 * mm, W - 2 * m - 3.5 * mm, 20 * mm, size=6)
        cv.setFillColor(cartas.NIVELES[0][1])
        cv.setFont("PopB", 6.3)
        cv.drawString(x + m, tope - 6 * 1.35 + 1.6, num)
        tope -= alto + 1.6 * mm
    cv.setStrokeColor(HexColor("#DADADA"))
    cv.setLineWidth(0.5)
    cv.line(x + m, y + 22 * mm, x + W - m, y + 22 * mm)
    texto(cv, "<font name='PopSB'>Contiene:</font> 70 cartas de Tema (140 temas), 24 de Acción, "
              "8 de Voto, 8 de Ayuda y reglamento.",
          x + m, y + 14 * mm, W - 2 * m, 7 * mm, size=5.3, color=GRIS)
    cv.setFillColor(TINTA)
    cv.setFont("PopSB", 5.5)
    cv.drawString(x + m, y + 10.5 * mm, AUTORIA)  # arriba de la muesca del pulgar


def laterales(cv):
    cy = (YB + YT) / 2
    girado(cv, X_LAT1 + D / 2, cy, 90, lambda: logo(cv, 0, -3.5 * mm, 19))

    def ficha():
        cv.setFillColor(TINTA)
        cv.setFont("PopSB", 8)
        cv.drawCentredString(0, 1.5 * mm, "4 a 8 jugadores · 14+ · 40–60 min")
        cv.setFillColor(GRIS)
        cv.setFont("PopR", 6.5)
        cv.drawCentredString(0, -4.5 * mm, cartas.LEMA)
    girado(cv, X_LAT2 + D / 2, cy, 90, ficha)


def tapas(cv):
    # tapa superior (sale del dorso): se lee desde el frente, así que va girada 180°
    girado(cv, X_DORSO + W / 2, YT + D / 2, 180, lambda: logo(cv, 0, -2.5 * mm, 15))

    def base():
        cv.setFillColor(TINTA)
        cv.setFont("PopSB", 6.5)
        cv.drawCentredString(0, 1 * mm, AUTORIA)
        cv.setFillColor(GRIS)
        cv.setFont("PopR", 5.5)
        cv.drawCentredString(0, -4 * mm, "110 cartas · reglamento")
    girado(cv, X_FRENTE + W / 2, Y0 + T + D / 2, 180, base)


def arte(cv):
    cv.setFillColor(white)
    cv.rect(X0 - SANGRADO, Y0 - SANGRADO, ANCHO_TOTAL + 2 * SANGRADO, ALTO_TOTAL + 2 * SANGRADO,
            stroke=0, fill=1)
    frente(cv)
    dorso_caja(cv)
    laterales(cv)
    tapas(cv)


def main():
    cv = canvas.Canvas(SALIDA, pagesize=A3)
    cv.setTitle("Opinólogos – caja")
    cv.setAuthor("@oficina.grafica_")
    for pagina in ("arte", "guia", "troquel"):
        if pagina in ("arte", "guia"):
            arte(cv)
            marcas_de_corte(cv)
        if pagina in ("guia", "troquel"):
            dibujar_troquel(cv)
        cv.setFont("PopM", 8)
        cv.setFillColor(GRIS)
        titulo = {"arte": "1 · arte para imprimir", "guia": "2 · arte + troquel (guía de corte y doblez)",
                  "troquel": "3 · troquel (corte en línea continua, doblez en punteada)"}[pagina]
        cv.drawString(15 * mm, PH - 15 * mm, f"opinólogos · caja · {titulo}")
        cv.showPage()
    cv.save()
    print(f"{SALIDA}: caja de {ANCHO / mm:.0f} x {ALTO / mm:.0f} x {PROF / mm:.0f} mm, "
          f"desplegado {ANCHO_TOTAL / mm:.0f} x {ALTO_TOTAL / mm:.0f} mm en A3")


if __name__ == "__main__":
    main()
