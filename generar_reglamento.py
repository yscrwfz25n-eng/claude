"""Arma el reglamento como librito del tamaño de las cartas (63 x 88 mm), para que entre en la caja.

Uso:  python3 generar_reglamento.py
  ->  opinologos-reglamento.pdf           páginas de 63 x 88 mm en orden de lectura
  ->  opinologos-reglamento-imprimir.pdf  hojas A4 doble faz (borde largo) con los pliegos
                                          armados: cortar, doblar al medio, intercalar y abrochar

Soporta el Markdown que usa REGLAMENTO.md: títulos ##/###, párrafos, listas,
citas (>), tablas (se pasan a lista) y **negrita**.
"""
import io
import re

from pypdf import PageObject, PdfReader, PdfWriter, Transformation
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.platypus import (KeepTogether, ListFlowable, ListItem, PageBreak, Paragraph,
                                SimpleDocTemplate)

import generar_pdf as cartas  # registra las fuentes y comparte colores

ENTRADA = "REGLAMENTO.md"
LECTURA = "opinologos-reglamento.pdf"
IMPRIMIR = "opinologos-reglamento-imprimir.pdf"
AUTORIA = "un juego de @oficina.grafica_"

TINTA = HexColor("#111111")
GRIS = HexColor("#6E6E6E")
AZUL = HexColor("#2F6FED")
PW, PH = cartas.CW, cartas.CH  # página del librito = tamaño de carta
# Secciones que arrancan en página nueva.
SALTO_ANTES = set()

SIMBOLOS = {
    "🔵": "<font name='Sym' color='#2F6FED'>●</font>",
    "🟠": "<font name='Sym' color='#F08A24'>●</font>",
    "🔴": "<font name='Sym' color='#D7263D'>●</font>",
    "✔": "<font name='Sym' color='#1F9D5C'>✔</font>",
    "✖": "<font name='Sym' color='#D93A3A'>✖</font>",
}

EST = {
    "h2": ParagraphStyle("h2", fontName="PopB", fontSize=10, leading=12.5, textColor=TINTA,
                         spaceBefore=2 * mm, spaceAfter=1.2 * mm),
    "h3": ParagraphStyle("h3", fontName="PopSB", fontSize=7.6, leading=9.5, textColor=AZUL,
                         spaceBefore=1.6 * mm, spaceAfter=0.5 * mm),
    "p": ParagraphStyle("p", fontName="PopR", fontSize=6.8, leading=9.2, textColor=TINTA, spaceAfter=1.2 * mm),
    "cita": ParagraphStyle("cita", fontName="PopR", fontSize=6.4, leading=8.6, textColor=GRIS,
                           leftIndent=2 * mm, spaceAfter=1.2 * mm),
}


# ---------- Markdown -> flowables ----------

def en_linea(texto):
    texto = texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    texto = re.sub(r"\*\*(.+?)\*\*", r"<font name='PopSB'>\1</font>", texto)
    for simbolo, reemplazo in SIMBOLOS.items():  # Poppins no trae estos símbolos
        texto = texto.replace(simbolo, reemplazo)
    return texto


def lista(items, numerada):
    """Un flowable por ítem, así una lista larga puede seguir en la página siguiente."""
    salida = []
    for n, t in enumerate(items, start=1):
        kw = {"bulletType": "1", "start": n, "bulletFontName": "PopSB"} if numerada else \
             {"bulletType": "bullet", "start": "•", "bulletFontName": "PopR"}
        salida.append(ListFlowable([ListItem(Paragraph(en_linea(t), EST["p"]), leftIndent=3 * mm)],
                                   leftIndent=3 * mm, bulletFontSize=6.8, **kw))
    return salida


def tabla_como_lista(filas):
    """En una página tan chica una tabla no entra: cada fila pasa a ser un ítem."""
    items = []
    for f in filas[1:]:
        items.append(f"**{f[0]}** ({f[1]}): {f[2]}" if len(f) == 3 else " · ".join(f))
    return lista(items, numerada=False)


