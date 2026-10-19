"""Separa al perro del fondo azul liso de la referencia (chroma key) -> perro.png con transparencia."""
import os

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

AQUI = os.path.dirname(os.path.abspath(__file__))
img = np.asarray(Image.open(os.path.join(AQUI, "referencia.webp")).convert("RGB")).astype(float)
r, g, b = img[..., 0], img[..., 1], img[..., 2]
# fondo y garabatos son azules (B muy por encima de R); el pelaje es marrón/beige
perro = (r - b) > -25
perro[:400] = False                               # títulos de la referencia
etiquetas, n = ndimage.label(perro)
mayor = np.argmax(np.bincount(etiquetas.ravel())[1:]) + 1
perro = ndimage.binary_fill_holes(etiquetas == mayor)
perro = ndimage.binary_opening(perro, iterations=2)
alfa = Image.fromarray((perro * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(1.2))
# quitar el reflejo azul del borde
rgb = img.copy()
borde = np.asarray(alfa) < 250
rgb[..., 2] = np.where(borde, np.minimum(b, (r + g) / 2), b)
out = Image.fromarray(rgb.astype("uint8")).convert("RGBA")
out.putalpha(alfa)
out = out.crop(out.getbbox())
out.save(os.path.join(AQUI, "perro.png"))
print("ok perro.png", out.size)
