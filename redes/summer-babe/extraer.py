"""Extrae el diseño «Summer Babe · Cocktail Club» de la foto de la plancha y lo deja en PNG sin fondo.

Uso:  python3 extraer.py  ->  summer-babe.png (al doble de resolución, fondo transparente)

1 · recorta la zona del diseño (sin los diseños vecinos de la plancha);
2 · estima el fondo (papel con luz despareja) con un filtro de máximo grande + desenfoque;
3 · «color a alfa»: cuánto se aleja cada píxel del fondo es su opacidad, y se recupera el color de tinta;
4 · limpia el ruido del papel, duplica la resolución y aplica un enfoque suave.
"""
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

im = np.asarray(Image.open("foto.jpg").convert("RGB")).astype(np.float32)
X0, Y0, X1, Y1 = 200, 535, 1165, 1640
img = im[Y0:Y1, X0:X1]
h, w = img.shape[:2]

# zona útil: deja afuera la flor rosa (abajo a la derecha) y el texto verde de la izquierda
zona = Image.new("L", (w, h), 0)
ImageDraw.Draw(zona).polygon([(15, 0), (w - 1, 0), (w - 1, 640), (925, 680), (925, h - 1), (15, h - 1)], fill=255)
zona = np.asarray(zona) > 0

fondo = np.stack([cv2.GaussianBlur(cv2.dilate(img[..., c], np.ones((41, 41), np.uint8)), (0, 0), 25) for c in range(3)], 2)
dif = np.clip(fondo - img, 0, None)                     # la tinta es más oscura que el papel
alfa = np.clip(dif.max(axis=2) / np.maximum(fondo.max(axis=2) * 0.75, 1), 0, 1)
alfa = np.clip((alfa - 0.07) / 0.93, 0, 1) ** 0.9        # fuera el grano del papel
alfa[~zona] = 0
# se queda solo con lo que está cerca de tinta firme: borra la neblina del papel y los bordes sueltos
firme = cv2.dilate((alfa > 0.35).astype(np.uint8), np.ones((9, 9), np.uint8))
firme = cv2.GaussianBlur(firme.astype(np.float32), (0, 0), 2)
alfa = alfa * np.clip(firme * 1.5, 0, 1)
alfa[alfa < 0.06] = 0
color = np.clip((img - fondo * (1 - alfa[..., None])) / np.maximum(alfa[..., None], 1e-3), 0, 255)
# el color recuperado solo es confiable donde la tinta es firme: en los bordes se usa el del trazo
# firme más cercano (así no queda un halo oscuro alrededor de las líneas)
from scipy import ndimage
seguro = alfa > 0.45
_, (iy, ix) = ndimage.distance_transform_edt(~seguro, return_indices=True)
color = np.where(seguro[..., None], color, color[iy, ix])
color = np.where(alfa[..., None] > 0.02, color, 0)

out = Image.fromarray(np.dstack([color, alfa * 255]).astype(np.uint8), "RGBA")
out = out.crop(out.getbbox())
out = out.resize((out.width * 2, out.height * 2), Image.LANCZOS)
rgb = out.convert("RGB").filter(ImageFilter.UnsharpMask(2, 60, 2))
rgb.putalpha(out.getchannel("A"))
rgb.save("summer-babe.png", optimize=True)
print("ok", rgb.size)
