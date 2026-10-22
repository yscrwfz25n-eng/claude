"""Pasa al español (argentino) los textos de la foto de papelería de casamiento.

Uso:  python3 redes/menu-boda/traducir.py  ->  menu-boda-es.jpg

1 · borra los textos originales: en cada zona detecta los píxeles de letra (oscuros sobre papel claro,
    o claros sobre la tarjeta bordó), descarta las líneas decorativas largas y rellena con cv2.inpaint.
2 · dibuja los textos nuevos con Chromium (SVG transparente a 2x) en la misma posición, inclinación y
    curva que los originales, y los compone sobre la foto con un desenfoque mínimo para que no queden
    más nítidos que la foto.
La foto original no se versiona (original.jpg).
"""
import os
import subprocess

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

AQUI = os.path.dirname(os.path.abspath(__file__))
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
W, H = 928, 1152
ESCALA = 2

# ---------- zonas a limpiar: (polígono, tipo de letra) ----------
ZONAS = [
    ([(250, 168), (400, 168), (475, 240), (458, 272), (390, 230), (250, 206)], "oscura"),   # título bebidas
    ([(315, 276), (468, 276), (468, 532), (315, 532)], "oscura"),                          # lista bebidas
    ([(548, 308), (532, 282), (600, 238), (700, 232), (775, 262), (765, 290), (700, 262), (600, 268), (560, 310)], "oscura"),  # título comida
    ([(560, 292), (745, 318), (742, 625), (590, 605), (540, 330)], "oscura"),              # lista comida
    ([(125, 640), (300, 650), (300, 700), (125, 664)], "clara"),                           # título tarjeta
    ([(15, 790), (222, 800), (222, 885), (15, 880)], "clara"),                            # ingredientes 1
    ([(180, 852), (310, 858), (310, 945), (180, 940)], "clara"),                          # ingredientes 2
    ([(300, 655), (494, 662), (494, 736), (300, 726)], "oscura"),                          # tarjetita de nombres
    ([(276, 680), (296, 684), (300, 702), (280, 700)], "clara-borde"),                     # resto de letra junto a la tarjetita
]

TINTA = "#5E2128"
CREMA = "#F4E8DE"
TARJETA_NOMBRE = "#6A1F2C"


def mascara_texto(img, poligono, tipo):
    zona = Image.new("L", (W, H), 0)
    ImageDraw.Draw(zona).polygon(poligono, fill=255)
    zona = np.asarray(zona) > 0
    gris = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY).astype(int)
    fondo = cv2.medianBlur(gris.astype(np.uint8), 15).astype(int)
    if tipo == "oscura":
        letra = fondo - gris > 14
    elif tipo == "clara":
        letra = gris - fondo > 18
    else:  # "clara-borde": junto a la tarjetita rosa el fondo local sale más claro; se compara con el bordó
        letra = gris > 120
    letra &= zona
    # fuera las líneas decorativas: componentes largos y finos
    etiquetas, n = ndimage.label(letra)
    for i, sl in enumerate(ndimage.find_objects(etiquetas), 1):
        h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        if max(h, w) > 45 and min(h, w) < 7:
            letra[sl][etiquetas[sl] == i] = False
    return ndimage.binary_dilation(letra, iterations=3)


def rellenar(img, sal, letras, superficie):
    """Reemplaza las letras por el fondo suavizado de la misma superficie (papel, tarjeta o tarjetita)."""
    relleno = ndimage.binary_dilation(letras, iterations=3) & superficie
    peso = (superficie & ~ndimage.binary_dilation(letras, iterations=7)).astype(float)
    fondo = np.zeros_like(sal)
    listo = np.zeros((H, W), bool)
    for sigma in (7, 16, 32, 64):  # si cerca no hay fondo limpio, se busca más lejos
        den = cv2.GaussianBlur(peso, (0, 0), sigma)
        ok = (den > 0.08) & ~listo
        for c in range(3):
            num = cv2.GaussianBlur(img[..., c].astype(float) * peso, (0, 0), sigma)
            fondo[..., c] = np.where(ok, num / np.maximum(den, 1e-6), fondo[..., c])
        listo |= ok
    grano = np.random.default_rng(7).normal(0, 1.6, (H, W))[..., None]
    relleno &= listo  # donde no se encontró fondo de la misma superficie, se deja la foto como está
    suave = cv2.GaussianBlur(relleno.astype(float), (0, 0), 1.0)[..., None] * superficie[..., None]
    return sal * (1 - suave) + (fondo + grano) * suave


