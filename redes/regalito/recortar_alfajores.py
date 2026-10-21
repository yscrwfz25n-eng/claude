"""Recorta el álbum de alfajores de su foto sobre fondo blanco -> album-alfajores.png (con transparencia).

Se inunda el fondo desde los bordes de la foto (gris claro casi sin color) y queda el álbum.
"""
import os

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

AQUI = os.path.dirname(os.path.abspath(__file__))
img = np.asarray(Image.open(os.path.join(AQUI, "alfajores-foto.jpg")).convert("RGB")).astype(int)
r, g, b = img[..., 0], img[..., 1], img[..., 2]
claro = (np.minimum(np.minimum(r, g), b) > 200) & ((np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)) < 18)
etiquetas, _ = ndimage.label(claro)
bordes = set(etiquetas[0]) | set(etiquetas[-1]) | set(etiquetas[:, 0]) | set(etiquetas[:, -1])
fondo = np.isin(etiquetas, [e for e in bordes if e])
album = ndimage.binary_fill_holes(~fondo)
album = ndimage.binary_opening(album, iterations=2)
alfa = Image.fromarray((album * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(.8))
out = Image.fromarray(img.astype("uint8")).convert("RGBA")
out.putalpha(alfa)
out = out.crop(out.getbbox())
out.save(os.path.join(AQUI, "album-alfajores.png"))
print("ok album-alfajores.png", out.size)
