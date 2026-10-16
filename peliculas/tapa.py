"""Tapa de THE WATCH LIST: colorida, con objetos de cine y series alrededor del logotipo.

Uso:  python3 peliculas/tapa.py  ->  peliculas/tapa.png (maqueta del cuaderno con elástico y cinta)

Ilustraciones vectoriales propias (sin afiches ni logos de películas, que tienen derechos).
"""
import math
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "citas"))

from portadas_personalizadas import PH, PW, Tapa, cuaderno, elastico, logotipo  # noqa: E402
from reportlab.lib.colors import HexColor  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402

INSTAGRAM = "@oficina.grafica_"
COBALTO = Tapa("#24408E", "#FBEFD9", "#2C4A9C", "#141414", "#2C4A9C")
ROJO, AMARILLO, ROSA, MENTA = HexColor("#E63946"), HexColor("#F7C548"), HexColor("#F48FB1"), HexColor("#5CC8B0")
CREMA, NEGRO, CIAN = HexColor("#FBEFD9"), HexColor("#141414"), HexColor("#4FC3F7")


def girar(cv, cx, cy, angulo):
    cv.saveState()
    cv.translate(cx, cy)
    cv.rotate(angulo)


def estrella(cv, cx, cy, r, color):
    p = cv.beginPath()
    for i in range(10):
        a = math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        (p.moveTo if i == 0 else p.lineTo)(cx + rr * math.cos(a), cy + rr * math.sin(a))
    p.close()
    cv.setFillColor(color)
    cv.drawPath(p, stroke=0, fill=1)


def pochoclos(cv, cx, cy):
    """Balde de pochoclos a rayas, con pochoclos asomando."""
    girar(cv, cx, cy, 6)
    w_ab, w_ar, h = 18 * mm, 26 * mm, 28 * mm
    # pochoclos detrás del borde superior
    for dx, dy, r in ((-9, 2, 4.2), (-3, 5, 4.6), (4, 4, 4.4), (10, 1.5, 4), (0, 0, 4), (-6, -1, 3.6),
                      (7, -0.5, 3.6)):
        cv.setFillColor(AMARILLO)
        cv.circle(dx * mm + 0.5 * mm, h / 2 + dy * mm - 0.6 * mm, r * mm, stroke=0, fill=1)
        cv.setFillColor(CREMA)
        cv.circle(dx * mm, h / 2 + dy * mm, r * mm * 0.92, stroke=0, fill=1)
    # balde: trapecio con rayas verticales
    p = cv.beginPath()
    p.moveTo(-w_ab / 2, -h / 2)
    p.lineTo(w_ab / 2, -h / 2)
    p.lineTo(w_ar / 2, h / 2)
    p.lineTo(-w_ar / 2, h / 2)
    p.close()
    cv.saveState()
    cv.clipPath(p, stroke=0, fill=0)
    n = 6
    for i in range(n):
        cv.setFillColor(ROJO if i % 2 == 0 else CREMA)
        x0 = -w_ar / 2 + i * w_ar / n
        cv.rect(x0, -h / 2, w_ar / n + 0.2, h, stroke=0, fill=1)
    cv.restoreState()
    cv.setFillColor(ROJO)
    cv.rect(-w_ar / 2 - 0.8 * mm, h / 2 - 3 * mm, w_ar + 1.6 * mm, 3.4 * mm, stroke=0, fill=1)
    cv.restoreState()


