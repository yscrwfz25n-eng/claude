"""Genera THE DATING LIST listo para imprenta: interior A5 de 60 páginas + tapa dura extendida.

Uso:  python3 citas/generar_libro.py
  -> citas/the-dating-list-interior.pdf   60 páginas A5 con 3 mm de sangrado (TrimBox marcado)
  -> citas/the-dating-list-tapa.pdf       tapa extendida: contratapa | lomo | tapa, con demasía de cartoné
  -> citas/libro-vista.png                vista previa de páginas clave

Interior pensado para papel ahuesado (bookcel) de 90-120 g, impreso en bordó y rojo:
el fondo del papel no se imprime. Solo la portadilla va a sangre en bordó.
"""
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
sys.path.insert(0, RAIZ)

import generar_pdf as base  # noqa: E402  (párrafos que se ajustan a la caja)
from maquetas import PH, PW, c, casilla  # noqa: E402  (fuentes, contenido y casillas)
from portadas_personalizadas import BORDO, logotipo  # noqa: E402  (logotipo THE / Dating / LIST)
from reportlab.lib.colors import HexColor  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.pdfbase import pdfmetrics  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402

SALIDA_INTERIOR = os.path.join(AQUI, "the-dating-list-interior.pdf")
SALIDA_TAPA = os.path.join(AQUI, "the-dating-list-tapa.pdf")
INSTAGRAM = "@oficina.grafica_"
QR = os.path.join(RAIZ, "imagenes", "qr-instagram-transparente.png")
FRASE = os.path.join(RAIZ, "imagenes", "frase-amor-beige.png")

SANGRADO = 3 * mm
INT, EXT, SUP, INF = 18 * mm, 13 * mm, 15 * mm, 15 * mm  # márgenes: interno (lomo), externo, arriba, abajo

TINTA = HexColor("#5C0F1E")
ROJO = HexColor("#C8102E")
LINEA = HexColor("#D6C3AE")
BEIGE = HexColor("#EFE3D0")

# Tapa dura: el cartón se forra con 15 mm de demasía que se dobla hacia adentro.
# El lomo depende del papel y la cantidad de hojas: confirmarlo con la imprenta.
DEMASIA = 15 * mm
LOMO = 10 * mm
CARTON = 3 * mm  # el cartón sobresale ~3 mm del interior en cada borde

CITAS = [(cat, t) for cat, lista in c.CATEGORIAS for t in lista]


# ---------- interior ----------

class Pagina:
    """Coordenadas de la página corte (sin sangrado) y márgenes espejados."""

    def __init__(self, numero):
        self.n = numero
        self.x0, self.y0 = SANGRADO, SANGRADO
        derecha = numero % 2 == 1  # la página 1 es impar y cae a la derecha
        self.izq = self.x0 + (INT if derecha else EXT)
        self.der = self.x0 + PW - (EXT if derecha else INT)
        self.arriba = self.y0 + PH - SUP
        self.abajo = self.y0 + INF
        self.ancho = self.der - self.izq
        self.cx = (self.izq + self.der) / 2


def folio(cv, p):
    cv.setFillColor(ROJO)
    cv.setFont("PopM", 7)
    cv.drawCentredString(p.cx, p.y0 + 7 * mm, str(p.n))


def titulo(cv, p, texto, y=None):
    y = p.arriba - 12 * mm if y is None else y
    cv.setFillColor(TINTA)
    cv.setFont("DMSerifIt", 26)
    cv.drawString(p.izq, y, texto)
    cv.setStrokeColor(ROJO)
    cv.setLineWidth(1)
    cv.line(p.izq, y - 3.5 * mm, p.izq + 10 * mm, y - 3.5 * mm)
    return y - 3.5 * mm


def renglon(cv, x1, x2, y):
    cv.setStrokeColor(LINEA)
    cv.setLineWidth(0.5)
    cv.line(x1, y, x2, y)


def etiqueta_campo(cv, x, y, texto, ancho_linea):
    cv.setFillColor(ROJO)
    cv.setFont("PopSB", 6.3)
    cv.drawString(x, y + 1.2 * mm, texto.upper())
    w = pdfmetrics.stringWidth(texto.upper(), "PopSB", 6.3) + 2 * mm
    renglon(cv, x + w, x + ancho_linea, y)