def limpiar(img):
    """Borra los textos zona por zona.

    El fondo de reemplazo se estima solo con píxeles de la misma superficie (color parecido a la mediana
    de la zona) y lejos de cualquier letra: así no se mezclan el mantel, el plato o el tinte rosado que
    la compresión JPEG deja alrededor de las letras.
    """
    sal = img.astype(float).copy()
    for poligono, tipo in ZONAS:
        letras = mascara_texto(img, poligono, tipo)
        zona = Image.new("L", (W, H), 0)
        ImageDraw.Draw(zona).polygon(poligono, fill=255)
        zona = np.asarray(zona) > 0
        ancha = ndimage.binary_dilation(zona, iterations=25)
        base = zona & ~ndimage.binary_dilation(letras, iterations=4)
        ref = np.median(img[base], axis=0)
        parecido = np.abs(img.astype(float) - ref).max(axis=2) < 24
        superficie = ndimage.binary_closing(parecido & ancha, iterations=6) & ancha
        sal = rellenar(img, sal, letras & superficie, superficie)
    return sal.clip(0, 255).astype(np.uint8)


def bloque(lineas, alto_linea, anchor, size, color, peso_titulo=None):
    out = []
    y = 0
    for texto, es_titulo in lineas:
        if texto is None:
            y += alto_linea * 0.9
            continue
        if es_titulo:
            out.append(f'<text y="{y:.1f}" font-family="DMSerif" font-size="{size * 0.95}" letter-spacing="0.6" '
                       f'fill="{color}" text-anchor="{anchor}">{texto}</text>')
        else:
            out.append(f'<text y="{y:.1f}" font-family="DMSerif" font-size="{size}" fill="{color}" '
                       f'text-anchor="{anchor}">{texto}</text>')
        y += alto_linea
    return "\n".join(out)


BEBIDAS = [("SIN ALCOHOL", True), ("Coca-Cola / Coca Zero", False), ("Sprite / Fanta", False), ("Agua tónica", False),
           ("Agua con y sin gas", False), ("Limonada con menta y jengibre", False), ("Jugo de naranja exprimido", False),
           ("Pomelo rosado", False), ("Licuado de frutilla", False), (None, False),
           ("CAFÉ Y TÉ", True), ("Café, cortado o lágrima", False), ("Espresso doble", False), ("Té en hebras", False),
           ("(Manzanilla, menta, frutos rojos o cedrón)", False), ("Submarino con chocolate en barra", False), (None, False),
           ("CON ALCOHOL", True), ("Fernet con coca", False), ("Gin tonic", False), ("Aperol spritz", False),
           ("Gancia batido", False), ("Malbec y Torrontés", False), ("Espumante extra brut", False), ("Cerveza tirada", False)]

COMIDA = [("ENTRADA", True), ("Empanadas de carne", False), ("cortada a cuchillo y de humita", False),
          ("Provoleta con orégano y oliva", False), ("Tabla de fiambres: jamón crudo,", False),
          ("salame de Tandil y quesos", False), ("Choripán en pan casero", False), ("con chimichurri y criolla", False),
          (None, False),
          ("PRINCIPAL", True), ("Bife de chorizo a punto", False), ("con papas rústicas", False),
          ("Ojo de bife con puré de calabaza", False), ("Sorrentinos de jamón y queso", False),
          ("con salsa rosa y albahaca", False), ("Ensalada de rúcula y parmesano", False), (None, False),
          ("POSTRE", True), ("Panqueques con dulce de leche", False), ("Flan casero con crema", False),
          ("Vigilante: queso y dulce", False), ("Helado de dulce de leche", False), ("Mesa dulce a la medianoche", False)]

TRAGO_1 = [("Cynar Julep", True), ("Cynar", False), ("jugo de pomelo", False), ("menta fresca", False), ("almíbar", False),
           ("rodaja de limón", False)]
TRAGO_2 = [("Fernet con coca", True), ("Fernet", False), ("Coca-Cola", False), ("mucho hielo", False), ("vaso alto", False),
           ("y amigos", False)]


def titulo_trago(lineas):
    """En la tarjeta bordó el nombre del trago va más marcado que los ingredientes."""
    out, y = [], 0
    for texto, es_titulo in lineas:
        peso = 'stroke="#F4E8DE" stroke-width="0.35"' if es_titulo else ""
        size = 12.2 if es_titulo else 12
        out.append(f'<text y="{y:.1f}" font-family="DMSerif" font-size="{size}" fill="{CREMA}" {peso} '
                   f'text-anchor="middle" letter-spacing="0.2">{texto}</text>')
        y += 12.4
    return "\n".join(out)


