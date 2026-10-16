"""Arma el reglamento como librito A5 y el archivo único para la imprenta.

Uso:  python3 generar_reglamento.py   (antes correr generar_pdf.py)
  ->  reglamento-librito-a5.pdf        páginas A5 en orden de lectura (tapa ... contratapa)
  ->  reglamento-librito-imprimir.pdf  hojas A4 armadas para doble faz, doblar y abrochar
  ->  opinologos-muestra-imprenta.pdf  cartas + librito, todo doble faz por el borde largo

Soporta el Markdown que usa REGLAMENTO.md: títulos ##/###, párrafos, listas,
citas (>), tablas y **negrita**.
"""
import io
import re

from pypdf import PageObject, PdfReader, PdfWriter, Transformation
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4, A5
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.platypus import (KeepTogether, ListFlowable, ListItem, PageBreak, Paragraph,
                                SimpleDocTemplate, Table, TableStyle)

import generar_pdf as cartas  # registra las fuentes y comparte colores

ENTRADA = "REGLAMENTO.md"
LIBRITO = "reglamento-librito-a5.pdf"
IMPRIMIR = "reglamento-librito-imprimir.pdf"
COMBINADO = "opinologos-muestra-imprenta.pdf"

TINTA = HexColor("#111111")
GRIS = HexColor("#6E6E6E")
LINEA = HexColor("#DADADA")
AZUL = HexColor("#2F6FED")
AW, AH = A5
# Secciones que arrancan en página nueva, para que el librito quede ordenado.
SALTO_ANTES = {"Una ronda", "Ejemplo de una ronda", "Cartas de Acción", "Juego limpio"}
MARGEN = 13 * mm

SIMBOLOS = {
    "🔵": "<font name='Sym' color='#2F6FED'>●</font>",
    "🟠": "<font name='Sym' color='#F08A24'>●</font>",
    "🔴": "<font name='Sym' color='#D7263D'>●</font>",
    "✔": "<font name='Sym' color='#1F9D5C'>✔</font>",
    "✖": "<font name='Sym' color='#D93A3A'>✖</font>",
}

EST = {
    "h2": ParagraphStyle("h2", fontName="PopB", fontSize=15, leading=19, textColor=TINTA,
                         spaceBefore=4 * mm, spaceAfter=2 * mm),
    "h3": ParagraphStyle("h3", fontName="PopSB", fontSize=10.5, leading=13, textColor=AZUL,
                         spaceBefore=3 * mm, spaceAfter=1 * mm),
    "p": ParagraphStyle("p", fontName="PopR", fontSize=9.3, leading=13.5, textColor=TINTA, spaceAfter=2 * mm),
    "cita": ParagraphStyle("cita", fontName="PopR", fontSize=8.5, leading=12, textColor=GRIS,
                           leftIndent=3 * mm, spaceAfter=2 * mm),
    "celda": ParagraphStyle("celda", fontName="PopR", fontSize=8, leading=10.8, textColor=TINTA),
}


# ---------- Markdown -> flowables ----------

def en_linea(texto):
    texto = texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    texto = re.sub(r"\*\*(.+?)\*\*", r"<font name='PopSB'>\1</font>", texto)
    for simbolo, reemplazo in SIMBOLOS.items():  # Poppins no trae estos símbolos
        texto = texto.replace(simbolo, reemplazo)
    return texto


def lista(items, numerada):
    flow = [ListItem(Paragraph(en_linea(t), EST["p"]), leftIndent=4 * mm) for t in items]
    kw = {"bulletType": "1", "bulletFontName": "PopSB"} if numerada else \
         {"bulletType": "bullet", "start": "•", "bulletFontName": "PopR"}
    return ListFlowable(flow, leftIndent=4 * mm, bulletFontSize=9.3, **kw)