def portadilla(cv, p):
    cv.setFillColor(BORDO.fondo)
    cv.rect(0, 0, PW + 2 * SANGRADO, PH + 2 * SANGRADO, stroke=0, fill=1)
    cx = p.x0 + PW / 2
    logotipo(cv, cx, p.y0 + PH / 2 + 8 * mm, BORDO)
    cv.setFillColor(BORDO.tinta)
    cv.setFont("PopR", 8)
    cv.drawCentredString(cx, p.y0 + PH / 2 - 52 * mm, "100 citas para hacer juntos")


def como_usar(cv, p):
    y = titulo(cv, p, "cómo usar este libro") - 14 * mm
    pasos = [
        "Elijan una cita de la lista: en orden, al azar o la que tengan ganas.",
        "Háganla. Sin apuro: no hay fecha límite.",
        "Tilden la casilla en la lista y en su página.",
        "Completen la página de la cita: fecha, lugar, quién la organizó, "
        "lo mejor y una anécdota.",
        "Pónganle puntaje y decidan si la repetirían.",
    ]
    for i, paso in enumerate(pasos, 1):
        cv.setFillColor(ROJO)
        cv.setFont("DMSerif", 18)
        cv.drawString(p.izq, y - 5 * mm, str(i))
        base.parrafo(cv, paso, p.izq + 10 * mm, y - 16 * mm, p.ancho - 10 * mm, 16 * mm, "PopR", 9.5, 8,
                     color=TINTA, interlineado=1.4)
        y -= 21 * mm
    base.parrafo(cv, "Cuando completen las 100, este libro va a ser la historia de ustedes.",
                 p.izq, p.abajo + 14 * mm, p.ancho, 16 * mm, "DMSerifIt", 15, 11, color=TINTA, interlineado=1.2)
    folio(cv, p)


def de_quien(cv, p):
    cx = p.cx
    cv.setFillColor(TINTA)
    cv.setFont("DMSerifIt", 24)
    cv.drawCentredString(cx, p.y0 + PH * 0.70, "Este libro es de")
    y = p.y0 + PH * 0.70 - 22 * mm
    renglon(cv, cx - 45 * mm, cx + 45 * mm, y)
    cv.setFont("Script", 30)
    cv.setFillColor(ROJO)
    cv.drawCentredString(cx, y - 13 * mm, "&")
    renglon(cv, cx - 45 * mm, cx + 45 * mm, y - 26 * mm)
    y -= 52 * mm
    for texto in ("Empezamos la lista el", "La terminamos el"):
        cv.setFillColor(TINTA)
        cv.setFont("PopR", 8.5)
        cv.drawCentredString(cx, y, texto)
        renglon(cv, cx - 25 * mm, cx + 25 * mm, y - 10 * mm)
        y -= 24 * mm
    folio(cv, p)


def paginas_lista():
    """Reparte las 100 citas (con títulos de categoría) en páginas de lista."""
    items = []
    for cat, lista in c.CATEGORIAS:
        items.append(("cat", cat))
        items += [("cita", t) for t in lista]
    paginas, actual, alto = [], [], 0
    disponible = [PH - SUP - INF - 30 * mm] + [PH - SUP - INF - 6 * mm] * 10
    for tipo, texto in items:
        h = 8.5 * mm if tipo == "cat" else 5.75 * mm
        if alto + h > disponible[len(paginas)] or (tipo == "cat" and alto + h + 5.75 * mm > disponible[len(paginas)]):
            paginas.append(actual)
            actual, alto = [], 0
        actual.append((tipo, texto))
        alto += h
    paginas.append(actual)
    return paginas


