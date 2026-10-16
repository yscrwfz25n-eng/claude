"""Convierte REGLAMENTO.md en un PDF A4 con el estilo del juego y arma el archivo para la imprenta.

Uso:  python3 generar_reglamento.py
  ->  reglamento.pdf                    (solo el reglamento)
  ->  opinologos-muestra-imprenta.pdf   (cartas + reglamento, listo para mandar)

Requiere haber corrido antes generar_pdf.py. Soporta el Markdown que usa el
reglamento: títulos #/##/###, párrafos, listas, citas (>), tablas y **negrita**.
"""
import re

from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (HRFlowable, ListFlowable, ListItem, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

import generar_pdf  # registra las fuentes Poppins

ENTRADA = "REGLAMENTO.md"
SALIDA = "reglamento.pdf"
COMBINADO = "opinologos-muestra-imprenta.pdf"

TINTA = HexColor("#111111")
GRIS = HexColor("#6E6E6E")
LINEA = HexColor("#DADADA")
AZUL = HexColor("#2F6FED")

SIMBOLOS = {
    "🔵": "<font name='Sym' color='#2F6FED'>●</font>",
    "🟠": "<font name='Sym' color='#F08A24'>●</font>",
    "🔴": "<font name='Sym' color='#D7263D'>●</font>",
    "✔": "<font name='Sym' color='#1F9D5C'>✔</font>",
    "✖": "<font name='Sym' color='#D93A3A'>✖</font>",
}

EST = {
    "h1": ParagraphStyle("h1", fontName="PopB", fontSize=24, leading=28, textColor=TINTA, spaceAfter=4 * mm),
    "h2": ParagraphStyle("h2", fontName="PopB", fontSize=14, leading=18, textColor=TINTA,
                         spaceBefore=5 * mm, spaceAfter=2 * mm),
    "h3": ParagraphStyle("h3", fontName="PopSB", fontSize=11, leading=14, textColor=AZUL,
                         spaceBefore=3 * mm, spaceAfter=1 * mm),
    "p": ParagraphStyle("p", fontName="PopR", fontSize=9.5, leading=14, textColor=TINTA, spaceAfter=2 * mm),
    "cita": ParagraphStyle("cita", fontName="PopR", fontSize=9, leading=13, textColor=GRIS,
                           leftIndent=4 * mm, spaceAfter=2 * mm),
    "celda": ParagraphStyle("celda", fontName="PopR", fontSize=8.5, leading=11.5, textColor=TINTA),
}


def en_linea(texto):
    """Markdown en línea -> mini HTML de reportlab."""
    texto = texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    texto = re.sub(r"\*\*(.+?)\*\*", r"<font name='PopSB'>\1</font>", texto)
    # Poppins no trae estos símbolos: se dibujan con DejaVu y el color de cada nivel
    for simbolo, reemplazo in SIMBOLOS.items():
        texto = texto.replace(simbolo, reemplazo)
    return texto


def lista(items, numerada):
    flow = [ListItem(Paragraph(en_linea(t), EST["p"]), leftIndent=5 * mm) for t in items]
    kw = {"bulletType": "1", "bulletFontName": "PopSB"} if numerada else \
         {"bulletType": "bullet", "start": "•", "bulletFontName": "PopR"}
    return ListFlowable(flow, leftIndent=5 * mm, bulletFontSize=9.5, **kw)


def tabla(filas):
    datos = [[Paragraph(f"<font name='PopSB'>{en_linea(c)}</font>" if n == 0 else en_linea(c), EST["celda"])
              for c in f] for n, f in enumerate(filas)]
    ancho = A4[0] - 40 * mm
    cols = [ancho * 0.18, ancho * 0.1, ancho * 0.72] if len(filas[0]) == 3 else None
    t = Table(datos, colWidths=cols, repeatRows=1)
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "PopSB"),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, TINTA),
        ("LINEBELOW", (0, 1), (-1, -1), 0.4, LINEA),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def convertir(md):
    flow, i, lineas = [], 0, md.splitlines()
    while i < len(lineas):
        l = lineas[i].rstrip()
        if not l:
            i += 1
        elif l.startswith("### "):
            flow.append(Paragraph(en_linea(l[4:]), EST["h3"])); i += 1
        elif l.startswith("## "):
            flow.append(Paragraph(en_linea(l[3:]), EST["h2"])); i += 1
        elif l.startswith("# "):
            flow.append(Paragraph(en_linea(l[2:].replace("OPINÓLOGOS", "opinólogos")), EST["h1"])); i += 1
        elif l.strip() == "---":
            flow.append(HRFlowable(width="100%", thickness=0.5, color=LINEA, spaceBefore=2 * mm,
                                   spaceAfter=2 * mm)); i += 1
        elif l.startswith(">"):
            bloque = []
            while i < len(lineas) and lineas[i].startswith(">"):
                bloque.append(lineas[i].lstrip("> ").strip()); i += 1
            flow.append(Paragraph(en_linea(" ".join(b for b in bloque if b)), EST["cita"]))
        elif l.startswith("|"):
            filas = []
            while i < len(lineas) and lineas[i].startswith("|"):
                celdas = [c.strip() for c in lineas[i].strip().strip("|").split("|")]
                if not all(set(c) <= set("-: ") for c in celdas):
                    filas.append(celdas)
                i += 1
            flow.append(tabla(filas)); flow.append(Spacer(1, 2 * mm))
        elif re.match(r"^(- |\d+\. )", l):
            numerada = bool(re.match(r"^\d+\. ", l))
            items = []
            while i < len(lineas) and re.match(r"^(- |\d+\. )", lineas[i]):
                items.append(re.sub(r"^(- |\d+\. )", "", lineas[i]).strip()); i += 1
            flow.append(lista(items, numerada)); flow.append(Spacer(1, 1.5 * mm))
        else:
            parr = []
            while i < len(lineas) and lineas[i].strip() and not re.match(r"^(#|>|\||- |\d+\. |---)", lineas[i]):
                parr.append(lineas[i].strip()); i += 1
            flow.append(Paragraph(en_linea(" ".join(parr)), EST["p"]))
    return flow


def pie(cv, doc):
    cv.setFont("PopB", 7)
    cv.setFillColor(GRIS)
    cv.drawString(20 * mm, 12 * mm, "opinólogos · reglamento")
    cv.drawRightString(A4[0] - 20 * mm, 12 * mm, str(doc.page))


def main():
    doc = SimpleDocTemplate(SALIDA, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=18 * mm, bottomMargin=20 * mm,
                            title="Opinólogos – reglamento", author="Opinólogos")
    doc.build(convertir(open(ENTRADA, encoding="utf-8").read()), onFirstPage=pie, onLaterPages=pie)

    escritor = PdfWriter()
    cartas = PdfReader(generar_pdf.SALIDA)
    for p in cartas.pages:
        escritor.add_page(p)
    regla = PdfReader(SALIDA)
    for p in regla.pages:
        escritor.add_page(p)
    if len(regla.pages) % 2:  # el reglamento ocupa hojas completas doble faz
        escritor.add_blank_page(*A4)
    escritor.add_metadata({"/Title": "Opinólogos – muestra para imprenta"})
    with open(COMBINADO, "wb") as f:
        escritor.write(f)
    print(f"{SALIDA}: {len(regla.pages)} páginas · {COMBINADO}: {len(escritor.pages)} páginas")


if __name__ == "__main__":
    main()
