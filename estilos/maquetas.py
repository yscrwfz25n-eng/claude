"""Maquetas de 3 estilos visuales para Opinólogos (una lámina PDF por estilo)."""
import os
import sys
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fuentes") + "/"
for alias, archivo in {
    "DMSerif": F + "DMSerifDisplay-Regular.ttf", "DMSerifIt": F + "DMSerifDisplay-Italic.ttf",
    "Archivo": F + "ArchivoBlack-Regular.ttf",
    "PopR": F + "Poppins-Regular.ttf", "PopM": F + "Poppins-Medium.ttf",
    "PopSB": F + "Poppins-SemiBold.ttf", "PopB": F + "Poppins-Bold.ttf",
    "PopXB": F + "Poppins-ExtraBold.ttf",
    "Sym": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
}.items():
    pdfmetrics.registerFont(TTFont(alias, archivo))

CW, CH = 63 * mm, 88 * mm
R = 3 * mm
GAP = 9 * mm
TEMA1 = (0, "El ananá en la pizza es una genialidad.", 1)
TEMA2 = (2, "Una verdad que duele vale más que una mentira que protege.", 47)
ACCION = ("¡Objeción!", "CUANDO QUIERAS",
          "Interrumpí a quien está hablando: tenés 10 segundos para refutarlo. El reloj se pausa.")
NIVELES = ["CALENTAMIENTO", "PICANTE", "PROFUNDO"]


def parrafo(cv, html, x, y, w, h, fuente, maximo, minimo, color, alin=TA_LEFT, v="centro", interl=1.15):
    size = maximo
    while True:
        p = Paragraph(html, ParagraphStyle("p", fontName=fuente, fontSize=size, leading=size * interl,
                                           textColor=color, alignment=alin))
        _, alto = p.wrap(w, h)
        if alto <= h or size <= minimo:
            break
        size -= 0.5
    oy = {"centro": y + (h - alto) / 2, "arriba": y + h - alto, "abajo": y}[v]
    p.drawOn(cv, x, oy)
    return size


def fondo(cv, x, y, color):
    cv.setFillColor(color)
    cv.roundRect(x, y, CW, CH, R, stroke=0, fill=1)


def contorno(cv, x, y, color=HexColor("#D8D2C8")):
    cv.setStrokeColor(color)
    cv.setLineWidth(0.5)
    cv.roundRect(x, y, CW, CH, R, stroke=1, fill=0)


def burbuja(cv, x, y, w, h, color, cola="izq", r=4 * mm):
    cv.setFillColor(color)
    cv.roundRect(x, y, w, h, r, stroke=0, fill=1)
    p = cv.beginPath()
    if cola == "izq":
        p.moveTo(x + 7 * mm, y + 0.5)
        p.lineTo(x + 6 * mm, y - 5 * mm)
        p.lineTo(x + 13 * mm, y + 0.5)
    else:
        p.moveTo(x + w - 13 * mm, y + 0.5)
        p.lineTo(x + w - 6 * mm, y - 5 * mm)
        p.lineTo(x + w - 7 * mm, y + 0.5)
    p.close()
    cv.drawPath(p, stroke=0, fill=1)