def tabla(filas):
    datos = [[Paragraph(f"<font name='PopSB'>{en_linea(c)}</font>" if n == 0 else en_linea(c), EST["celda"])
              for c in f] for n, f in enumerate(filas)]
    ancho = AW - 2 * MARGEN
    cols = [ancho * 0.17, ancho * 0.13, ancho * 0.70] if len(filas[0]) == 3 else None
    t = Table(datos, colWidths=cols, repeatRows=1)
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, TINTA),
        ("LINEBELOW", (0, 1), (-1, -1), 0.4, LINEA),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def convertir(md):
    # La tapa ya lleva título, lema y ficha: el cuerpo arranca en «Objetivo».
    lineas = md.splitlines()
    inicio = next(i for i, l in enumerate(lineas) if l.startswith("**Objetivo:**"))
    lineas = lineas[inicio:]
    flow, i = [], 0
    pendiente = []  # los títulos se mantienen junto a lo que les sigue
    while i < len(lineas):
        l = lineas[i].rstrip()
        nuevo = None
        if not l:
            i += 1
            continue
        if l.startswith("### "):
            pendiente.append(Paragraph(en_linea(l[4:]), EST["h3"])); i += 1
            continue
        if l.startswith("## "):
            if l[3:] in SALTO_ANTES:
                flow.append(PageBreak())
            pendiente.append(Paragraph(en_linea(l[3:]), EST["h2"])); i += 1
            continue
        if l.strip() == "---":
            i += 1
            continue
        if l.startswith(">"):
            bloque = []
            while i < len(lineas) and lineas[i].startswith(">"):
                bloque.append(lineas[i].lstrip("> ").strip()); i += 1
            nuevo = Paragraph(en_linea(" ".join(b for b in bloque if b)), EST["cita"])
        elif l.startswith("|"):
            filas = []
            while i < len(lineas) and lineas[i].startswith("|"):
                celdas = [c.strip() for c in lineas[i].strip().strip("|").split("|")]
                if not all(set(c) <= set("-: ") for c in celdas):
                    filas.append(celdas)
                i += 1
            nuevo = tabla(filas)
        elif re.match(r"^(- |\d+\. )", l):
            numerada = bool(re.match(r"^\d+\. ", l))
            items = []
            while i < len(lineas) and re.match(r"^(- |\d+\. )", lineas[i]):
                items.append(re.sub(r"^(- |\d+\. )", "", lineas[i]).strip()); i += 1
            nuevo = lista(items, numerada)
        else:
            parr = []
            while i < len(lineas) and lineas[i].strip() and not re.match(r"^(#|>|\||- |\d+\. |---)", lineas[i]):
                parr.append(lineas[i].strip()); i += 1
            nuevo = Paragraph(en_linea(" ".join(parr)), EST["p"])
        if pendiente:
            flow.append(KeepTogether(pendiente + [nuevo]))
            pendiente = []
        else:
            flow.append(nuevo)
    return flow


# ---------- tapa y contratapa ----------

def logo(cv, cx, y, size):
    ancho = pdfmetrics.stringWidth(cartas.NOMBRE, "PopB", size)
    x0 = cx - (ancho + size * 0.45) / 2
    cv.setFillColor(white)
    cv.setFont("PopB", size)
    cv.drawString(x0, y, cartas.NOMBRE)
    r = size * 0.055
    for i, (_, col) in enumerate(cartas.NIVELES):
        cv.setFillColor(col)
        cv.circle(x0 + ancho + size * 0.12 + i * r * 2.9, y + r * 1.1, r, stroke=0, fill=1)


def tapa():
    buf = io.BytesIO()
    cv = canvas.Canvas(buf, pagesize=A5)
    cv.setFillColor(cartas.OSCURO)
    cv.rect(0, 0, AW, AH, stroke=0, fill=1)
    logo(cv, AW / 2, AH / 2 + 12 * mm, 34)
    cv.setFillColor(cartas.GRIS_OSCURO)
    cv.setFont("PopR", 10)
    cv.drawCentredString(AW / 2, AH / 2, cartas.LEMA)
    cv.setFillColor(white)
    cv.setFont("PopSB", 12)
    cv.drawCentredString(AW / 2, AH / 2 - 22 * mm, "reglamento")
    cv.setFillColor(cartas.GRIS_OSCURO)
    cv.setFont("PopM", 8.5)
    cv.drawCentredString(AW / 2, 18 * mm, "4 a 8 jugadores  ·  14+ años  ·  40 a 60 minutos")
    cv.showPage()
    cv.save()
    return PdfReader(buf).pages[0]


