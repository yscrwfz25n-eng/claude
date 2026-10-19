"""Página de muestra del interior del ÁLBUM DE VINOS.

Uso:  python3 vinos/generar_pagina.py
  -> vinos/album-de-vinos-pagina-muestra.pdf   A5 con 3 mm de sangrado
  -> vinos/pagina-muestra.png                  vista previa al corte
"""
import os
import subprocess
import tempfile

from PIL import Image

from generar_tapa import AQUI, pdf_de_imprenta

SALIDA = os.path.join(AQUI, "album-de-vinos-pagina-muestra.pdf")

if __name__ == "__main__":
    pdf_de_imprenta("pagina.html", SALIDA, "Álbum de vinos – página de muestra")
    base = os.path.join(tempfile.mkdtemp(), "pagina")
    subprocess.run(["pdftoppm", "-r", "150", "-png", "-singlefile", SALIDA, base], check=True)
    img = Image.open(base + ".png")
    s = round(3 / 25.4 * 150)
    img.crop((s, s, img.width - s, img.height - s)).save(os.path.join(AQUI, "pagina-muestra.png"))
    print("ok pagina-muestra.png")
