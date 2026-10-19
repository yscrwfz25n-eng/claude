"""Foto de producto (render) de las cajas de Opinólogos y Match, con cartas en primer plano.

Uso:  python3 redes/foto_producto.py  ->  redes/foto-producto-cajas.png (1080 x 1350)

Toma el arte real de las cajas y las cartas (los PDF de imprenta), lo arma en 3D con
transformaciones de perspectiva y le suma sombras y luz de estudio.
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, RAIZ)

import generar_caja as caja  # noqa: E402  (medidas y posición de cada cara en el troquel)
import generar_pdf as cartas  # noqa: E402  (grilla de cartas en la hoja A4)

DPI = 300
ESCALA = DPI / 72
SALIDA = os.path.join(AQUI, "foto-producto-cajas.png")
W, H = 1080, 1350


def pagina(pdf, n, tmp):
    base = os.path.join(tmp, f"{os.path.basename(pdf)}-{n}")
    subprocess.run(["pdftoppm", "-r", str(DPI), "-png", "-singlefile", "-f", str(n), "-l", str(n), pdf, base],
                   check=True)
    return Image.open(base + ".png").convert("RGB")


def recorte(img, x, y, w, h, alto_pagina):
    """Recorta un rectángulo dado en puntos PDF (origen abajo a la izquierda)."""
    return img.crop((round(x * ESCALA), round((alto_pagina - y - h) * ESCALA),
                     round((x + w) * ESCALA), round((alto_pagina - y) * ESCALA)))


def caras_de_caja(pdf, tmp):
    img = pagina(pdf, 1, tmp)
    ph = caja.PH
    frente = recorte(img, caja.X_FRENTE, caja.YB, caja.W, caja.H, ph)
    lateral = recorte(img, caja.X_LAT1, caja.YB, caja.D, caja.H, ph)
    tapa = recorte(img, caja.X_DORSO, caja.YT, caja.W, caja.D, ph).rotate(180)
    return frente, lateral, tapa


def coeficientes(destino, origen):
    """Coeficientes de Image.PERSPECTIVE que llevan el cuadrilátero destino al rectángulo origen."""
    import numpy as np
    filas = []
    for (x, y), (u, v) in zip(destino, origen):
        filas.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        filas.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    a = np.array(filas, dtype=float)
    b = np.array([c for p in origen for c in p], dtype=float)
    return np.linalg.solve(a, b).tolist()


def pegar_en_cuad(lienzo, img, cuad, brillo=1.0):
    """Deforma img para que ocupe el cuadrilátero cuad (TL, TR, BR, BL) del lienzo."""
    w, h = img.size
    img = ImageEnhance.Brightness(img).enhance(brillo)
    coef = coeficientes(cuad, [(0, 0), (w, 0), (w, h), (0, h)])
    capa = img.convert("RGBA").transform(lienzo.size, Image.PERSPECTIVE, coef, Image.BICUBIC)
    mascara = Image.new("L", lienzo.size, 0)
    ImageDraw.Draw(mascara).polygon(cuad, fill=255)
    capa.putalpha(ImageChops.multiply(capa.getchannel("A"), mascara))
    lienzo.alpha_composite(capa)


def sombra(lienzo, poligono, desenfoque, opacidad):
    capa = Image.new("L", lienzo.size, 0)
    ImageDraw.Draw(capa).polygon(poligono, fill=int(255 * opacidad))
    capa = capa.filter(ImageFilter.GaussianBlur(desenfoque))
    negro = Image.new("RGBA", lienzo.size, (20, 26, 34, 0))
    negro.putalpha(capa)
    lienzo.alpha_composite(negro)


def caja_3d(lienzo, caras, x0, y0, alto):
    """Caja parada vista de frente-izquierda. (x0, y0) = esquina inferior izquierda del frente."""
    frente, lateral, tapa = caras
    ancho = alto * caja.W / caja.H * 0.9      # el frente gira un poco: se acorta
    prof = alto * caja.D / caja.H * 0.42      # el lateral se ve muy en escorzo
    sube = alto * 0.035                       # lo que "sube" el fondo por la perspectiva
    tl, tr = (x0, y0 - alto), (x0 + ancho, y0 - alto * 0.985 - sube * 0.3)
    br, bl = (x0 + ancho, y0 - sube * 0.3), (x0, y0)
    lat_tl, lat_bl = (x0 - prof, y0 - alto * 0.97 - sube), (x0 - prof, y0 - sube)
    atras_tr = (tr[0] - prof, tr[1] - sube - alto * 0.012)
    # sombra proyectada hacia la derecha y atrás, más una sombra de contacto
    sombra(lienzo, [bl, br, (br[0] + alto * 0.55, br[1] - alto * 0.2), (bl[0] + alto * 0.35, bl[1] - alto * 0.22),
                    lat_bl], alto * 0.06, 0.32)
    sombra(lienzo, [(lat_bl[0], lat_bl[1] + 2), (bl[0], bl[1] + 4), (br[0], br[1] + 4), (br[0] - 4, br[1] - 6),
                    (lat_bl[0] + 4, lat_bl[1] - 6)], 6, 0.55)
    pegar_en_cuad(lienzo, lateral, [lat_tl, tl, bl, lat_bl], brillo=0.78)
    pegar_en_cuad(lienzo, tapa, [lat_tl, atras_tr, tr, tl], brillo=1.06)
    pegar_en_cuad(lienzo, frente, [tl, tr, br, bl], brillo=0.98)
    d = ImageDraw.Draw(lienzo)
    d.line([tl, tr], fill=(255, 255, 255, 90), width=2)  # brillo en la arista de arriba


def carta_en_mesa(lienzo, img, cx, cy, angulo, ancho):
    """Carta apoyada sobre la mesa: rotada y aplastada en vertical por la perspectiva."""
    w, h = img.size
    img = img.resize((round(ancho), round(ancho * h / w)), Image.LANCZOS).convert("RGBA")
    img = img.rotate(angulo, expand=True, resample=Image.BICUBIC)
    img = img.resize((img.width, round(img.height * 0.5)), Image.LANCZOS)
    sombra_c = Image.new("RGBA", img.size, (20, 26, 34, 0))
    sombra_c.putalpha(img.getchannel("A").point(lambda a: int(a * 0.35)).filter(ImageFilter.GaussianBlur(6)))
    lienzo.alpha_composite(sombra_c, (round(cx - img.width / 2 + 5), round(cy - img.height / 2 + 7)))
    lienzo.alpha_composite(img, (round(cx - img.width / 2), round(cy - img.height / 2)))


def fondo():
    """Estudio: pared papel y mesa un tono más oscuro, con luz suave desde arriba a la izquierda."""
    import numpy as np
    yy, xx = np.mgrid[0:H, 0:W]
    horizonte = H * 0.56
    pared = np.array([238, 231, 216], float)
    mesa = np.array([222, 212, 188], float)
    t = np.clip((yy - horizonte) / 60 + 0.5, 0, 1)[..., None]
    base = pared * (1 - t) + mesa * t
    luz = 1.06 - 0.16 * np.hypot((xx - W * 0.25) / W, (yy - H * 0.2) / H)[..., None]
    img = np.clip(base * luz, 0, 255).astype("uint8")
    return Image.fromarray(img, "RGB").convert("RGBA")


def carta(pdf, pagina_n, indice, tmp):
    img = pagina(pdf, pagina_n, tmp)
    x, y = cartas.posicion(indice)
    return recorte(img, x, y, cartas.CW, cartas.CH, cartas.PH)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        op = caras_de_caja(os.path.join(RAIZ, "opinologos-caja.pdf"), tmp)
        ma = caras_de_caja(os.path.join(RAIZ, "match", "match-caja.pdf"), tmp)
        c_op = carta(os.path.join(RAIZ, "opinologos-muestra-imprenta.pdf"), 1, 4, tmp)
        c_ma = carta(os.path.join(RAIZ, "match", "match-cartas.pdf"), 1, 1, tmp)
        c_reto = carta(os.path.join(RAIZ, "match", "match-cartas.pdf"), 21, 0, tmp)
    lienzo = fondo()
    caja_3d(lienzo, op, 215, 870, 630)       # Opinólogos, atrás a la izquierda
    caja_3d(lienzo, ma, 585, 965, 680)       # Match, adelante a la derecha
    carta_en_mesa(lienzo, c_op, 290, 1165, 14, 270)
    carta_en_mesa(lienzo, c_ma, 560, 1205, -6, 270)
    carta_en_mesa(lienzo, c_reto, 815, 1170, -22, 270)
    grano = Image.effect_noise((W, H), 18).convert("L").point(lambda v: 128 + (v - 128) // 3)
    lienzo = ImageChops.overlay(lienzo.convert("RGB"), Image.merge("RGB", (grano, grano, grano)))
    lienzo.save(SALIDA)
    print("ok", os.path.relpath(SALIDA, RAIZ))


if __name__ == "__main__":
    main()
