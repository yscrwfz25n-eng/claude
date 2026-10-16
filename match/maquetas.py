"""Maquetas de estilo para MATCH: dos propuestas sobre las mismas 6 cartas.

Uso:  python3 match/maquetas.py  ->  match/estilo-a-noche.png, match/estilo-b-rosa.png,
      match/estilo-c-pasion.png
"""
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))

import generar_pdf as base  # noqa: E402  (registra Poppins y Sym)
from reportlab.lib.colors import HexColor, white  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.pdfbase import pdfmetrics  # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402

F = os.path.join(os.path.dirname(AQUI), "fuentes")
pdfmetrics.registerFont(TTFont("DMSerif", os.path.join(F, "DMSerifDisplay-Regular.ttf")))
pdfmetrics.registerFont(TTFont("DMSerifIt", os.path.join(F, "DMSerifDisplay-Italic.ttf")))

CW, CH, M = base.CW, base.CH, 6 * mm
GAP = 9 * mm

MUESTRAS = [
    ("pregunta", "ambos", False, "Contá qué pensaste la primera vez que viste a tu pareja."),
    ("pregunta", "pareja", False, "¿Cuál es mi comida favorita?"),
    ("pregunta", "pareja", True, "¿Dónde me gusta más que me besen?"),
    ("reto", None, True, "Dale un beso donde elija tu pareja."),
    ("dorso", "preguntas", None, None),
    ("dorso", "retos", None, None),
]


def redondeada(cv, x, y, color):
    cv.setFillColor(color)
    cv.roundRect(x, y, CW, CH, 3 * mm, stroke=0, fill=1)


def pastilla(cv, x, y, texto, fondo, tinta, fuente="PopSB", size=6.5):
    ancho = pdfmetrics.stringWidth(texto, fuente, size) + 5 * mm
    cv.setFillColor(fondo)
    cv.roundRect(x, y, ancho, 5.5 * mm, 2.75 * mm, stroke=0, fill=1)
    cv.setFillColor(tinta)
    cv.setFont(fuente, size)
    cv.drawString(x + 2.5 * mm, y + 1.8 * mm, texto)
    return ancho


def circulos(cv, cx, cy, r, c1, c2, grosor):
    cv.setLineWidth(grosor)
    cv.setStrokeColor(c1)
    cv.circle(cx - r * 0.7, cy, r, stroke=1, fill=0)
    cv.setStrokeColor(c2)
    cv.circle(cx + r * 0.7, cy, r, stroke=1, fill=0)


# ---------------- A · NOCHE ----------------
class Noche:
    nombre = "A · Noche"
    bajada = "Fondo oscuro, rosa neón y letra grande. Se siente íntimo, de juego para después de las 22."
    fondo = HexColor("#16121C")
    rosa = HexColor("#FF3D7F")
    lila = HexColor("#B9A7FF")
    gris = HexColor("#8C8496")

    def logo(self, cv, x, y, size, centrado=False):
        ancho = pdfmetrics.stringWidth("match", "PopB", size)
        r = size * 0.16
        total = ancho + r * 4
        x0 = x - total / 2 if centrado else x
        cv.setFillColor(white)
        cv.setFont("PopB", size)
        cv.drawString(x0, y, "match")
        circulos(cv, x0 + ancho + r * 2, y + size * 0.3, r, self.lila, self.rosa, max(0.6, size * 0.05))

    def carta(self, cv, x, y, tipo, quien, hot, texto):
        redondeada(cv, x, y, self.fondo)
        if tipo == "dorso":
            self.logo(cv, x + CW / 2, y + CH / 2, 26, centrado=True)
            cv.setFillColor(self.rosa if quien == "retos" else self.lila)
            cv.setFont("PopM", 8)
            cv.drawCentredString(x + CW / 2, y + 10 * mm, quien)
            return
        if tipo == "reto":
            cv.setFillColor(self.rosa)
            cv.setFont("PopB", 22)
            cv.drawString(x + M, y + CH - 18 * mm, "reto")
        elif quien == "pareja":
            pastilla(cv, x + M, y + CH - 13 * mm, "responde tu pareja", self.lila, self.fondo)
        if hot:
            pastilla(cv, x + CW - M - 10 * mm, y + CH - 13 * mm, "+18", self.rosa, white)
        base.parrafo(cv, texto, x + M, y + 14 * mm, CW - 2 * M, CH - 40 * mm, "PopSB", 15, 10,
                     color=white, vertical="centro", interlineado=1.2)
        self.logo(cv, x + M, y + 6 * mm, 7)


