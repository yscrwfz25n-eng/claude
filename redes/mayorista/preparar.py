"""Prepara la foto del pedido y la recorta a 9:16 (1080 x 1920). La foto original (foto.jpg) no se versiona.
Con PIXELAR = True tapa la etiqueta de envío (nombre, dirección, QR y número de seguimiento)."""
from PIL import Image, ImageDraw, ImageFilter

PIXELAR = False  # se decidió mostrar la etiqueta

im = Image.open("foto.jpg").convert("RGB")
if PIXELAR:
    box = (50, 500, 810, 1330)  # etiqueta completa, con margen, en la foto original (1179 x 2096)
    eti = im.crop(box)
    w, h = eti.size
    eti = eti.resize((w // 30, h // 30), Image.BILINEAR).resize((w, h), Image.NEAREST).filter(ImageFilter.GaussianBlur(12))
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((15, 15, w - 15, h - 15), radius=40, fill=255)
    im.paste(eti, box, m.filter(ImageFilter.GaussianBlur(14)))
im = im.resize((1080, round(1080 * im.height / im.width)), Image.LANCZOS)
top = (im.height - 1920) // 2
im.crop((0, top, 1080, top + 1920)).save("_base.jpg", quality=93)
print("ok _base.jpg")