def convertir(md):
    # La tapa ya lleva título, lema y ficha: el cuerpo arranca en «Objetivo».
    lineas = md.splitlines()
    inicio = next(i for i, l in enumerate(lineas) if l.startswith("**Objetivo:**"))
    lineas = lineas[inicio:]
    flow, i, pendiente = [], 0, []  # los títulos se mantienen junto a lo que les sigue
    while i < len(lineas):
        l = lineas[i].rstrip()
        if not l or l.strip() == "---":
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
            nuevo = tabla_como_lista(filas)
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
        nuevos = nuevo if isinstance(nuevo, list) else [nuevo]
        if pendiente:
            flow.append(KeepTogether(pendiente + nuevos[:1]))
            flow.extend(nuevos[1:])
            pendiente = []
        else:
            flow.extend(nuevos)
    return flow


# ---------- tapa y contratapa ----------

def logo(cv, cx, y, size):
    ancho = pdfmetrics.stringWidth(cartas.NOMBRE, "PopB", size)
    x0 = cx - (ancho + size * 0.45) / 2
    cv.setFillColor(TINTA)
    cv.setFont("PopB", size)
    cv.drawString(x0, y, cartas.NOMBRE)
    r = size * 0.055
    for i, (_, col) in enumerate(cartas.NIVELES):
        cv.setFillColor(col)
        cv.circle(x0 + ancho + size * 0.12 + i * r * 2.9, y + r * 1.1, r, stroke=0, fill=1)


def una_pagina(dibujar):
    buf = io.BytesIO()
    cv = canvas.Canvas(buf, pagesize=(PW, PH))
    dibujar(cv)
    cv.showPage()
    cv.save()
    return PdfReader(buf).pages[0]


def tapa(cv):
    logo(cv, PW / 2, PH / 2 + 8 * mm, 17)
    cv.setFillColor(GRIS)
    cv.setFont("PopR", 6.3)
    cv.drawCentredString(PW / 2, PH / 2 + 1.5 * mm, cartas.LEMA)
    cv.setFillColor(TINTA)
    cv.setFont("PopSB", 8)
    cv.drawCentredString(PW / 2, PH / 2 - 10 * mm, "reglamento")
    cv.setFillColor(GRIS)
    cv.setFont("PopM", 5.6)
    cv.drawCentredString(PW / 2, 13 * mm, "4 a 8 jugadores · 14+ años · 40 a 60 min")
    cv.setFillColor(TINTA)
    cv.setFont("PopSB", 6)
    cv.drawCentredString(PW / 2, 7 * mm, AUTORIA)


def contratapa(cv):
    cv.setFillColor(TINTA)
    cv.setFont("PopB", 9)
    cv.drawCentredString(PW / 2, PH - 20 * mm, "No gana quien tiene razón.")
    cv.drawCentredString(PW / 2, PH - 25 * mm, "Gana quien convence.")
    cv.setFillColor(GRIS)
    cv.setFont("PopR", 5.8)
    for n, linea in enumerate(["Un juego de debate para adolescentes y adultos.",
                               "Todos opinan, todos debaten y el primero que",
                               "logra que alguien cambie de opinión",
                               "se lleva la carta."]):
        cv.drawCentredString(PW / 2, PH - 33 * mm - n * 3.2 * mm, linea)
    cv.setFillColor(TINTA)
    cv.setFont("PopSB", 6)
    cv.drawCentredString(PW / 2, 33 * mm, "contenido")
    cv.setFillColor(GRIS)
    cv.setFont("PopR", 5.6)
    for n, linea in enumerate(["70 cartas de Tema (140 temas) · 24 de Acción",
                               "8 de Voto · 8 de Ayuda · este reglamento"]):
        cv.drawCentredString(PW / 2, 29 * mm - n * 3.2 * mm, linea)
    logo(cv, PW / 2, 13 * mm, 9)
    cv.setFillColor(TINTA)
    cv.setFont("PopSB", 6)
    cv.drawCentredString(PW / 2, 7 * mm, AUTORIA)


