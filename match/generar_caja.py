"""Genera la caja de MATCH (estilo C · Pasión): tuck box en una hoja A3.

Uso:  python3 match/generar_caja.py  ->  match/match-caja.pdf
  página 1: arte para imprimir (con 3 mm de sangrado y marcas de corte)
  página 2: arte + troquel (guía para cortar y doblar a mano)
  página 3: troquel solo (para plotter de corte)

Usa el mismo troquel que la caja de Opinólogos (interior 65 x 90 x 42 mm),
que entra justo para las 121 cartas.
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))

import importlib.util  # noqa: E402

# La caja de Opinólogos se carga por ruta: este archivo tiene el mismo nombre.
_spec = importlib.util.spec_from_file_location("caja_base", os.path.join(os.path.dirname(AQUI), "generar_caja.py"))
caja = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(caja)  # troquel, marcas, medidas y helpers
from maquetas import Pasion, pastilla  # noqa: E402
from reportlab.lib.colors import HexColor  # noqa: E402
from reportlab.lib.pagesizes import A3  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402

import generar_pdf as base  # noqa: E402

SALIDA = os.path.join(AQUI, "match-caja.pdf")
P = Pasion()
W, H, D = caja.W, caja.H, caja.D
X_DORSO, X_LAT1, X_FRENTE, X_LAT2 = caja.X_DORSO, caja.X_LAT1, caja.X_FRENTE, caja.X_LAT2
YB, YT, Y0, T = caja.YB, caja.YT, caja.Y0, caja.T
BEIGE_SUAVE = HexColor("#A8987F")  # beige apagado para textos secundarios
girado, texto = caja.girado, caja.texto


def marco(cv, x, y, w, h, margen=3 * mm, color=None):
    cv.setStrokeColor(color or P.beige)
    cv.setLineWidth(0.5)
    cv.roundRect(x + margen, y + margen, w - 2 * margen, h - 2 * margen, 2 * mm, stroke=1, fill=0)


def marco_con_muesca(cv, x, y, w, h, arriba, margen=3 * mm):
    """Marco beige que rodea la muesca del pulgar en vez de quedar cortado por ella."""
    r, R = 2 * mm, caja.MUESCA + margen
    x1, y1, x2, y2 = x + margen, y + margen, x + w - margen, y + h - margen
    cx = x + w / 2
    p = cv.beginPath()
    if arriba:  # muesca en el borde superior (frente)
        p.moveTo(cx + R, y2)
        p.lineTo(x2 - r, y2)
        p.arcTo(x2 - 2 * r, y2 - 2 * r, x2, y2, 90, -90)
        p.lineTo(x2, y1 + r)
        p.arcTo(x2 - 2 * r, y1, x2, y1 + 2 * r, 0, -90)
        p.lineTo(x1 + r, y1)
        p.arcTo(x1, y1, x1 + 2 * r, y1 + 2 * r, 270, -90)
        p.lineTo(x1, y2 - r)
        p.arcTo(x1, y2 - 2 * r, x1 + 2 * r, y2, 180, -90)
        p.lineTo(cx - R, y2)
        p.arcTo(cx - R, y + h - R, cx + R, y + h + R, 180, 180)
    else:  # muesca en el borde inferior (dorso)
        p.moveTo(cx - R, y1)
        p.lineTo(x1 + r, y1)
        p.arcTo(x1, y1, x1 + 2 * r, y1 + 2 * r, 270, -90)
        p.lineTo(x1, y2 - r)
        p.arcTo(x1, y2 - 2 * r, x1 + 2 * r, y2, 180, -90)
        p.lineTo(x2 - r, y2)
        p.arcTo(x2 - 2 * r, y2 - 2 * r, x2, y2, 90, -90)
        p.lineTo(x2, y1 + r)
        p.arcTo(x2 - 2 * r, y1, x2, y1 + 2 * r, 0, -90)
        p.lineTo(cx + R, y1)
        p.arcTo(cx - R, y - R, cx + R, y + R, 0, 180)
    cv.setStrokeColor(P.beige)
    cv.setLineWidth(0.5)
    cv.drawPath(p, stroke=1, fill=0)


def mini_carta(cv, cx, cy, angulo, tipo, frase):
    """Carta en miniatura (escala ~0,45) para ilustrar el frente."""
    w, h = 24.5 * mm, 34.2 * mm
    color = P.bordo if tipo == "pregunta" else P.negro

    def dib():
        cv.setFillColor(HexColor("#000000"), alpha=0.35)
        cv.roundRect(-w / 2 + 0.9 * mm, -h / 2 - 0.9 * mm, w, h, 1.4 * mm, stroke=0, fill=1)
        cv.setFillColor(color)
        cv.setStrokeColor(P.beige)
        cv.setLineWidth(0.35)
        cv.roundRect(-w / 2, -h / 2, w, h, 1.4 * mm, stroke=1, fill=1)
        marco(cv, -w / 2, -h / 2, w, h, margen=1.3 * mm)
        m = 2.6 * mm
        if tipo == "pregunta":
            cv.saveState()
            cv.translate(-w / 2 + m, h / 2 - 6 * mm)
            cv.scale(0.45, 0.45)
            pastilla(cv, 0, 0, "responde tu pareja", P.beige, P.bordo)
            cv.restoreState()
        else:
            cv.setFillColor(P.beige)
            cv.setFont("DMSerifIt", 10.5)
            cv.drawString(-w / 2 + m, h / 2 - 8 * mm, "reto")
            cv.setStrokeColor(P.rojo)
            cv.setLineWidth(0.6)
            cv.line(-w / 2 + m, h / 2 - 9.2 * mm, -w / 2 + m + 5.5 * mm, h / 2 - 9.2 * mm)
            cv.saveState()
            cv.translate(w / 2 - m - 4.5 * mm, h / 2 - 6 * mm)
            cv.scale(0.45, 0.45)
            pastilla(cv, 0, 0, "+18", P.rojo, P.beige)
            cv.restoreState()
        base.parrafo(cv, frase, -w / 2 + m, -h / 2 + 6 * mm, w - 2 * m, h - 17 * mm, "DMSerif", 8, 5,
                     color=P.beige, vertical="centro", interlineado=1.15)
        P.logo(cv, -w / 2 + m, -h / 2 + 3 * mm, 4.2)
    girado(cv, cx, cy, angulo, dib)


# ---------- caras de la caja ----------

def frente(cv):
    x, y = X_FRENTE, YB
    marco_con_muesca(cv, x, y, W, H, arriba=True)
    P.logo(cv, x + W / 2, YT - 25 * mm, 34, centrado=True)
    cv.setFillColor(P.beige)
    cv.setFont("PopM", 6.3)
    cv.drawCentredString(x + W / 2, YT - 32 * mm, "preguntas y retos para parejas")
    cv.setStrokeColor(P.rojo)
    cv.setLineWidth(1)
    cv.line(x + W / 2 - 5 * mm, YT - 35 * mm, x + W / 2 + 5 * mm, YT - 35 * mm)
    mini_carta(cv, x + W / 2 - 13 * mm, y + 33 * mm, 6, "pregunta", "¿Dónde me gusta más que me besen?")
    mini_carta(cv, x + W / 2 + 13 * mm, y + 32 * mm, -5, "reto", "Dale un beso donde elija tu pareja.")
    cv.setFillColor(P.beige)
    cv.setFont("PopM", 5.8)
    cv.drawCentredString(x + W / 2, y + 9.5 * mm, "2 jugadores  ·  +18")
    cv.setFont("PopSB", 5.8)
    cv.drawCentredString(x + W / 2, y + 5.3 * mm, caja.AUTORIA)


def dorso_caja(cv):
    x, y, m = X_DORSO, YB, 7 * mm
    marco_con_muesca(cv, x, y, W, H, arriba=False)
    cv.setFillColor(P.beige)
    cv.setFont("DMSerif", 13.5)
    cv.drawString(x + m, YT - 16 * mm, "¿Cuánto conocés")
    cv.drawString(x + m, YT - 22 * mm, "a tu pareja?")
    texto(cv, "Preguntas para conocerse de verdad y retos para animarse a todo. "
              "Sin ganadores: se juega hasta que quieran.",
          x + m, YT - 40 * mm, W - 2 * m, 14 * mm, size=6.3, color=BEIGE_SUAVE)
    cv.setFillColor(P.beige)
    cv.setFont("DMSerifIt", 10)
    cv.drawString(x + m, YT - 44 * mm, "cómo se juega")
    cv.setStrokeColor(P.rojo)
    cv.setLineWidth(0.8)
    cv.line(x + m, YT - 45.5 * mm, x + m + 7 * mm, YT - 45.5 * mm)
    pasos = [("1", "Sacá una Pregunta y leela en voz alta."),
             ("2", "Si dice «responde tu pareja», tiene que adivinar. Si acierta: ¡Match!"),
             ("3", "Si se equivoca, o no querés responder: toca Reto.")]
    tope = YT - 48.5 * mm
    for num, paso in pasos:
        alto = texto(cv, paso, x + m + 3.5 * mm, tope - 20 * mm, W - 2 * m - 3.5 * mm, 20 * mm,
                     size=6, color=P.beige)
        cv.setFillColor(P.rojo)
        cv.setFont("PopB", 6.3)
        cv.drawString(x + m, tope - 6 * 1.35 + 1.6, num)
        tope -= alto + 1.6 * mm
    cv.setStrokeColor(BEIGE_SUAVE)
    cv.setLineWidth(0.4)
    cv.line(x + m, y + 22 * mm, x + W - m, y + 22 * mm)
    texto(cv, "<font name='PopSB'>Contiene:</font> 90 Preguntas, 30 Retos y 1 carta de cómo jugar.",
          x + m, y + 14.5 * mm, W - 2 * m - 10 * mm, 7 * mm, size=5.3, color=BEIGE_SUAVE)
    pastilla(cv, x + W - m - 9 * mm, y + 13.5 * mm, "+18", P.rojo, P.beige)


def laterales(cv):
    cy = (YB + YT) / 2
    marco(cv, X_LAT1, YB, D, H)
    girado(cv, X_LAT1 + D / 2, cy, 90, lambda: P.logo(cv, 0, -4 * mm, 26, centrado=True))

    # Segundo lateral: QR de Instagram sobre una placa beige para que se escanee bien.
    marco(cv, X_LAT2, YB, D, H)
    ancho_img, alto_img = 1393, 1700
    qr_ancho = caja.QR_ANCHO
    qr_alto = qr_ancho * alto_img / ancho_img
    qx, qy = X_LAT2 + (D - qr_ancho) / 2, cy - qr_alto / 2 - 5 * mm
    pad = 2.5 * mm
    cv.setFillColor(P.beige)
    cv.roundRect(qx - pad, qy - pad, qr_ancho + 2 * pad, qr_alto + 2 * pad, 2 * mm, stroke=0, fill=1)
    qr = os.path.join(os.path.dirname(AQUI), "imagenes", "qr-instagram-transparente.png")
    cv.drawImage(qr, qx, qy, qr_ancho, qr_alto, mask="auto")  # fondo transparente: queda sobre el beige
    cv.setFillColor(P.beige)
    cv.setFont("DMSerifIt", 10)
    cv.drawCentredString(X_LAT2 + D / 2, qy + qr_alto + pad + 6 * mm, "seguinos")
    cv.setFillColor(BEIGE_SUAVE)
    cv.setFont("PopR", 6)
    cv.drawCentredString(X_LAT2 + D / 2, qy + qr_alto + pad + 2.5 * mm, "en Instagram")


def tapas(cv):
    # tapa superior (sale del dorso): se lee desde el frente, así que va girada 180°
    girado(cv, X_DORSO + W / 2, YT + D / 2, 180, lambda: P.logo(cv, 0, -3 * mm, 20, centrado=True))

    def abajo():
        cv.setFillColor(P.beige)
        cv.setFont("PopR", 6)
        cv.drawCentredString(0, -1 * mm, "121 cartas  ·  +18")
    girado(cv, X_FRENTE + W / 2, Y0 + T + D / 2, 180, abajo)


def arte(cv):
    # Fondo negro pleno: cubre todo el desplegado más el sangrado; el troquel recorta el resto.
    s = caja.SANGRADO
    cv.setFillColor(P.negro)
    cv.rect(caja.X0 - s, Y0 - s, caja.ANCHO_TOTAL + 2 * s, caja.ALTO_TOTAL + 2 * s, stroke=0, fill=1)
    frente(cv)
    dorso_caja(cv)
    laterales(cv)
    tapas(cv)


def main():
    cv = canvas.Canvas(SALIDA, pagesize=A3)
    cv.setTitle("Match – caja")
    cv.setAuthor("@oficina.grafica_")
    titulos = {"arte": "1 · arte para imprimir", "guia": "2 · arte + troquel (guía de corte y doblez)",
               "troquel": "3 · troquel (corte en línea continua, doblez en punteada)"}
    for pagina in ("arte", "guia", "troquel"):
        if pagina in ("arte", "guia"):
            arte(cv)
            caja.marcas_de_corte(cv)
        if pagina in ("guia", "troquel"):
            caja.dibujar_troquel(cv)
        cv.setFont("PopM", 8)
        cv.setFillColor(caja.GRIS)
        cv.drawString(15 * mm, A3[1] - 15 * mm, f"match · caja · {titulos[pagina]}")
        cv.showPage()
    cv.save()
    print(f"{os.path.relpath(SALIDA)}: caja de {caja.ANCHO / mm:.0f} x {caja.ALTO / mm:.0f} x "
          f"{caja.PROF / mm:.0f} mm en A3")


if __name__ == "__main__":
    main()