def claqueta(cv, cx, cy):
    girar(cv, cx, cy, -10)
    w, h = 34 * mm, 22 * mm
    cv.setFillColor(NEGRO)
    cv.roundRect(-w / 2, -h / 2, w, h, 1.2 * mm, stroke=0, fill=1)
    cv.setStrokeColor(CREMA)
    cv.setLineWidth(0.6)
    for k in (1, 2):
        y = -h / 2 + k * h / 3
        cv.line(-w / 2 + 2 * mm, y, w / 2 - 2 * mm, y)
    cv.line(0, -h / 2 + 2 * mm, 0, -h / 2 + h / 3)
    cv.setFillColor(CREMA)
    cv.setFont("PopSB", 5)
    cv.drawString(-w / 2 + 2.5 * mm, h / 2 - 5.5 * mm, "ESCENA  1")
    cv.drawString(-w / 2 + 2.5 * mm, -h / 2 + h / 3 + 2 * mm, "TOMA  100")
    # barra superior abierta, con rayas diagonales
    cv.saveState()
    cv.translate(-w / 2, h / 2 - 0.3 * mm)  # bisagra pegada al cuerpo
    cv.rotate(11)
    bw, bh = w, 6 * mm
    p = cv.beginPath()
    p.rect(0, 0, bw, bh)
    cv.saveState()
    cv.clipPath(p, stroke=0, fill=0)
    cv.setFillColor(NEGRO)
    cv.rect(0, 0, bw, bh, stroke=0, fill=1)
    cv.setFillColor(CREMA)
    for i in range(-1, 8):
        q = cv.beginPath()
        x0 = i * 5.5 * mm
        q.moveTo(x0, 0)
        q.lineTo(x0 + 2.8 * mm, 0)
        q.lineTo(x0 + 2.8 * mm + bh, bh)
        q.lineTo(x0 + bh, bh)
        q.close()
        cv.drawPath(q, stroke=0, fill=1)
    cv.restoreState()
    cv.restoreState()
    cv.setFillColor(HexColor("#9A9A9A"))
    cv.circle(-w / 2 + 1.2 * mm, h / 2 + 0.6 * mm, 1.1 * mm, stroke=0, fill=1)  # perno de la bisagra
    cv.restoreState()


def rollo(cv, cx, cy, r, fondo):
    cv.setFillColor(AMARILLO)
    cv.circle(cx, cy, r, stroke=0, fill=1)
    cv.setFillColor(fondo)
    for i in range(5):
        a = math.radians(90 + i * 72)
        cv.circle(cx + r * 0.55 * math.cos(a), cy + r * 0.55 * math.sin(a), r * 0.22, stroke=0, fill=1)
    cv.circle(cx, cy, r * 0.12, stroke=0, fill=1)
    cv.setStrokeColor(HexColor("#D9A62E"))
    cv.setLineWidth(1)
    cv.circle(cx, cy, r * 0.93, stroke=1, fill=0)


def entrada(cv, cx, cy, fondo):
    girar(cv, cx, cy, 78)
    w, h = 30 * mm, 13 * mm
    cv.setFillColor(ROSA)
    cv.roundRect(-w / 2, -h / 2, w, h, 1.5 * mm, stroke=0, fill=1)
    cv.setFillColor(fondo)
    cv.circle(-w / 2, 0, 2.2 * mm, stroke=0, fill=1)
    cv.circle(w / 2, 0, 2.2 * mm, stroke=0, fill=1)
    cv.setStrokeColor(CREMA)
    cv.setLineWidth(0.5)
    cv.setDash(1, 1.2)
    cv.line(w / 2 - 8 * mm, -h / 2 + 1 * mm, w / 2 - 8 * mm, h / 2 - 1 * mm)
    cv.setDash()
    cv.setFillColor(CREMA)
    cv.setFont("PopB", 5.5)
    cv.drawCentredString(-4 * mm, 0.6 * mm, "ADMIT ONE")
    cv.setFont("PopM", 3.6)
    cv.drawCentredString(-4 * mm, -2.6 * mm, "Nº 001")
    cv.restoreState()


def anteojos_3d(cv, cx, cy):
    girar(cv, cx, cy, 8)
    lw, lh = 11 * mm, 7.5 * mm
    cv.setFillColor(CREMA)
    cv.roundRect(-lw - 2.5 * mm, -lh / 2 - 1.2 * mm, 2 * lw + 5 * mm, lh + 2.4 * mm, 2 * mm, stroke=0, fill=1)
    cv.setFillColor(ROJO)
    cv.roundRect(-lw - 1.2 * mm, -lh / 2, lw, lh, 1.4 * mm, stroke=0, fill=1)
    cv.setFillColor(CIAN)
    cv.roundRect(1.2 * mm, -lh / 2, lw, lh, 1.4 * mm, stroke=0, fill=1)
    cv.setStrokeColor(CREMA)
    cv.setLineWidth(2)
    cv.line(-lw - 2.5 * mm, lh / 2, -lw - 7 * mm, lh / 2 + 2.5 * mm)
    cv.line(lw + 2.5 * mm, lh / 2, lw + 7 * mm, lh / 2 + 2.5 * mm)
    cv.restoreState()