def svg():
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
  @font-face{{font-family:DMSerif;src:url('../../fuentes/DMSerifDisplay-Regular.ttf');}}
  html,body{{margin:0;background:transparent;}}
</style></head><body>
<svg width="{W * ESCALA}" height="{H * ESCALA}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <path id="arco-bebidas" d="M258 189Q392 176 462 258"/>
    <path id="arco-comida" d="M552 300Q650 210 770 282"/>
    <path id="arco-tarjeta" d="M132 652Q215 653 305 693"/>
  </defs>
  <!-- página de bebidas: casi de frente -->
  <text font-family="DMSerif" font-size="13.5" letter-spacing="1.1" fill="{TINTA}"><textPath href="#arco-bebidas">BEBIDAS · BARRA LIBRE</textPath></text>
  <g transform="translate(462 289) rotate(-0.4)">{bloque(BEBIDAS, 10.15, "end", 9.6, TINTA)}</g>
  <!-- página de comida: en perspectiva (las líneas bajan, el margen derecho queda casi vertical) -->
  <text font-family="DMSerif" font-size="13" letter-spacing="1.1" fill="{TINTA}"><textPath href="#arco-comida" startOffset="2">MENÚ · ¡BUEN PROVECHO!</textPath></text>
  <g transform="matrix(1 0.335 -0.072 1 739 350)">{bloque(COMIDA, 10.6, "end", 9.4, TINTA)}</g>
  <!-- tarjeta bordó: los tragos de los novios -->
  <text font-family="DMSerif" font-size="9.4" letter-spacing="1.6" fill="{CREMA}"><textPath href="#arco-tarjeta">LOS TRAGOS DE LOS NOVIOS</textPath></text>
  <g transform="translate(151 806) rotate(4)">{titulo_trago(TRAGO_1)}</g>
  <g transform="translate(242 867) rotate(4)">{titulo_trago(TRAGO_2)}</g>
  <!-- tarjetita con los nombres -->
  <g transform="translate(392 693) rotate(5.5)" font-family="DMSerif" font-size="18.5" fill="{TARJETA_NOMBRE}" text-anchor="middle">
    <text y="0">Lucía y</text><text y="26">Tomás Pérez</text></g>
</svg></body></html>"""


def capa_textos():
    html = os.path.join(AQUI, "_textos.html")
    png = os.path.join(AQUI, "_textos.png")
    with open(html, "w", encoding="utf-8") as f:
        f.write(svg())
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", f"--window-size={W * ESCALA},{H * ESCALA + 200}",
                    "--default-background-color=00000000", "--virtual-time-budget=3000",
                    f"--screenshot={png}", "file://" + html], check=True, capture_output=True)
    capa = Image.open(png).convert("RGBA").crop((0, 0, W * ESCALA, H * ESCALA)).resize((W, H), Image.LANCZOS)
    os.remove(html)
    os.remove(png)
    return capa.filter(ImageFilter.GaussianBlur(0.35))


def mascara_tarjetita(img):
    """Píxeles de la tarjetita rosa: el título de la tarjeta bordó pasa por debajo de ella."""
    r, g, b = [img[..., i].astype(int) for i in range(3)]
    rosa = (r > 170) & (r - b > 35) & (g < 175) & (g > 110)
    rosa = ndimage.binary_closing(rosa, iterations=4)
    caja = np.zeros_like(rosa)
    caja[640:745, 270:490] = True
    return ndimage.binary_fill_holes(rosa & caja)


def main():
    img = np.asarray(Image.open(os.path.join(AQUI, "original.jpg")).convert("RGB"))
    limpia = limpiar(img)
    capa = capa_textos()
    # el título de la tarjeta bordó no se dibuja encima de la tarjetita rosa
    tapa = mascara_tarjetita(img)
    alfa = np.asarray(capa.getchannel("A")).copy()
    zona_titulo = np.zeros_like(tapa)
    zona_titulo[630:705, 100:320] = True
    alfa[tapa & zona_titulo] = 0
    capa.putalpha(Image.fromarray(alfa))
    final = Image.fromarray(limpia).convert("RGBA")
    final.alpha_composite(capa)
    final.convert("RGB").save(os.path.join(AQUI, "menu-boda-es.jpg"), quality=95)
    Image.fromarray(limpia).save(os.path.join(AQUI, "_limpia.jpg"), quality=92)
    print("ok menu-boda-es.jpg")


if __name__ == "__main__":
    main()