def contratapa():
    buf = io.BytesIO()
    cv = canvas.Canvas(buf, pagesize=A5)
    cv.setFillColor(cartas.OSCURO)
    cv.rect(0, 0, AW, AH, stroke=0, fill=1)
    cv.setFillColor(white)
    cv.setFont("PopB", 15)
    cv.drawCentredString(AW / 2, AH - 45 * mm, "No gana quien tiene razón.")
    cv.drawCentredString(AW / 2, AH - 53 * mm, "Gana quien convence.")
    cv.setFillColor(cartas.GRIS_OSCURO)
    cv.setFont("PopR", 9)
    for n, linea in enumerate(["Un juego de debate para adolescentes y adultos.",
                               "Todos opinan, todos debaten y el primero que logra",
                               "que alguien cambie de opinión se lleva la carta."]):
        cv.drawCentredString(AW / 2, AH - 68 * mm - n * 5 * mm, linea)
    cv.setFont("PopSB", 8.5)
    cv.setFillColor(white)
    cv.drawCentredString(AW / 2, 62 * mm, "contenido")
    cv.setFont("PopR", 8.5)
    cv.setFillColor(cartas.GRIS_OSCURO)
    for n, linea in enumerate(["70 cartas de Tema (140 temas)", "24 cartas de Acción",
                               "8 cartas de Voto · 8 cartas de Ayuda", "este reglamento"]):
        cv.drawCentredString(AW / 2, 56 * mm - n * 5 * mm, linea)
    logo(cv, AW / 2, 16 * mm, 14)
    cv.showPage()
    cv.save()
    return PdfReader(buf).pages[0]


def numero_pagina(cv, doc):
    cv.setFont("PopM", 6.5)
    cv.setFillColor(GRIS)
    cv.drawCentredString(AW / 2, 8 * mm, str(doc.page + 1))  # la tapa es la página 1


# ---------- armado ----------

def librito_en_orden():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A5, leftMargin=MARGEN, rightMargin=MARGEN,
                            topMargin=MARGEN, bottomMargin=15 * mm)
    doc.build(convertir(open(ENTRADA, encoding="utf-8").read()),
              onFirstPage=numero_pagina, onLaterPages=numero_pagina)
    cuerpo = PdfReader(buf).pages

    paginas = [tapa()] + list(cuerpo)
    while (len(paginas) + 1) % 4:  # el total tiene que ser múltiplo de 4
        paginas.append(PageObject.create_blank_page(width=AW, height=AH))
    paginas.append(contratapa())
    return paginas


def imponer(paginas):
    """Hojas A4 verticales con dos páginas A5 giradas, para doble faz por el borde largo.

    Cada hoja, vista apaisada: frente [N-1-2s | 2s] y dorso [2s+1 | N-2-2s].
    El dorso va girado 180° porque el borde largo de la hoja vertical es el
    borde corto de la vista apaisada.
    """
    W, H = A4
    n = len(paginas)
    hojas = []
    for s in range(n // 4):
        for izq, der, dorso in ((n - 1 - 2 * s, 2 * s, False), (2 * s + 1, n - 2 - 2 * s, True)):
            hoja = PageObject.create_blank_page(width=W, height=H)
            for idx, ox in ((izq, 0), (der, AW)):
                if dorso:  # (x, y) apaisado -> (y, H - x)
                    t = Transformation().translate(ox, 0).rotate(-90).translate(0, H)
                else:      # (x, y) apaisado -> (W - y, x)
                    t = Transformation().translate(ox, 0).rotate(90).translate(W, 0)
                hoja.merge_transformed_page(paginas[idx], t)
            hojas.append(hoja)
    return hojas


def guardar(paginas, archivo, titulo):
    w = PdfWriter()
    for p in paginas:
        w.add_page(p)
    w.add_metadata({"/Title": titulo, "/Author": "Opinólogos"})
    with open(archivo, "wb") as f:
        w.write(f)


def main():
    paginas = librito_en_orden()
    guardar(paginas, LIBRITO, "Opinólogos – reglamento (librito A5)")
    hojas = imponer(PdfReader(LIBRITO).pages)
    guardar(hojas, IMPRIMIR, "Opinólogos – reglamento para imprimir")
    todo = list(PdfReader(cartas.SALIDA).pages) + list(PdfReader(IMPRIMIR).pages)
    guardar(todo, COMBINADO, "Opinólogos – muestra para imprenta")
    print(f"{LIBRITO}: {len(paginas)} páginas A5 · {IMPRIMIR}: {len(hojas)} caras A4 · "
          f"{COMBINADO}: {len(todo)} páginas")


if __name__ == "__main__":
    main()