def numero_pagina(cv, doc):
    cv.setFont("PopM", 5.5)
    cv.setFillColor(GRIS)
    cv.drawCentredString(PW / 2, 3.5 * mm, str(doc.page + 1))  # la tapa es la página 1


# ---------- armado ----------

def librito_en_orden():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=(PW, PH), leftMargin=5 * mm, rightMargin=5 * mm,
                            topMargin=5 * mm, bottomMargin=7 * mm)
    doc.build(convertir(open(ENTRADA, encoding="utf-8").read()),
              onFirstPage=numero_pagina, onLaterPages=numero_pagina)
    paginas = [una_pagina(tapa)] + list(PdfReader(buf).pages)
    while (len(paginas) + 1) % 4:  # el total tiene que ser múltiplo de 4
        paginas.append(PageObject.create_blank_page(width=PW, height=PH))
    paginas.append(una_pagina(contratapa))
    return paginas


def marcas(cv, x0, y0, filas):
    """Marcas de corte alrededor de los pliegos y marca de doblez en el medio."""
    cv.setStrokeColor(cartas.GRIS)
    cv.setLineWidth(0.3)
    sep, largo = 2 * mm, 5 * mm
    ancho = 2 * PW
    for x in (x0, x0 + ancho):
        cv.line(x, y0 - sep, x, y0 - sep - largo)
        cv.line(x, y0 + filas * PH + sep, x, y0 + filas * PH + sep + largo)
    for j in range(filas + 1):
        y = y0 + j * PH
        cv.line(x0 - sep, y, x0 - sep - largo, y)
        cv.line(x0 + ancho + sep, y, x0 + ancho + sep + largo, y)
    cv.setDash(1.5, 1.5)  # doblez
    xm = x0 + PW
    cv.line(xm, y0 - sep, xm, y0 - sep - largo)
    cv.line(xm, y0 + filas * PH + sep, xm, y0 + filas * PH + sep + largo)
    cv.setDash()


def imponer(paginas):
    """Pliegos de 126 x 88 mm (dos páginas) apilados de a 3 por cara A4.

    Pliego s: frente [N-1-2s | 2s], dorso [2s+1 | N-2-2s]. Al voltear la hoja A4 por
    el borde largo el pliego queda en la misma fila, así que no hace falta girar nada.
    """
    W, H = A4
    n = len(paginas)
    pliegos = n // 4
    por_hoja = int((H - 20 * mm) // PH)
    x0 = (W - 2 * PW) / 2
    hojas = []
    for inicio in range(0, pliegos, por_hoja):
        grupo = range(inicio, min(inicio + por_hoja, pliegos))
        y0 = (H - len(grupo) * PH) / 2
        for cara in ("frente", "dorso"):
            buf = io.BytesIO()
            cv = canvas.Canvas(buf, pagesize=A4)
            marcas(cv, x0, y0, len(grupo))
            cv.showPage()
            cv.save()
            hoja = PdfReader(buf).pages[0]
            for fila, s in enumerate(grupo):
                izq, der = (n - 1 - 2 * s, 2 * s) if cara == "frente" else (2 * s + 1, n - 2 - 2 * s)
                y = y0 + (len(grupo) - 1 - fila) * PH
                for idx, ox in ((izq, x0), (der, x0 + PW)):
                    hoja.merge_transformed_page(paginas[idx], Transformation().translate(ox, y))
            hojas.append(hoja)
    return hojas


def guardar(paginas, archivo, titulo):
    w = PdfWriter()
    for p in paginas:
        w.add_page(p)
    w.add_metadata({"/Title": titulo, "/Author": "@oficina.grafica_"})
    with open(archivo, "wb") as f:
        w.write(f)


def main():
    paginas = librito_en_orden()
    guardar(paginas, LECTURA, "Opinólogos – reglamento")
    hojas = imponer(PdfReader(LECTURA).pages)
    guardar(hojas, IMPRIMIR, "Opinólogos – reglamento para imprimir")
    print(f"{LECTURA}: {len(paginas)} páginas de 63 x 88 mm · {IMPRIMIR}: {len(hojas)} caras A4")


if __name__ == "__main__":
    main()