def lista(cv, p, items, primera, numero_inicial):
    y = (titulo(cv, p, "la lista") - 8 * mm) if primera else p.arriba - 2 * mm
    if primera:
        cv.setFillColor(TINTA)
        cv.setFont("PopR", 8)
        cv.drawString(p.izq, y, "Tilden cada cita cuando la hagan.")
        y -= 10 * mm
    n = numero_inicial
    for tipo, texto in items:
        if tipo == "cat":
            y -= 2 * mm
            cv.setFillColor(ROJO)
            cv.setFont("PopSB", 7)
            cv.drawString(p.izq, y, texto.upper())
            y -= 6.5 * mm
            continue
        n += 1
        casilla(cv, p.izq, y - 0.7 * mm, 3.4 * mm, TINTA, grosor=0.6)
        cv.setFillColor(ROJO)
        cv.setFont("PopM", 6.5)
        cv.drawRightString(p.izq + 11 * mm, y, f"{n:02d}")
        cv.setFillColor(TINTA)
        cv.setFont("PopR", 7.8)
        cv.drawString(p.izq + 13.5 * mm, y, texto)
        y -= 5.75 * mm
    folio(cv, p)
    return n


def bloque_cita(cv, p, top, numero, categoria, texto):
    x, ancho = p.izq, p.ancho
    casilla(cv, x, top - 7 * mm, 6 * mm, TINTA, grosor=0.9)
    cv.setFillColor(ROJO)
    cv.setFont("PopSB", 7)
    cv.drawString(x + 9 * mm, top - 2.5 * mm, f"CITA Nº {numero:02d}")
    cv.setFillColor(LINEA)
    cv.setFont("PopM", 6.3)
    cv.drawRightString(x + ancho, top - 2.5 * mm, categoria.upper())
    base.parrafo(cv, texto, x + 9 * mm, top - 18 * mm, ancho - 9 * mm, 13.5 * mm, "DMSerif", 15, 10.5,
                 color=TINTA, interlineado=1.1)
    fila = top - 27 * mm
    mitad = ancho / 2
    etiqueta_campo(cv, x, fila, "Fecha", mitad - 4 * mm)
    etiqueta_campo(cv, x + mitad + 2 * mm, fila, "Lugar", mitad - 2 * mm)
    fila -= 9 * mm
    etiqueta_campo(cv, x, fila, "La organizó", mitad - 4 * mm)
    cv.setFillColor(ROJO)
    cv.setFont("PopSB", 6.3)
    cv.drawString(x + mitad + 2 * mm, fila + 1.2 * mm, "PUNTAJE")
    cv.setFillColor(TINTA)
    cv.setFont("Sym", 10)
    cv.drawString(x + mitad + 16 * mm, fila + 0.6 * mm, "♡ ♡ ♡ ♡ ♡")
    fila -= 9 * mm
    etiqueta_campo(cv, x, fila, "Lo mejor", ancho)
    renglon(cv, x, x + ancho, fila - 7 * mm)
    fila -= 15 * mm
    etiqueta_campo(cv, x, fila, "Una anécdota", ancho)
    renglon(cv, x, x + ancho, fila - 7 * mm)
    renglon(cv, x, x + ancho, fila - 14 * mm)
    fila -= 22 * mm
    cv.setFillColor(ROJO)
    cv.setFont("PopSB", 6.3)
    cv.drawString(x, fila + 1.2 * mm, "¿LA REPETIRÍAN?")
    cv.setFillColor(TINTA)
    cv.setFont("PopR", 7.5)
    for i, op in enumerate(("sí", "no")):
        ox = x + 26 * mm + i * 14 * mm
        cv.setStrokeColor(TINTA)
        cv.setLineWidth(0.6)
        cv.circle(ox, fila + 2 * mm, 1.5 * mm, stroke=1, fill=0)
        cv.drawString(ox + 2.8 * mm, fila + 1 * mm, op)


def pagina_citas(cv, p, i):
    """Dos citas por página: la i y la i+1 (base 0)."""
    mitad = p.y0 + PH / 2
    for k, top in ((0, p.arriba), (1, mitad - 4 * mm)):
        cat, texto = CITAS[i + k]
        bloque_cita(cv, p, top, i + k + 1, cat, texto)
    cv.setStrokeColor(ROJO)
    cv.setLineWidth(0.5)
    cv.setDash(1, 2)
    cv.line(p.izq, mitad + 3 * mm, p.der, mitad + 3 * mm)
    cv.setDash()
    folio(cv, p)


