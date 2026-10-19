"""Corrige el texto ilegible que inventó Gemini en la foto de la caja de Match.

La pastilla de la carta bordó decía «¿Quaná rame gestas?»; se redibuja con el texto
real, «responde tu pareja», con el mismo ángulo, tamaño y colores de la foto.

Uso:  python3 redes/gemini/corregir_match.py  ->  redes/gemini/match-foto-corregida.jpg
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGINAL = os.path.join(AQUI, "match-gemini-original.jpg")
SALIDA = os.path.join(AQUI, "match-foto-corregida.jpg")

CENTRO = (744, 1160)   # centro de la pastilla en la foto (px)
LARGO, ALTO = 154, 31  # tamaño de la pastilla en la foto (px)
ANGULO = 16.3          # inclinación de la carta (grados, antihorario)
SS = 6                 # sobremuestreo para que el texto quede suave


def colores(foto):
    zona = np.asarray(foto.crop((CENTRO[0] - 60, CENTRO[1] - 14, CENTRO[0] + 60, CENTRO[1] + 14))).reshape(-1, 3)
    brillo = zona.sum(axis=1)
    fondo = tuple(int(c) for c in np.median(zona[brillo > np.percentile(brillo, 70)], axis=0))
    tinta = tuple(int(c) for c in np.median(zona[brillo < np.percentile(brillo, 8)], axis=0))
    return fondo, tinta


def pastilla(fondo, tinta):
    w, h = LARGO * SS, ALTO * SS
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=fondo + (255,))
    fuente = ImageFont.truetype(os.path.join(RAIZ, "fuentes", "Poppins-Medium.ttf"), int(h * 0.5))
    texto = "responde tu pareja"
    caja = d.textbbox((0, 0), texto, font=fuente)
    tx = (w - (caja[2] - caja[0])) / 2 - caja[0]
    ty = (h - (caja[3] - caja[1])) / 2 - caja[1]
    d.text((tx, ty), texto, font=fuente, fill=tinta + (255,))
    img = img.rotate(ANGULO, expand=True, resample=Image.BICUBIC)
    img = img.resize((img.width // SS, img.height // SS), Image.LANCZOS)
    return img.filter(ImageFilter.GaussianBlur(0.35))  # misma suavidad que la foto


def main():
    foto = Image.open(ORIGINAL).convert("RGB")
    fondo, tinta = colores(foto)
    p = pastilla(fondo, tinta)
    foto.paste(p, (CENTRO[0] - p.width // 2, CENTRO[1] - p.height // 2), p)
    foto.save(SALIDA, quality=95)
    print("ok", os.path.basename(SALIDA), "fondo", fondo, "tinta", tinta)


if __name__ == "__main__":
    main()