# ---------------- B · ROSA ----------------
class Rosa:
    nombre = "B · Rosa"
    bajada = "Rosa pastel con bordó y letra con serifa. Romántico, ideal para regalar."
    fondo = HexColor("#FBE3E6")
    bordo = HexColor("#7A1734")
    coral = HexColor("#F2546B")
    crema = HexColor("#FFF6F2")

    def logo(self, cv, x, y, size, color=None, centrado=False, color2=None):
        color = color or self.bordo
        color2 = color2 or self.coral
        ancho = pdfmetrics.stringWidth("match", "DMSerifIt", size)
        r = size * 0.15
        total = ancho + r * 4
        x0 = x - total / 2 if centrado else x
        cv.setFillColor(color)
        cv.setFont("DMSerifIt", size)
        cv.drawString(x0, y, "match")
        circulos(cv, x0 + ancho + r * 2, y + size * 0.3, r, color, color2, max(0.6, size * 0.045))

    def carta(self, cv, x, y, tipo, quien, hot, texto):
        if tipo == "dorso":
            redondeada(cv, x, y, self.bordo if quien == "retos" else self.coral)
            self.logo(cv, x + CW / 2, y + CH / 2, 30, color=self.crema, centrado=True,
                      color2=self.bordo if quien == "preguntas" else self.coral)
            cv.setFillColor(self.crema)
            cv.setFont("PopM", 8)
            cv.drawCentredString(x + CW / 2, y + 10 * mm, quien)
            return
        redondeada(cv, x, y, self.bordo if tipo == "reto" else self.fondo)
        tinta = self.crema if tipo == "reto" else self.bordo
        if tipo == "reto":
            cv.setFillColor(self.crema)
            cv.setFont("DMSerifIt", 24)
            cv.drawString(x + M, y + CH - 19 * mm, "reto")
        elif quien == "pareja":
            pastilla(cv, x + M, y + CH - 13 * mm, "responde tu pareja", self.bordo, self.crema)
        if hot:
            pastilla(cv, x + CW - M - 10 * mm, y + CH - 13 * mm, "+18", self.coral, white)
        base.parrafo(cv, texto, x + M, y + 14 * mm, CW - 2 * M, CH - 40 * mm, "DMSerif", 17, 11,
                     color=tinta, vertical="centro", interlineado=1.15)
        self.logo(cv, x + M, y + 6 * mm, 9, color=tinta)