# ---------------- ESTILO A · SOBREMESA ----------------
class Sobremesa:
    nombre = "A · Sobremesa"
    bajada = "Editorial y cálido: papel crema, tipografía con serifa, como un buen libro de sobremesa."
    papel = HexColor("#F3EBDD")
    tinta = HexColor("#2B2420")
    niveles = [HexColor("#3F78A6"), HexColor("#D27A2C"), HexColor("#9C2B2E")]
    violeta = HexColor("#5D4B8C")

    def tema(self, cv, x, y, t):
        nivel, texto, n = t
        col = self.niveles[nivel]
        fondo(cv, x, y, self.papel)
        cv.setFillColor(col)
        cv.circle(x + 7 * mm, y + CH - 8 * mm, 1.6 * mm, stroke=0, fill=1)
        cv.setFont("PopSB", 6.5)
        cv.setFillColor(self.tinta)
        cv.drawString(x + 10 * mm, y + CH - 9 * mm, NIVELES[nivel])
        cv.setFont("PopM", 6.5)
        cv.drawRightString(x + CW - 5 * mm, y + CH - 9 * mm, f"Nº {n:02d} · A")
        cv.setFont("DMSerif", 54)
        cv.setFillColor(col)
        cv.drawString(x + 4.5 * mm, y + CH - 30 * mm, "“")
        parrafo(cv, texto, x + 6 * mm, y + 22 * mm, CW - 12 * mm, 42 * mm, "DMSerif", 21, 12,
                self.tinta, v="arriba", interl=1.12)
        cv.setStrokeColor(self.tinta)
        cv.setLineWidth(0.5)
        cv.line(x + 6 * mm, y + 15 * mm, x + CW - 6 * mm, y + 15 * mm)
        cv.setFont("PopSB", 6.5)
        cv.setFillColor(HexColor("#2F7D4F"))
        cv.drawString(x + 6 * mm, y + 10.5 * mm, "A FAVOR")
        cv.setFillColor(HexColor("#B23A32"))
        cv.drawRightString(x + CW - 6 * mm, y + 10.5 * mm, "EN CONTRA")
        cv.setFont("DMSerifIt", 7.5)
        cv.setFillColor(self.tinta)
        cv.drawCentredString(x + CW / 2, y + 5 * mm, "Opinólogos")

    def accion(self, cv, x, y):
        nombre, cuando, texto = ACCION
        fondo(cv, x, y, self.papel)
        cv.setFillColor(self.violeta)
        cv.roundRect(x + 6 * mm, y + CH - 12 * mm, 26 * mm, 5.5 * mm, 2.75 * mm, stroke=0, fill=1)
        cv.setFillColor(self.papel)
        cv.setFont("PopSB", 6)
        cv.drawCentredString(x + 19 * mm, y + CH - 10.2 * mm, cuando)
        parrafo(cv, f"<i>{nombre}</i>", x + 6 * mm, y + CH - 34 * mm, CW - 12 * mm, 18 * mm,
                "DMSerifIt", 26, 14, self.violeta, v="arriba")
        parrafo(cv, texto, x + 6 * mm, y + 16 * mm, CW - 12 * mm, 34 * mm, "PopR", 9.5, 7,
                self.tinta, v="arriba", interl=1.35)
        cv.setFont("DMSerifIt", 7.5)
        cv.setFillColor(self.tinta)
        cv.drawCentredString(x + CW / 2, y + 5 * mm, "Opinólogos")

    def voto(self, cv, x, y):
        fondo(cv, x, y, HexColor("#2F7D4F"))
        cv.setStrokeColor(self.papel)
        cv.setLineWidth(0.8)
        cv.roundRect(x + 4 * mm, y + 4 * mm, CW - 8 * mm, CH - 8 * mm, 2 * mm, stroke=1, fill=0)
        cv.setFillColor(self.papel)
        cv.setFont("Sym", 46)
        cv.drawCentredString(x + CW / 2, y + CH / 2 + 4 * mm, "✔")
        cv.setFont("DMSerif", 26)
        cv.drawCentredString(x + CW / 2, y + CH / 2 - 14 * mm, "A favor")

    def dorso(self, cv, x, y):
        fondo(cv, x, y, self.tinta)
        cv.setStrokeColor(self.papel)
        cv.setLineWidth(0.8)
        cv.roundRect(x + 4 * mm, y + 4 * mm, CW - 8 * mm, CH - 8 * mm, 2 * mm, stroke=1, fill=0)
        cv.setLineWidth(0.3)
        cv.roundRect(x + 5.2 * mm, y + 5.2 * mm, CW - 10.4 * mm, CH - 10.4 * mm, 1.5 * mm, stroke=1, fill=0)
        cv.setFillColor(self.papel)
        cv.setFont("DMSerif", 40)
        cv.drawCentredString(x + CW / 2, y + CH / 2 + 8 * mm, "“")
        cv.setFont("DMSerif", 21)
        cv.drawCentredString(x + CW / 2, y + CH / 2 - 2 * mm, "Opinólogos")
        cv.setFont("DMSerifIt", 8.5)
        cv.drawCentredString(x + CW / 2, y + CH / 2 - 9 * mm, "Todos opinan. Pocos convencen.")
        cv.setFont("PopM", 6)
        cv.drawCentredString(x + CW / 2, y + 10 * mm, "ACCIÓN")