def final(cv, p):
    cv.setFillColor(ROJO)
    cv.setFont("PopSB", 8)
    cv.drawCentredString(p.cx, p.arriba - 6 * mm, "100 DE 100")
    cv.setFillColor(TINTA)
    cv.setFont("DMSerifIt", 30)
    cv.drawCentredString(p.cx, p.arriba - 22 * mm, "Lo lograron.")
    y = p.arriba - 40 * mm
    for _ in range(2):
        cv.setFillColor(ROJO)
        cv.setFont("PopSB", 6.3)
        cv.drawString(p.izq, y + 1.2 * mm, "DE")
        renglon(cv, p.izq + 6 * mm, p.izq + p.ancho / 2 - 4 * mm, y)
        cv.drawString(p.izq + p.ancho / 2, y + 1.2 * mm, "PARA")
        renglon(cv, p.izq + p.ancho / 2 + 9 * mm, p.der, y)
        for k in range(1, 7):
            renglon(cv, p.izq, p.der, y - k * 7.5 * mm)
        y -= 72 * mm
    folio(cv, p)


def creditos(cv, p):
    cv.setFillColor(TINTA)
    cv.setFont("DMSerifIt", 12)
    cv.drawCentredString(p.cx, p.abajo + 22 * mm, "The Dating List")
    cv.setFont("PopR", 7)
    cv.drawCentredString(p.cx, p.abajo + 16 * mm, f"diseñado por {INSTAGRAM}")


def interior():
    W, H = PW + 2 * SANGRADO, PH + 2 * SANGRADO
    cv = canvas.Canvas(SALIDA_INTERIOR, pagesize=(W, H))
    cv.setTitle("The Dating List – interior")
    cv.setAuthor(INSTAGRAM)
    paginas = [portadilla, como_usar, de_quien]
    listas = paginas_lista()
    inicio = 0
    for j, items in enumerate(listas):
        def dib(cv, p, items=items, j=j, ini=inicio):
            lista(cv, p, items, j == 0, ini)
        paginas.append(dib)
        inicio += sum(1 for t, _ in items if t == "cita")
    for i in range(0, 100, 2):
        paginas.append(lambda cv, p, i=i: pagina_citas(cv, p, i))
    paginas += [final, creditos]
    while len(paginas) % 4:  # pliegos completos: se agregan páginas en blanco antes de los créditos
        paginas.insert(-1, lambda cv, p: None)
    for n, dibujar in enumerate(paginas, 1):
        cv.setTrimBox((SANGRADO, SANGRADO, SANGRADO + PW, SANGRADO + PH))
        cv.setBleedBox((0, 0, W, H))
        dibujar(cv, Pagina(n))
        cv.showPage()
    cv.save()
    return len(paginas), len(listas)


# ---------- tapa extendida ----------