def tele(cv, cx, cy):
    """Tele retro, por las series."""
    girar(cv, cx, cy, -5)
    w, h = 30 * mm, 23 * mm
    cv.setStrokeColor(CREMA)
    cv.setLineWidth(1.2)
    cv.line(0, h / 2, -6 * mm, h / 2 + 9 * mm)
    cv.line(0, h / 2, 7 * mm, h / 2 + 8 * mm)
    cv.setFillColor(CREMA)
    cv.circle(-6 * mm, h / 2 + 9 * mm, 1 * mm, stroke=0, fill=1)
    cv.circle(7 * mm, h / 2 + 8 * mm, 1 * mm, stroke=0, fill=1)
    cv.setFillColor(MENTA)
    cv.roundRect(-w / 2, -h / 2, w, h, 3 * mm, stroke=0, fill=1)
    cv.setFillColor(NEGRO)
    cv.roundRect(-w / 2 + 2.5 * mm, -h / 2 + 2.5 * mm, w - 11 * mm, h - 5 * mm, 2.5 * mm, stroke=0, fill=1)
    estrella(cv, -w / 2 + 2.5 * mm + (w - 11 * mm) / 2, 0, 4 * mm, AMARILLO)
    cv.setFillColor(CREMA)
    cv.circle(w / 2 - 4.2 * mm, h / 2 - 6 * mm, 1.6 * mm, stroke=0, fill=1)
    cv.circle(w / 2 - 4.2 * mm, h / 2 - 11 * mm, 1.6 * mm, stroke=0, fill=1)
    cv.setFillColor(NEGRO)
    cv.rect(-w / 2 + 5 * mm, -h / 2 - 2.5 * mm, 2 * mm, 2.5 * mm, stroke=0, fill=1)
    cv.rect(w / 2 - 7 * mm, -h / 2 - 2.5 * mm, 2 * mm, 2.5 * mm, stroke=0, fill=1)
    cv.restoreState()


def tira_de_pelicula(cv, x0, y0, largo, angulo):
    girar(cv, x0, y0, angulo)
    h = 13 * mm
    cv.setFillColor(NEGRO)
    cv.rect(0, -h / 2, largo, h, stroke=0, fill=1)
    cv.setFillColor(CREMA)
    paso = 4 * mm
    for i in range(int(largo / paso)):
        cv.roundRect(i * paso + 1 * mm, h / 2 - 2.6 * mm, 2 * mm, 1.6 * mm, 0.4 * mm, stroke=0, fill=1)
        cv.roundRect(i * paso + 1 * mm, -h / 2 + 1 * mm, 2 * mm, 1.6 * mm, 0.4 * mm, stroke=0, fill=1)
    colores = (ROSA, AMARILLO, MENTA, ROJO)
    cuadro = 11 * mm
    for i in range(int(largo / (cuadro + 1.5 * mm))):
        cv.setFillColor(colores[i % 4])
        cv.rect(i * (cuadro + 1.5 * mm) + 1 * mm, -3.6 * mm, cuadro, 7.2 * mm, stroke=0, fill=1)
    cv.restoreState()


def trofeo(cv, cx, cy):
    """Trofeo dorado genérico con una estrella (no la estatuilla del Oscar, que es marca registrada)."""
    oro, sombra = HexColor("#F2C14E"), HexColor("#D49B2A")
    cv.setFillColor(sombra)
    cv.rect(cx - 7 * mm, cy - 16 * mm, 14 * mm, 4 * mm, stroke=0, fill=1)  # base
    cv.setFillColor(NEGRO)
    cv.rect(cx - 5.5 * mm, cy - 12 * mm, 11 * mm, 3.5 * mm, stroke=0, fill=1)
    cv.setFillColor(oro)
    cv.rect(cx - 1.4 * mm, cy - 8.5 * mm, 2.8 * mm, 5 * mm, stroke=0, fill=1)  # pie
    p = cv.beginPath()  # copa
    p.moveTo(cx - 8 * mm, cy + 8 * mm)
    p.lineTo(cx + 8 * mm, cy + 8 * mm)
    p.curveTo(cx + 8 * mm, cy - 2 * mm, cx + 3 * mm, cy - 4 * mm, cx, cy - 4 * mm)
    p.curveTo(cx - 3 * mm, cy - 4 * mm, cx - 8 * mm, cy - 2 * mm, cx - 8 * mm, cy + 8 * mm)
    p.close()
    cv.drawPath(p, stroke=0, fill=1)
    cv.setStrokeColor(oro)
    cv.setLineWidth(1.6)
    cv.arc(cx - 11.5 * mm, cy, cx - 5 * mm, cy + 7 * mm, 90, 180)  # asas
    cv.arc(cx + 5 * mm, cy, cx + 11.5 * mm, cy + 7 * mm, -90, 180)
    estrella(cv, cx, cy + 13.5 * mm, 4.5 * mm, oro)
    estrella(cv, cx, cy + 2.5 * mm, 2.6 * mm, sombra)