# ---------------- ESTILO B · FIESTA ----------------
class Fiesta:
    nombre = "B · Fiesta"
    bajada = "Pop y ruidoso: colores plenos, globos de diálogo y letra gruesa. Se ve de lejos en la mesa."
    niveles = [HexColor("#2C5BFF"), HexColor("#FF7A00"), HexColor("#E3173E")]
    negro = HexColor("#141414")
    amarillo = HexColor("#FFD23F")
    violeta = HexColor("#7B2FF7")

    def tema(self, cv, x, y, t):
        nivel, texto, n = t
        col = self.niveles[nivel]
        fondo(cv, x, y, col)
        cv.setFillColor(white)
        cv.setFont("Archivo", 9)
        cv.drawString(x + 5 * mm, y + CH - 9.5 * mm, NIVELES[nivel])
        cv.setFont("PopB", 7)
        cv.drawRightString(x + CW - 5 * mm, y + CH - 9.5 * mm, f"#{n:02d}·A")
        bx, by, bw, bh = x + 4.5 * mm, y + 24 * mm, CW - 9 * mm, CH - 38 * mm
        burbuja(cv, bx, by, bw, bh, white)
        parrafo(cv, texto, bx + 4 * mm, by + 3 * mm, bw - 8 * mm, bh - 6 * mm, "Archivo", 17, 10,
                self.negro, alin=TA_LEFT, interl=1.1)
        for i, (txt, c) in enumerate((("✔ A FAVOR", HexColor("#00A862")), ("✖ EN CONTRA", HexColor("#E3173E")))):
            px = x + 4.5 * mm + i * (CW - 9 * mm) / 2 + (1 * mm if i else 0)
            pw = (CW - 9 * mm) / 2 - 1 * mm
            cv.setFillColor(self.negro)
            cv.roundRect(px, y + 9 * mm, pw, 6.5 * mm, 3.25 * mm, stroke=0, fill=1)
            cv.setFillColor(white)
            cv.setFont("Sym", 6.3)
            cv.drawCentredString(px + pw / 2, y + 11.2 * mm, txt)
        cv.setFillColor(white)
        cv.setFont("Archivo", 6.5)
        cv.drawCentredString(x + CW / 2, y + 4 * mm, "OPINÓLOGOS")

    def accion(self, cv, x, y):
        nombre, cuando, texto = ACCION
        fondo(cv, x, y, self.violeta)
        cv.setFillColor(self.amarillo)
        cv.roundRect(x + 5 * mm, y + CH - 12 * mm, 28 * mm, 6 * mm, 3 * mm, stroke=0, fill=1)
        cv.setFillColor(self.negro)
        cv.setFont("Archivo", 6.5)
        cv.drawCentredString(x + 19 * mm, y + CH - 10 * mm, cuando)
        parrafo(cv, nombre.upper(), x + 5 * mm, y + CH - 32 * mm, CW - 10 * mm, 17 * mm, "Archivo", 22, 12,
                white, v="arriba", interl=1.0)
        bx, by, bw, bh = x + 4.5 * mm, y + 13 * mm, CW - 9 * mm, 34 * mm
        burbuja(cv, bx, by, bw, bh, white, cola="der")
        parrafo(cv, texto, bx + 4 * mm, by + 3 * mm, bw - 8 * mm, bh - 6 * mm, "PopSB", 10, 7,
                self.negro, interl=1.25)
        cv.setFillColor(white)
        cv.setFont("Archivo", 6.5)
        cv.drawCentredString(x + CW / 2, y + 4 * mm, "OPINÓLOGOS")

    def voto(self, cv, x, y):
        fondo(cv, x, y, HexColor("#00A862"))
        cv.setFillColor(white)
        cv.circle(x + CW / 2, y + CH / 2 + 8 * mm, 15 * mm, stroke=0, fill=1)
        cv.setFillColor(HexColor("#00A862"))
        cv.setFont("Sym", 40)
        cv.drawCentredString(x + CW / 2, y + CH / 2 + 2 * mm, "✔")
        cv.setFillColor(white)
        cv.setFont("Archivo", 22)
        cv.drawCentredString(x + CW / 2, y + CH / 2 - 18 * mm, "A FAVOR")

    def dorso(self, cv, x, y):
        fondo(cv, x, y, self.negro)
        bx, by, bw, bh = x + 5 * mm, y + CH / 2 - 9 * mm, CW - 10 * mm, 20 * mm
        burbuja(cv, bx, by, bw, bh, self.amarillo)
        cv.setFillColor(self.negro)
        cv.setFont("Archivo", 15.5)
        cv.drawCentredString(x + CW / 2, by + 7.5 * mm, "OPINÓLOGOS")
        cv.setFillColor(white)
        cv.setFont("PopSB", 7.5)
        cv.drawCentredString(x + CW / 2, by - 12 * mm, "Todos opinan. Pocos convencen.")
        cv.setFillColor(self.violeta)
        cv.setFont("Archivo", 7)
        cv.drawCentredString(x + CW / 2, y + 9 * mm, "ACCIÓN")