# ---------------- C · PASIÓN ----------------
class Pasion:
    nombre = "C · Pasión"
    bajada = "Negro, rojo y bordó con detalles en beige. Elegante y sensual, tipo etiqueta de vino."
    negro = HexColor("#0F0D0D")
    rojo = HexColor("#C8102E")
    bordo = HexColor("#5C0F1E")
    beige = HexColor("#E6D5B8")

    def logo(self, cv, x, y, size, centrado=False, color2=None):
        ancho = pdfmetrics.stringWidth("match", "DMSerifIt", size)
        r = size * 0.15
        total = ancho + r * 5
        x0 = x - total / 2 if centrado else x
        cv.setFillColor(self.beige)
        cv.setFont("DMSerifIt", size)
        cv.drawString(x0, y, "match")
        circulos(cv, x0 + ancho + r * 2.9, y + size * 0.32, r, self.beige, color2 or self.rojo,
                 max(0.6, size * 0.045))

    def marco(self, cv, x, y):
        cv.setStrokeColor(self.beige)
        cv.setLineWidth(0.5)
        cv.roundRect(x + 2.5 * mm, y + 2.5 * mm, CW - 5 * mm, CH - 5 * mm, 2 * mm, stroke=1, fill=0)

    def carta(self, cv, x, y, tipo, quien, hot, texto):
        fondo = self.bordo if tipo == "reto" or quien == "retos" else self.negro
        redondeada(cv, x, y, fondo)
        self.marco(cv, x, y)
        if tipo == "dorso":
            self.logo(cv, x + CW / 2, y + CH / 2, 30, centrado=True)
            cv.setFillColor(self.beige)
            cv.setFont("PopM", 7.5)
            cv.drawCentredString(x + CW / 2, y + 10 * mm, quien.upper())
            cv.setFillColor(self.rojo)
            cv.circle(x + CW / 2, y + 15 * mm, 0.9 * mm, stroke=0, fill=1)
            return
        if tipo == "reto":
            cv.setFillColor(self.beige)
            cv.setFont("DMSerifIt", 24)
            cv.drawString(x + M, y + CH - 19 * mm, "reto")
            cv.setStrokeColor(self.rojo)
            cv.setLineWidth(1.2)
            cv.line(x + M, y + CH - 21.5 * mm, x + M + 12 * mm, y + CH - 21.5 * mm)
        elif quien == "pareja":
            pastilla(cv, x + M, y + CH - 13 * mm, "responde tu pareja", self.beige, self.negro)
        if hot:
            pastilla(cv, x + CW - M - 10 * mm, y + CH - 13 * mm, "+18", self.rojo, self.beige)
        base.parrafo(cv, texto, x + M, y + 14 * mm, CW - 2 * M, CH - 40 * mm, "DMSerif", 17, 11,
                     color=self.beige, vertical="centro", interlineado=1.15)
        self.logo(cv, x + M, y + 7 * mm, 9)


def lamina(estilo, salida_pdf):
    W = 6 * CW + 7 * GAP
    H = CH + 46 * mm
    cv = canvas.Canvas(salida_pdf, pagesize=(W, H))
    cv.setFillColor(HexColor("#ECECEC"))
    cv.rect(0, 0, W, H, stroke=0, fill=1)
    cv.setFillColor(HexColor("#111111"))
    cv.setFont("PopB", 20)
    cv.drawString(GAP, H - 15 * mm, estilo.nombre)
    cv.setFont("PopR", 10)
    cv.setFillColor(HexColor("#444444"))
    cv.drawString(GAP, H - 22 * mm, estilo.bajada)
    etiquetas = ["Pregunta (responden los dos)", "Pregunta · responde tu pareja", "Pregunta +18",
                 "Reto +18", "Dorso · preguntas", "Dorso · retos"]
    y = 9 * mm
    for i, (muestra, et) in enumerate(zip(MUESTRAS, etiquetas)):
        x = GAP + i * (CW + GAP)
        estilo.carta(cv, x, y, *muestra)
        cv.setFont("PopM", 8)
        cv.setFillColor(HexColor("#666666"))
        cv.drawString(x, y + CH + 3 * mm, et)
    cv.showPage()
    cv.save()


if __name__ == "__main__":
    for clase, nombre in ((Noche, "estilo-a-noche"), (Rosa, "estilo-b-rosa"),
                          (Pasion, "estilo-c-pasion")):
        pdf = os.path.join(AQUI, nombre + ".pdf")
        lamina(clase(), pdf)
        subprocess.run(["pdftoppm", "-r", "130", "-png", "-singlefile", pdf, os.path.join(AQUI, nombre)],
                       check=True)
        os.remove(pdf)
        print("ok", nombre + ".png")