NOCHE = Tapa("#1E2A5A", "#FBEFD9", "#26346B", "#141414", "#26346B")
CARTEL = Tapa("#FBEFD9", "#B3122E", "#FBEFD9", "#141414", "#FBEFD9")  # tablero crema, letras rojas
ROJO_CARTEL, FOCO = HexColor("#C8102E"), HexColor("#FFD86B")


def foco(cv, cx, cy, r=1.25 * mm):
    cv.setFillColor(FOCO, alpha=0.28)
    cv.circle(cx, cy, r * 2.1, stroke=0, fill=1)
    cv.setFillColor(FOCO, alpha=1)
    cv.circle(cx, cy, r, stroke=0, fill=1)
    cv.setFillColor(HexColor("#FFFFFF"), alpha=0.8)
    cv.circle(cx - r * 0.3, cy + r * 0.3, r * 0.35, stroke=0, fill=1)
    cv.setFillColor(HexColor("#FFFFFF"), alpha=1)


def focos_en_rect(cv, x1, y1, x2, y2, paso=5.6 * mm):
    for xa, ya, xb, yb in ((x1, y1, x2, y1), (x2, y1, x2, y2), (x2, y2, x1, y2), (x1, y2, x1, y1)):
        largo = math.hypot(xb - xa, yb - ya)
        n = max(1, round(largo / paso))
        for i in range(n):
            f = i / n
            foco(cv, xa + (xb - xa) * f, ya + (yb - ya) * f)


def letrero(cv, cx, y, filas):
    """Tablero de letras sueltas, como las marquesinas de los cines viejos."""
    tw, th, sep = 6.4 * mm, 8 * mm, 0.9 * mm
    ancho = max(len(f) for f in filas) * (tw + sep) + 5 * mm
    alto = len(filas) * (th + 2 * mm) + 3 * mm
    cv.setFillColor(NEGRO)
    cv.roundRect(cx - ancho / 2, y, ancho, alto, 1.5 * mm, stroke=0, fill=1)
    for k, fila in enumerate(filas):
        fy = y + alto - 2.5 * mm - (k + 1) * th - k * 2 * mm
        x0 = cx - (len(fila) * (tw + sep) - sep) / 2
        for i, ch in enumerate(fila):
            if ch == " ":
                continue
            girar(cv, x0 + i * (tw + sep) + tw / 2, fy + th / 2, (-1.5, 1, -0.5, 2, 0)[(i + k) % 5])
            cv.setFillColor(CREMA)
            cv.rect(-tw / 2, -th / 2, tw, th, stroke=0, fill=1)
            cv.setFillColor(NEGRO)
            cv.setFont("PopB", 13)
            cv.drawCentredString(0, -th / 2 + 1.9 * mm, ch)
            cv.restoreState()