# ---------------- ESTILO C · MINIMAL ----------------
class Minimal:
    nombre = "C · Minimal"
    bajada = "Limpio y moderno: fondo blanco, mucho aire y un solo acento de color. Se siente premium."
    tinta = HexColor("#111111")
    gris = HexColor("#8C8C8C")
    niveles = [HexColor("#2F6FED"), HexColor("#F08A24"), HexColor("#D7263D")]
    violeta = HexColor("#6B4EE6")

    def tema(self, cv, x, y, t):
        nivel, texto, n = t
        col = self.niveles[nivel]
        fondo(cv, x, y, white)
        contorno(cv, x, y, HexColor("#E2E2E2"))
        cv.setFillColor(col)
        p = cv.beginPath()
        p.roundRect(x, y, CW, CH, R)
        cv.saveState()
        cv.clipPath(p, stroke=0, fill=0)
        cv.rect(x, y + CH - 2.5 * mm, CW, 2.5 * mm, stroke=0, fill=1)
        cv.restoreState()
        cv.setFont("PopM", 6.3)
        cv.setFillColor(col)
        cv.drawString(x + 6 * mm, y + CH - 10 * mm, NIVELES[nivel].lower())
        cv.setFillColor(self.gris)
        cv.drawRightString(x + CW - 6 * mm, y + CH - 10 * mm, f"{n:02d}a")
        parrafo(cv, texto, x + 6 * mm, y + 24 * mm, CW - 12 * mm, 46 * mm, "PopSB", 15.5, 10,
                self.tinta, v="arriba", interl=1.22)
        cv.setFont("PopR", 6.5)
        cv.setFillColor(self.tinta)
        cv.drawString(x + 6 * mm, y + 13 * mm, "a favor")
        cv.drawRightString(x + CW - 6 * mm, y + 13 * mm, "en contra")
        cv.setStrokeColor(HexColor("#DADADA"))
        cv.setLineWidth(0.5)
        cv.line(x + 17 * mm, y + 14.1 * mm, x + CW - 20 * mm, y + 14.1 * mm)
        cv.setFont("PopB", 6.3)
        cv.setFillColor(self.tinta)
        cv.drawString(x + 6 * mm, y + 5.5 * mm, "opinólogos")
        cv.setFillColor(col)
        cv.circle(x + 6 * mm + pdfmetrics.stringWidth("opinólogos", "PopB", 6.3) + 1.3 * mm,
                  y + 6.1 * mm, 0.8 * mm, stroke=0, fill=1)

    def accion(self, cv, x, y):
        nombre, cuando, texto = ACCION
        fondo(cv, x, y, white)
        contorno(cv, x, y, HexColor("#E2E2E2"))
        cv.setFont("PopM", 6.3)
        cv.setFillColor(self.violeta)
        cv.drawString(x + 6 * mm, y + CH - 10 * mm, "acción · " + cuando.lower())
        parrafo(cv, nombre, x + 6 * mm, y + CH - 30 * mm, CW - 12 * mm, 15 * mm, "PopB", 19, 12,
                self.tinta, v="arriba")
        cv.setFillColor(self.violeta)
        cv.rect(x + 6 * mm, y + CH - 33 * mm, 8 * mm, 0.9 * mm, stroke=0, fill=1)
        parrafo(cv, texto, x + 6 * mm, y + 14 * mm, CW - 12 * mm, 34 * mm, "PopR", 9.5, 7,
                self.tinta, v="arriba", interl=1.4)
        cv.setFont("PopB", 6.3)
        cv.setFillColor(self.tinta)
        cv.drawString(x + 6 * mm, y + 5.5 * mm, "opinólogos")

    def voto(self, cv, x, y):
        fondo(cv, x, y, HexColor("#1F9D5C"))
        cv.setFillColor(white)
        cv.setFont("PopB", 30)
        cv.drawString(x + 6 * mm, y + CH - 22 * mm, "a favor")
        cv.setFont("Sym", 70)
        cv.drawRightString(x + CW - 5 * mm, y + 8 * mm, "✔")
        cv.setFont("PopB", 6.3)
        cv.drawString(x + 6 * mm, y + 5.5 * mm, "opinólogos")

    def dorso(self, cv, x, y):
        fondo(cv, x, y, self.tinta)
        cv.setFillColor(white)
        cv.setFont("PopB", 17)
        w = pdfmetrics.stringWidth("opinólogos", "PopB", 17)
        x0 = x + (CW - w - 8 * mm) / 2
        cv.drawString(x0, y + CH / 2, "opinólogos")
        for i, col in enumerate(self.niveles):
            cv.setFillColor(col)
            cv.circle(x0 + w + 1.8 * mm + i * 2.6 * mm, y + CH / 2 + 0.9 * mm, 0.9 * mm,
                      stroke=0, fill=1)
        cv.setFillColor(HexColor("#9A9A9A"))
        cv.setFont("PopR", 7)
        cv.drawCentredString(x + CW / 2, y + CH / 2 - 7 * mm, "todos opinan. pocos convencen.")
        cv.setFillColor(self.violeta)
        cv.setFont("PopM", 6.3)
        cv.drawCentredString(x + CW / 2, y + 8 * mm, "acción")


