"""Tendencia «kinda chic…» (texto amarillo pálido sobre una foto) con los 5 productos + cierre.

Uso:  python3 redes/tendencias/kinda-chic/generar.py  ->  slide-1.png … slide-6.png (1080 x 1350)

Match y Opinólogos usan las fotos de producto finales de Gemini; los libros se montan sobre el
mismo fondo de estudio que foto_producto.py, con sombra suave, para que se vean como fotos.
"""
import os
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

AQUI = os.path.dirname(os.path.abspath(__file__))
REDES = os.path.dirname(os.path.dirname(AQUI))
RAIZ = os.path.dirname(REDES)
sys.path.insert(0, REDES)
import foto_producto as fp  # noqa: E402

W, H = 1080, 1350
AMARILLO = (250, 243, 168)
FUENTE = ImageFont.truetype(os.path.join(RAIZ, "fuentes", "Poppins-Medium.ttf"), 54)

SLIDES = [
    ("foto", "gemini/match-foto-final.jpg", "kinda chic que tu pareja sepa cuál es tu comida favorita"),
    ("foto", "gemini/opinologos-foto-final.jpg", "kinda chic cambiar de opinión en medio de un debate"),
    ("objeto", "regalito/libro-dating-list.png", "kinda chic tener las próximas 100 citas ya planeadas"),
    ("objeto", "vinos/libro-tapa.png", "kinda chic acordarte del nombre del vino de anoche"),
    ("objeto", "regalito/album-alfajores.png", "kinda chic tener un álbum solo para alfajores"),
]


def foto(ruta, bajar=230):
    """Foto a sangre, corrida hacia abajo: arriba se estira la pared lisa para que el texto no tape el producto."""
    img = ImageOps.fit(Image.open(ruta).convert("RGB"), (W, H), Image.LANCZOS, centering=(0.5, 0.6))
    lienzo = Image.new("RGB", (W, H))
    lienzo.paste(img.crop((0, 0, W, 1)).resize((W, bajar)), (0, 0))
    lienzo.paste(img.crop((0, 0, W, H - bajar)), (0, bajar))
    return lienzo


def objeto(ruta, alto, angulo):
    """Producto recortado sobre el fondo de estudio, apoyado en la mesa, con sombra de contacto."""
    lienzo = fp.fondo()
    img = Image.open(ruta).convert("RGBA")
    img = img.resize((round(img.width * alto / img.height), alto), Image.LANCZOS).rotate(angulo, expand=True,
                                                                                     resample=Image.BICUBIC)
    x, y = (W - img.width) // 2, H - img.height - 150
    sombra = Image.new("RGBA", lienzo.size, (0, 0, 0, 0))
    mascara = img.getchannel("A").point(lambda a: int(a * 0.35))
    sombra.paste((40, 30, 20, 255), (x + 18, y + 26), mascara)
    lienzo.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(22)))
    lienzo.alpha_composite(img, (x, y))
    return lienzo.convert("RGB")


def texto(img, frase):
    d = ImageDraw.Draw(img)
    lineas = textwrap.wrap(frase, 25)
    alto_linea = 70
    y = 120
    for linea in lineas:
        ancho = d.textlength(linea, font=FUENTE)
        x = (W - ancho) / 2
        d.text((x + 2, y + 3), linea, font=FUENTE, fill=(0, 0, 0, 90))
        d.text((x, y), linea, font=FUENTE, fill=AMARILLO)
        y += alto_linea
    return img


def cierre():
    """Última slide: el logo sobre papel y «kinda chic pedirlo por MD»."""
    img = fp.fondo().convert("RGB")
    d = ImageDraw.Draw(img)
    marker = ImageFont.truetype(os.path.join(RAIZ, "fuentes", "PermanentMarker-Regular.ttf"), 64)
    cx, cy, r = W // 2, 760, 62
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(20, 42, 64), width=15)
    d.line((cx, cy - r - 30, cx, cy + r + 30), fill=(20, 42, 64), width=15)
    d.line((cx - r - 30, cy, cx + r + 30, cy), fill=(20, 42, 64), width=15)
    d.ellipse((cx - 20, cy - 20, cx + 20, cy + 20), fill=(28, 130, 217))
    ancho = d.textlength("Oficina Gráfica", font=marker)
    d.text(((W - ancho) / 2, cy + 120), "Oficina Gráfica", font=marker, fill=(20, 42, 64))
    return img


def main():
    for i, (tipo, ruta, frase) in enumerate(SLIDES, 1):
        ruta = os.path.join(REDES, ruta)
        if tipo == "foto":
            img = foto(ruta)
        else:
            alto = 720 if "alfajores" not in ruta else 640
            img = objeto(ruta, alto, (-4, 3, -3)[i % 3])
        texto(img, frase).save(os.path.join(AQUI, f"slide-{i}.png"))
    texto(cierre(), "kinda chic pedirlo por MD").save(
        os.path.join(AQUI, f"slide-{len(SLIDES) + 1}.png"))
    print("ok", len(SLIDES) + 1, "slides")


if __name__ == "__main__":
    main()