def marquesina(cv, cx, y_base, ancho, alto):
    x1, x2, y1, y2 = cx - ancho / 2, cx + ancho / 2, y_base, y_base + alto
    # cresta semicircular con «EN CARTELERA»
    r = 26 * mm
    cv.setFillColor(ROJO_CARTEL)
    cv.wedge(cx - r, y2 - r, cx + r, y2 + r, 0, 180, stroke=0, fill=1)
    for i in range(11):
        a = math.radians(8 + i * 16.4)
        foco(cv, cx + (r - 3 * mm) * math.cos(a), y2 + (r - 3 * mm) * math.sin(a))
    cv.setFillColor(FOCO)
    cv.setFont("PopB", 8.5)
    cv.drawCentredString(cx, y2 + 9 * mm, "EN CARTELERA")
    estrella(cv, cx, y2 + 17 * mm, 3.2 * mm, FOCO)
    # marco rojo con focos y tablero crema
    cv.setFillColor(ROJO_CARTEL)
    cv.roundRect(x1, y1, ancho, alto, 2.5 * mm, stroke=0, fill=1)
    focos_en_rect(cv, x1 + 3 * mm, y1 + 3 * mm, x2 - 3 * mm, y2 - 3 * mm)
    cv.setFillColor(CREMA)
    cv.roundRect(x1 + 6.5 * mm, y1 + 6.5 * mm, ancho - 13 * mm, alto - 13 * mm, 1.5 * mm, stroke=0, fill=1)
    cv.setStrokeColor(ROJO_CARTEL)
    cv.setLineWidth(0.6)
    cv.roundRect(x1 + 8.5 * mm, y1 + 8.5 * mm, ancho - 17 * mm, alto - 17 * mm, 1 * mm, stroke=1, fill=0)


def tapa(cv, x, y, t=NOCHE):
    cuaderno(cv, x, y, t)
    cx = x + 68 * mm  # centro del área libre a la izquierda del elástico
    cv.saveState()
    p = cv.beginPath()
    p.roundRect(x, y, PW, PH, 3 * mm)
    cv.clipPath(p, stroke=0, fill=0)
    # rayos de luz suaves detrás del cartel
    for i in range(9):
        a1, a2 = math.radians(i * 40), math.radians(i * 40 + 14)
        q = cv.beginPath()
        q.moveTo(cx, y + 132 * mm)
        q.lineTo(cx + 220 * mm * math.cos(a1), y + 132 * mm + 220 * mm * math.sin(a1))
        q.lineTo(cx + 220 * mm * math.cos(a2), y + 132 * mm + 220 * mm * math.sin(a2))
        q.close()
        cv.setFillColor(HexColor("#FFFFFF"), alpha=0.035)
        cv.drawPath(q, stroke=0, fill=1)
    cv.setFillColor(HexColor("#FFFFFF"), alpha=1)
    for ex, ey, r in ((12, 196, 1.6), (124, 196, 2), (10, 120, 1.4), (126, 112, 1.6), (8, 86, 1.8),
                      (122, 70, 1.4)):
        estrella(cv, x + ex * mm, y + ey * mm, r * mm, AMARILLO)
    tira_de_pelicula(cv, x - 5 * mm, y + 9 * mm, 170 * mm, 0)
    marquesina(cv, cx, y + 92 * mm, 112 * mm, 78 * mm)
    logotipo(cv, cx, y + 128 * mm, CARTEL, escala=0.72, palabra="Watch")
    letrero(cv, cx, y + 60 * mm, ["100 PELÍCULAS", "Y SERIES"])
    pochoclos(cv, x + 22 * mm, y + 36 * mm)
    trofeo(cv, x + 48 * mm, y + 37 * mm)
    claqueta(cv, x + 82 * mm, y + 33 * mm)
    tele(cv, x + 114 * mm, y + 33 * mm)
    cv.restoreState()
    cv.setFillColor(t.tinta)
    cv.setFont("DMSerif", 9.5)
    cv.drawCentredString(cx, y + PH - 10 * mm, INSTAGRAM)
    elastico(cv, x, y, t)


def main():
    m = 16 * mm
    pdf = os.path.join(AQUI, "tapa.pdf")
    cv = canvas.Canvas(pdf, pagesize=(PW + 2 * m, PH + 2 * m))
    cv.setFillColor(HexColor("#F3ECE2"))
    cv.rect(0, 0, PW + 2 * m, PH + 2 * m, stroke=0, fill=1)
    tapa(cv, m, m + 4 * mm)
    cv.showPage()
    cv.save()
    subprocess.run(["pdftoppm", "-r", "150", "-png", "-singlefile", pdf, os.path.join(AQUI, "tapa")], check=True)
    os.remove(pdf)
    print("ok tapa.png")


if __name__ == "__main__":
    main()