def tapa():
    tw, th = PW + CARTON, PH + 2 * CARTON  # cada tapa de cartón
    W = 2 * DEMASIA + 2 * tw + LOMO
    H = 2 * DEMASIA + th
    cv = canvas.Canvas(SALIDA_TAPA, pagesize=(W, H))
    cv.setTitle("The Dating List – tapa extendida")
    cv.setAuthor(INSTAGRAM)
    cv.setFillColor(BORDO.fondo)
    cv.rect(0, 0, W, H, stroke=0, fill=1)
    x_contra, x_lomo, x_tapa = DEMASIA, DEMASIA + tw, DEMASIA + tw + LOMO
    y0 = DEMASIA

    # «100» tono sobre tono en la tapa: sangra hacia abajo y hacia el borde
    cv.saveState()
    pth = cv.beginPath()
    pth.rect(x_tapa, 0, tw + DEMASIA, H)
    cv.clipPath(pth, stroke=0, fill=0)
    t = cv.beginText()
    t.setFont("DMSerif", 250)
    t.setHorizScale(68)
    t.setFillColor(BORDO.sombra)
    t.setTextOrigin(x_tapa + 38 * mm, y0 - 12 * mm)
    t.textOut("100")
    cv.drawText(t)
    cv.restoreState()

    # tapa
    cx = x_tapa + tw / 2
    cv.setFillColor(BORDO.tinta)
    cv.setFont("DMSerif", 11)
    cv.drawCentredString(cx, y0 + th - 24 * mm, INSTAGRAM)
    logotipo(cv, cx, y0 + th / 2 + 6 * mm, BORDO)
    cv.setFillColor(BORDO.tinta)
    cv.setFont("PopR", 7.5)
    cv.drawCentredString(cx, y0 + 52 * mm, "100 citas para hacer juntos")

    # lomo
    cv.saveState()
    cv.translate(x_lomo + LOMO / 2, y0 + th / 2)
    cv.rotate(-90)
    cv.setFont("DMSerif", 9)
    cv.drawCentredString(0, -1.2 * mm, "THE DATING LIST")
    cv.restoreState()

    # contratapa: la frase manuscrita y el QR de Instagram
    ccx = x_contra + tw / 2
    fw = 62 * mm
    fh = fw * 1172 / 705
    cv.drawImage(FRASE, ccx - fw / 2, y0 + th - 22 * mm - fh, fw, fh, mask="auto")
    qw = 24 * mm
    qh = qw * 1700 / 1393
    qx, qy = ccx - qw / 2, y0 + 22 * mm
    pad = 2.5 * mm
    cv.setFillColor(BEIGE)
    cv.roundRect(qx - pad, qy - pad, qw + 2 * pad, qh + 2 * pad, 2 * mm, stroke=0, fill=1)
    cv.drawImage(QR, qx, qy, qw, qh, mask="auto")
    cv.setFillColor(BORDO.tinta)
    cv.setFont("DMSerifIt", 10)
    cv.drawCentredString(ccx, qy + qh + pad + 5 * mm, "seguinos en Instagram")

    # guías: corte (borde de la demasía), cartón y lomo, fuera del arte
    cv.setStrokeColor(HexColor("#E6007E"))
    cv.setLineWidth(0.4)
    cv.setDash(2, 2)
    for x in (x_contra, x_lomo, x_tapa, x_tapa + tw):
        cv.line(x, 0, x, 6 * mm)
        cv.line(x, H - 6 * mm, x, H)
    for y in (y0, y0 + th):
        cv.line(0, y, 6 * mm, y)
        cv.line(W - 6 * mm, y, W, y)
    cv.setDash()
    cv.showPage()
    cv.save()
    return W, H


# ---------- vista previa ----------

def vista_previa(total):
    tmp = os.path.join(AQUI, "_vista")
    os.makedirs(tmp, exist_ok=True)
    elegidas = [1, 2, 3, 4, 8, total - 2]  # total - 2: página final «Lo lograron»
    for n in elegidas:
        subprocess.run(["pdftoppm", "-r", "60", "-png", "-singlefile", "-f", str(n), "-l", str(n),
                        SALIDA_INTERIOR, os.path.join(tmp, f"p{n:02d}")], check=True)
    subprocess.run(["pdftoppm", "-r", "45", "-png", "-singlefile", SALIDA_TAPA, os.path.join(tmp, "tapa")], check=True)
    from PIL import Image
    pags = [Image.open(os.path.join(tmp, f"p{n:02d}.png")) for n in elegidas]
    tapa_img = Image.open(os.path.join(tmp, "tapa.png"))
    w, h = pags[0].size
    gap = 16
    W = max(len(pags) * (w + gap) + gap, tapa_img.width + 2 * gap)
    H = h + tapa_img.height + 3 * gap
    out = Image.new("RGB", (W, H), "#ECE6DC")
    out.paste(tapa_img, ((W - tapa_img.width) // 2, gap))
    for i, im in enumerate(pags):
        out.paste(im, (gap + i * (w + gap), tapa_img.height + 2 * gap))
    out.save(os.path.join(AQUI, "libro-vista.png"))
    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))
    os.rmdir(tmp)


if __name__ == "__main__":
    total, n_listas = interior()
    W, H = tapa()
    vista_previa(total)
    print(f"{os.path.relpath(SALIDA_INTERIOR)}: {total} páginas A5 ({n_listas} de lista)")
    print(f"{os.path.relpath(SALIDA_TAPA)}: {W / mm:.0f} x {H / mm:.0f} mm (lomo {LOMO / mm:.0f} mm)")
