"""Corrige los textos deformados que inventó la IA en la foto de Match en el living.

Uso:  python3 redes/ia-feed/corregir.py  ->  match-ia-corregida.jpg

Cada superficie con texto (frente de la caja, carta de arriba del mazo, carta del abanico,
carta en la mano) se reemplaza por el arte real, deformado en perspectiva sobre los cuatro
vértices medidos en la foto. Después se le aplica la luz de la foto (cociente de las versiones
muy desenfocadas) y un desenfoque mínimo, para que no quede más nítido que el resto.
"""
import os
import sys
import tempfile

import cv2
import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
REDES = os.path.dirname(AQUI)
RAIZ = os.path.dirname(REDES)
sys.path.insert(0, REDES)
import foto_producto as fp  # noqa: E402

CARTAS = os.path.join(RAIZ, "match", "match-cartas.pdf")

# (arte, vértices del rectángulo útil en el arte [TL, TR, BR, BL], vértices en la foto, zona del arte a usar)
PIEZAS = []


def pegar(foto, arte, origen, destino, mascara_arte, pluma=2.0, luz=True):
    h, w = foto.shape[:2]
    # se achica primero el arte (promediando) al tamaño aproximado que tiene en la foto: así las
    # líneas finas no se cortan en serrucho al deformarlo
    def lado(p, a, b):
        return np.hypot(*np.subtract(p[b], p[a]))
    # la compresión que manda es la del lado más achicado (en una carta acostada es la profundidad)
    f = min(1.0, 1.3 * min(lado(destino, 0, 1) / lado(origen, 0, 1), lado(destino, 1, 2) / lado(origen, 1, 2)))
    arte = cv2.resize(arte, None, fx=f, fy=f, interpolation=cv2.INTER_AREA)
    mascara_arte = cv2.resize(mascara_arte, None, fx=f, fy=f, interpolation=cv2.INTER_AREA)
    origen = [(x * f, y * f) for x, y in origen]
    m = cv2.getPerspectiveTransform(np.float32(origen), np.float32(destino))
    deformado = cv2.warpPerspective(arte, m, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    mascara = cv2.warpPerspective(mascara_arte, m, (w, h), flags=cv2.INTER_LINEAR)
    mascara = cv2.GaussianBlur(mascara, (0, 0), pluma)[..., None]
    if luz:
        # luz de la foto: se igualan los negros y los claros de la pieza con los de la foto (por canal),
        # sin cocientes locales, que dejaban halos alrededor de las líneas
        sel = mascara[..., 0] > 0.5
        for c in range(3):
            fo, de = foto[..., c][sel], deformado[..., c][sel]
            f_bajo, f_alto = np.percentile(fo, 10), np.percentile(fo, 99.5)
            d_bajo, d_alto = np.percentile(de, 10), np.percentile(de, 99.5)
            deformado[..., c] = (deformado[..., c] - d_bajo) * (f_alto - f_bajo) / max(d_alto - d_bajo, 1) + f_bajo
    deformado = cv2.GaussianBlur(deformado, (0, 0), 0.55)
    return foto * (1 - mascara) + deformado * mascara


def borrar_texto(foto, x0, y0, x1, y1):
    """Dentro del rectángulo, las letras claras se reemplazan por el fondo (promedio de lo que no es letra)."""
    zona = foto[y0:y1, x0:x1]
    gris = zona.mean(axis=2)
    letra = gris > np.median(gris) + 22
    letra = cv2.dilate(letra.astype(np.uint8), np.ones((3, 3), np.uint8), iterations=2).astype(bool)
    peso = (~letra).astype(np.float32)
    den = cv2.GaussianBlur(peso, (0, 0), 6)
    fondo = np.stack([cv2.GaussianBlur(zona[..., c] * peso, (0, 0), 6) / np.maximum(den, 1e-3) for c in range(3)], 2)
    suave = cv2.GaussianBlur(letra.astype(np.float32), (0, 0), 1.0)[..., None]
    salida = foto.copy()
    salida[y0:y1, x0:x1] = zona * (1 - suave) + fondo * suave
    return salida


def rect(ancho, alto, x0=0, y0=0, x1=None, y1=None):
    mk = np.zeros((alto, ancho), np.float32)
    mk[y0:y1 if y1 else alto, x0:x1 if x1 else ancho] = 1
    return mk


def main():
    foto = np.asarray(Image.open(os.path.join(AQUI, "match-ia.jpg")).convert("RGB")).astype(np.float32)
    # 1 · frente de la caja: el marco crema del arte (35,35)-(733,1028) va sobre el marco de la foto
    frente = np.asarray(Image.open(os.path.join(REDES, "caras", "match-frente.png")).convert("RGB")).astype(np.float32)
    origen = [(35, 35), (733, 35), (733, 1028), (35, 1028)]
    destino = [(452, 1338), (674, 1300), (678, 1638), (452, 1690)]
    foto = pegar(foto, frente, origen, destino, rect(768, 1063, 14, 165, 754, 1050))
    # 2 · cartas: el arte es la carta al corte (744 x 1039 a 300 dpi); las esquinas se redondean
    def carta(nombre):
        return np.asarray(Image.open(os.path.join(AQUI, nombre)).convert("RGB")).astype(np.float32)
    esquinas = [(0, 0), (744, 0), (744, 1039), (0, 1039)]
    redonda = np.zeros((1039, 744), np.float32)
    cv2.rectangle(redonda, (0, 40), (743, 998), 1, -1)
    cv2.rectangle(redonda, (40, 0), (703, 1038), 1, -1)
    for cx, cy in ((40, 40), (703, 40), (703, 998), (40, 998)):
        cv2.circle(redonda, (cx, cy), 40, 1, -1)
    # carta de arriba del mazo: boca abajo (el dorso se lee mejor que una pregunta tan en escorzo)
    foto = pegar(foto, carta("_dorso-preg.png"), esquinas, [(805, 1461), (962, 1528), (830, 1557), (686, 1515)], redonda, 1.2)
    # carta de adelante del abanico
    foto = pegar(foto, carta("_preg-comida.png"), esquinas, [(672, 1700), (885, 1712), (800, 1842), (590, 1822)], redonda, 1.2)
    # carta de adelante en la mano izquierda: los dedos que la tapan quedan por encima
    antes = foto.copy()
    foto = pegar(foto, carta("_preg-mate.png"), esquinas, [(436, 688), (550, 703), (523, 850), (405, 836)], redonda, 1.2)
    r, g, b = antes[..., 0], antes[..., 1], antes[..., 2]
    piel = ((r > 140) & (r - b > 25) & (g > 90)).astype(np.float32)
    piel[:812] = 0  # los dedos solo tapan la parte de abajo; arriba, lo claro es texto de la carta
    piel = cv2.GaussianBlur(piel, (0, 0), 1.2)[..., None]
    foto = antes * piel + foto * (1 - piel)

    # 3 · restos de texto inventado en cartas medio tapadas: se borran con el color de la carta
    for x0, y0, x1, y1 in ((1186, 705, 1224, 765), (1160, 703, 1184, 757),   # mano derecha
                           (818, 1742, 895, 1790),                            # abanico, segunda carta
                           (380, 768, 404, 818)):                             # mano izquierda, carta del medio
        foto = borrar_texto(foto, x0, y0, x1, y1)

    Image.fromarray(foto.clip(0, 255).astype(np.uint8)).save(os.path.join(AQUI, "match-ia-corregida.jpg"), quality=95)
    print("ok")


if __name__ == "__main__":
    main()