def lamina(estilo, salida):
    W = 5 * CW + 6 * GAP
    H = CH + 46 * mm
    cv = canvas.Canvas(salida, pagesize=(W, H))
    cv.setFillColor(HexColor("#ECECEC"))
    cv.rect(0, 0, W, H, stroke=0, fill=1)
    cv.setFillColor(HexColor("#111111"))
    cv.setFont("PopB", 20)
    cv.drawString(GAP, H - 15 * mm, estilo.nombre)
    cv.setFont("PopR", 10)
    cv.setFillColor(HexColor("#444444"))
    cv.drawString(GAP, H - 22 * mm, estilo.bajada)
    y = 9 * mm
    etiquetas = ["Tema · Calentamiento", "Tema · Profundo", "Acción", "Voto", "Dorso (Acción)"]
    acciones = [lambda x: estilo.tema(cv, x, y, TEMA1), lambda x: estilo.tema(cv, x, y, TEMA2),
                lambda x: estilo.accion(cv, x, y), lambda x: estilo.voto(cv, x, y),
                lambda x: estilo.dorso(cv, x, y)]
    for i, (dib, et) in enumerate(zip(acciones, etiquetas)):
        x = GAP + i * (CW + GAP)
        dib(x)
        cv.setFont("PopM", 8)
        cv.setFillColor(HexColor("#666666"))
        cv.drawString(x, y + CH + 3 * mm, et)
    cv.showPage()
    cv.save()


if __name__ == "__main__":
    destino = sys.argv[1]
    for clase, archivo in ((Sobremesa, "estilo-a-sobremesa"), (Fiesta, "estilo-b-fiesta"),
                           (Minimal, "estilo-c-minimal")):
        lamina(clase(), f"{destino}/{archivo}.pdf")
        print("ok", archivo)
