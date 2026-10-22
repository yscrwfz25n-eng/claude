"""Pasa las etiquetas del PDF a PNG con fondo transparente.

Uso:  python3 etiquetas/sin_fondo.py etiquetas.pdf  ->  etiquetas/png/NN-nombre.png

Cada página trae una imagen RGB sobre blanco. El blanco del fondo se vuelve transparente con
«color a alfa» respecto de la tinta de esa etiqueta (bordó en la mayoría, gris claro en las de
serum), así los bordes de las letras quedan suaves. El texto blanco dentro de las barras de color
NO se borra: lo que queda encerrado por una barra se conserva tal cual.
"""
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image
from scipy import ndimage

AQUI = os.path.dirname(os.path.abspath(__file__))
NOMBRES = [
    "resaltador-de-bronceado", "bronceador-intense-brazilian-tropical", "ultra-glitter",
    "protector-solar-daily-invisible", "protector-solar-con-color", "crema-de-manos", "agua-micelar",
    "bruma-facial", "serum-iluminador-roll-on", "lip-oil-hidratante", "serum-vitamina-c-radiance",
    "serum-retinol-age-defy", "serum-ceramide-jojoba", "crema-facial-niacinamida",
    "crema-facial-boost-hydra-plump", "crema-facial-alantoina-avena", "mascarilla-arcilla-organica",
    "mascarilla-fresh-mix-vitamina-c", "mascarilla-fresh-mix-hialuronico", "crema-exfoliante",
    "crema-exfoliante-scrub-watermelon", "balsamo-labial", "fijador-de-cejas", "body-splash",
]


def sin_fondo(img):
    rgb = np.asarray(img.convert("RGB")).astype(float)
    dist = 255 - rgb.min(axis=2)                       # cuánto se aleja del blanco
    tinta_px = dist > 0.7 * dist.max()
    tinta = np.median(rgb[tinta_px], axis=0)           # color de tinta de esta etiqueta
    d_tinta = 255 - tinta.min()
    alfa = np.clip(dist / d_tinta, 0, 1)

    # barras de color: componentes grandes de tinta; lo que encierran (texto blanco) se conserva
    h, w = dist.shape
    etiquetas, _ = ndimage.label(dist > 0.5 * d_tinta)
    barras = np.zeros((h, w), bool)
    for i, sl in enumerate(ndimage.find_objects(etiquetas), 1):
        alto, ancho = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        comp = etiquetas[sl] == i
        if ancho > 0.45 * w and alto > 0.03 * h:
            lleno = ndimage.binary_fill_holes(comp)
            if lleno.mean() > 0.85:  # casi un rectángulo: es una barra, no el logo
                barras[sl] |= lleno
    adentro = ndimage.binary_erosion(barras, iterations=2)

    color = np.where(adentro[..., None], rgb, tinta)
    alfa = np.where(adentro, 1.0, alfa)
    out = np.dstack([color, alfa * 255]).clip(0, 255).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def main(pdf):
    salida = os.path.join(AQUI, "png")
    os.makedirs(salida, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdfimages", "-png", pdf, os.path.join(tmp, "e")], check=True)
        archivos = sorted(f for f in os.listdir(tmp) if f.endswith(".png"))
        assert len(archivos) == len(NOMBRES), f"{len(archivos)} imágenes, {len(NOMBRES)} nombres"
        for n, (f, nombre) in enumerate(zip(archivos, NOMBRES), 1):
            img = sin_fondo(Image.open(os.path.join(tmp, f)))
            img = img.crop(img.getbbox())
            img.save(os.path.join(salida, f"{n:02d}-{nombre}.png"), optimize=True)
    print("ok", len(NOMBRES), "png en", os.path.relpath(salida))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, "etiquetas.pdf"))
