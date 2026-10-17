"""Imagen 9:16 (1080 x 1920) con una frase de amor, para historias de Instagram.

Uso:  python3 redes/frase_amor.py  ->  redes/frase-amor.png
"""
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path[:0] = [RAIZ, os.path.join(RAIZ, "citas")]

import portadas_personalizadas  # noqa: E402,F401  (registra Poppins)
from reportlab.lib.colors import HexColor  # noqa: E402
from reportlab.lib.enums import TA_CENTER  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402
from reportlab.platypus import Paragraph  # noqa: E402

W, H = 540, 960  # puntos; se exporta a 144 dpi -> 1080 x 1920 px

FRASE = ("Soy fiel al pensamiento de que no hay tinta suficiente ni hoja lo bastante grande para "
         "los sentimientos de un enamorado. Pero voy a esforzarme para que, en unas pocas hojas, "
         "pueda explicarte todo lo que atraviesa mi cuerpo y mi mente cada vez que me besas, "
         "me abrazas o solo me miras a los ojos.")
CIERRE = "Casi como si fuera una cuestión religiosa."


def main():
    """Versión sin diseño: fondo blanco, letra negra, nada más."""
    pdf = os.path.join(AQUI, "frase-amor.pdf")
    cv = canvas.Canvas(pdf, pagesize=(W, H))
    cv.setFillColor(HexColor("#FFFFFF"))
    cv.rect(0, 0, W, H, stroke=0, fill=1)
    estilo = ParagraphStyle("f", fontName="PopR", fontSize=19, leading=28, textColor=HexColor("#000000"),
                            alignment=TA_CENTER)
    p = Paragraph(f"“{FRASE}<br/><br/>{CIERRE}”", estilo)
    ancho = W - 110
    _, alto = p.wrap(ancho, H)
    p.drawOn(cv, (W - ancho) / 2, (H - alto) / 2)
    cv.showPage()
    cv.save()
    subprocess.run(["pdftoppm", "-r", "144", "-png", "-singlefile", pdf, os.path.join(AQUI, "frase-amor")],
                   check=True)
    os.remove(pdf)
    print("ok frase-amor.png")


if __name__ == "__main__":
    main()
