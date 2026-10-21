"""Recorta el perro salchicha de las dos capturas de referencia (carrusel continuo sobre fondo rosa).

Las capturas (ref-1.png, ref-2.png) no se suben al repositorio: muestran cuentas y mensajes de terceros.

Uso:  python3 redes/regalito/recortar_perro.py  ->  perro-salchicha.png (con transparencia)
       y deja en COSTURA (dentro del PNG) la columna donde estaba el corte entre las dos slides.

Se unen las dos slides, se separa el fondo rosa por color y se queda con la mancha conectada
que contiene al perro (descarta textos, corazones y productos que no lo tocan).
"""
import os

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

AQUI = os.path.dirname(os.path.abspath(__file__))
Y0, Y1 = 554, 1895          # alto útil del posteo en la captura (abajo se corta antes del botón de audio)
ROSA = np.array([248, 218, 247])

slides = [np.asarray(Image.open(os.path.join(AQUI, f)).convert("RGB"))[Y0:Y1] for f in ("ref-1.png", "ref-2.png")]
img = np.concatenate(slides, axis=1).astype(int)
ancho_slide = slides[0].shape[1]

dist = np.sqrt(((img - ROSA) ** 2).sum(axis=2))
r, g, b = img[..., 0], img[..., 1], img[..., 2]
pelaje = (dist > 38) & ~((b > r - 10) & (b > 150))         # fuera los rosas/lilas de corazones y destellos
pelaje = ndimage.binary_opening(pelaje, iterations=2)
etiquetas, _ = ndimage.label(pelaje)
semilla = etiquetas[700, 1000]                               # un punto del cuello del perro
perro = ndimage.binary_fill_holes(etiquetas == semilla)
perro = ndimage.binary_closing(perro, iterations=3)
# el corazón rosa que tapaba un poco la oreja: se rellena con el pelaje más cercano
mancha = perro & (r > 205) & (b > r - 10) & (b > 150)  # solo rosa claro: la nariz tiene reflejos azulados
mancha = ndimage.binary_dilation(mancha, iterations=4) & perro
_, (iy, ix) = ndimage.distance_transform_edt(mancha, return_indices=True)
img = img[iy, ix]
suave = np.stack([ndimage.gaussian_filter(img[..., c].astype(float), 4) for c in range(3)], axis=2)
# el parche se funde con el pelaje: borde difuminado y un poco de grano para que no quede liso
peso = ndimage.gaussian_filter(mancha.astype(float), 3)[..., None]
grano = np.random.default_rng(3).normal(0, 9, img.shape[:2])[..., None]
img = (img * (1 - peso) + (suave + grano) * peso).clip(0, 255).astype(int)
alfa = Image.fromarray((perro * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(1.1))
out = Image.fromarray(img.astype("uint8")).convert("RGBA")
out.putalpha(alfa)
caja = out.getbbox()
out = out.crop(caja)
out.save(os.path.join(AQUI, "perro-salchicha.png"))
print("ok perro-salchicha.png", out.size, "costura en x =", ancho_slide - caja[0])
