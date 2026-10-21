"""Recortes con fondo transparente de los 4 productos, para el carrusel «Te quiero… pedir un regalito».

Uso:  python3 redes/regalito/productos.py
  -> caja-opinologos.png, caja-match.png   cajas en 3D (mismo render que foto_producto.py)
  -> carta-*.png                           cartas sueltas con sombra
  -> libro-dating-list.png                 The Dating List (tapa dura con elástico)
  -> libro-vinos.png                       Álbum de vinos (anillado)
"""
import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "citas"))

import foto_producto as fp  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402
import tapa as dating  # noqa: E402  (citas/tapa.py)
from portadas_personalizadas import PH, PW  # noqa: E402


def recortar(img):
    return img.crop(img.getbbox())


def caja(pdf, nombre, tmp):
    lienzo = Image.new("RGBA", (900, 1100), (0, 0, 0, 0))
    fp.caja_3d(lienzo, fp.caras_de_caja(pdf, tmp), 260, 980, 800)
    recortar(lienzo).save(os.path.join(AQUI, nombre))


def carta(pdf, pagina, indice, nombre, tmp):
    img = fp.carta(pdf, pagina, indice, tmp).convert("RGBA")
    img = img.resize((round(img.width * 0.55), round(img.height * 0.55)), Image.LANCZOS)
    m = 40
    sombra = Image.new("RGBA", (img.width + 2 * m, img.height + 2 * m), (0, 0, 0, 0))
    negro = Image.new("RGBA", img.size, (20, 26, 34, 90))
    sombra.paste(negro, (m + 6, m + 10))
    sombra = sombra.filter(ImageFilter.GaussianBlur(12))
    sombra.alpha_composite(img, (m, m))
    recortar(sombra).save(os.path.join(AQUI, nombre))


def dating_list(tmp):
    m = 16 * mm
    pdf = os.path.join(tmp, "dating.pdf")
    cv = canvas.Canvas(pdf, pagesize=(PW + 2 * m, PH + 2 * m))
    dating.tapa(cv, m, m + 4 * mm)
    cv.showPage()
    cv.save()
    base = os.path.join(tmp, "dating")
    subprocess.run(["pdftocairo", "-r", "200", "-png", "-transp", "-singlefile", pdf, base], check=True)
    recortar(Image.open(base + ".png")).save(os.path.join(AQUI, "libro-dating-list.png"))


def main():
    with tempfile.TemporaryDirectory() as tmp:
        caja(os.path.join(RAIZ, "opinologos-caja.pdf"), "caja-opinologos.png", tmp)
        caja(os.path.join(RAIZ, "match", "match-caja.pdf"), "caja-match.png", tmp)
        carta(os.path.join(RAIZ, "match", "match-cartas.pdf"), 1, 1, "carta-match.png", tmp)
        carta(os.path.join(RAIZ, "match", "match-cartas.pdf"), 21, 0, "carta-match-reto.png", tmp)
        carta(os.path.join(RAIZ, "opinologos-muestra-imprenta.pdf"), 1, 4, "carta-opinologos.png", tmp)
        dating_list(tmp)
    shutil.copy(os.path.join(os.path.dirname(AQUI), "vinos", "libro-tapa.png"), os.path.join(AQUI, "libro-vinos.png"))
    shutil.copy(os.path.join(os.path.dirname(AQUI), "enojo", "perro.png"), os.path.join(AQUI, "perro.png"))
    for f in sorted(os.listdir(AQUI)):
        if f.endswith(".png"):
            print(f, Image.open(os.path.join(AQUI, f)).size)


if __name__ == "__main__":
    main()
