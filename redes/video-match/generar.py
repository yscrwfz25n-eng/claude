"""Video 9:16 (1080 x 1920, 18 s, 30 fps, sin audio) para la preventa de Match, hecho con el arte
real de las cartas y la caja. La voz en off se graba aparte (guion en GUION.md).

Uso:  python3 redes/video-match/generar.py  ->  redes/video-match/match-preventa.mp4

Escenas: 0-3 s pregunta de arranque · 3-6,5 s dos cartas «responde tu pareja» · 6,5-10 s el reto ·
10-13,5 s la caja · 13,5-18 s preventa y pedido por MD. Los textos quedan entre y = 250 y y = 1600.
"""
import math
import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
REDES = os.path.dirname(AQUI)
RAIZ = os.path.dirname(REDES)
sys.path.insert(0, REDES)
import foto_producto as fp  # noqa: E402

W, H, FPS, DURACION = 1080, 1920, 30, 18.0
PAPEL, TINTA, VIVO, CELESTE = (238, 231, 216), (20, 42, 64), (28, 130, 217), (155, 208, 239)
F = os.path.join(RAIZ, "fuentes")
BUNGEE = lambda s: ImageFont.truetype(os.path.join(F, "Bungee-Regular.ttf"), s)  # noqa: E731
KARLA = lambda s: ImageFont.truetype(os.path.join(F, "Karla[wght].ttf"), s)  # noqa: E731
MARKER = lambda s: ImageFont.truetype(os.path.join(F, "PermanentMarker-Regular.ttf"), s)  # noqa: E731


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def tramo(t, a, b):
    return ease((t - a) / (b - a))


def cargar_cartas():
    pdf = os.path.join(RAIZ, "match", "match-cartas.pdf")
    with tempfile.TemporaryDirectory() as tmp:
        cartas = {"dorso": fp.carta(pdf, 2, 0, tmp), "comida": fp.carta(pdf, 1, 1, tmp),
                  "miedo": fp.carta(pdf, 1, 5, tmp), "reto": fp.carta(pdf, 21, 8, tmp)}
    salida = {}
    for k, im in cartas.items():
        im = im.convert("RGBA").resize((560, round(560 * im.height / im.width)), Image.LANCZOS)
        # esquinas redondeadas
        m = Image.new("L", im.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius=34, fill=255)
        im.putalpha(m)
        salida[k] = im
    return salida


def con_sombra(lienzo, im, cx, cy, ang=0.0, escala=1.0, alfa=1.0, escala_x=1.0):
    if alfa <= 0 or escala <= 0 or escala_x <= 0.01:
        return
    w, h = max(1, round(im.width * escala * escala_x)), max(1, round(im.height * escala))
    im = im.resize((w, h), Image.BICUBIC).rotate(ang, expand=True, resample=Image.BICUBIC)
    if alfa < 1:
        a = im.getchannel("A").point(lambda v: int(v * alfa))
        im.putalpha(a)
    sombra = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sombra.putalpha(im.getchannel("A").point(lambda v: int(v * 0.35)))
    sombra = sombra.filter(ImageFilter.GaussianBlur(18))
    x, y = round(cx - im.width / 2), round(cy - im.height / 2)
    lienzo.alpha_composite(sombra, (x + 10, y + 26))
    lienzo.alpha_composite(im, (x, y))


def texto(d, s, y, fuente, color, alfa=1.0, cx=W / 2):
    if alfa <= 0:
        return
    caja = d.textbbox((0, 0), s, font=fuente)
    col = color + (int(255 * alfa),)
    d.text((cx - (caja[2] - caja[0]) / 2 - caja[0], y), s, font=fuente, fill=col)


def fondo(color):
    return Image.new("RGBA", (W, H), color + (255,))


def firma(lienzo, color, y=1660):
    d = ImageDraw.Draw(lienzo)
    f = MARKER(40)
    s = "Oficina Gráfica"
    ancho = d.textlength(s, font=f) + 62
    x0 = (W - ancho) / 2
    cx, cy, r = x0 + 24, y + 26, 17
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=color, width=6)
    d.line((cx, cy - r - 8, cx, cy + r + 8), fill=color, width=6)
    d.line((cx - r - 8, cy, cx + r + 8, cy), fill=color, width=6)
    d.ellipse((cx - 6, cy - 6, cx + 6, cy + 6), fill=(59, 127, 208))
    d.text((x0 + 62, y), s, font=f, fill=color)


def escena_cartas(t, C):
    """0 a 10 s, sobre fondo tinta."""
    lienzo = fondo(TINTA)
    d = ImageDraw.Draw(lienzo, "RGBA")
    if t < 3.0:
        a = tramo(t, 0.1, 0.7)
        texto(d, "¿CUÁNTO TE CONOCE", 300, BUNGEE(80), PAPEL, a)
        texto(d, "TU PAREJA?", 400, BUNGEE(96), CELESTE, a)
        y = 1040 + (1 - tramo(t, 0.8, 1.6)) * 900
        con_sombra(lienzo, C["dorso"], W / 2, y, -3)
    elif t < 6.5:
        texto(d, "RESPONDE TU PAREJA", 300, BUNGEE(64), CELESTE, 1)
        texto(d, "Si acierta: ¡match!", 395, KARLA(52), PAPEL, tramo(t, 3.2, 3.7))
        giro = tramo(t, 3.0, 3.5)
        if giro < 0.5:
            con_sombra(lienzo, C["dorso"], W / 2, 1040, -3, escala_x=1 - giro * 2)
        else:
            con_sombra(lienzo, C["comida"], W / 2, 1040, -3, escala_x=(giro - 0.5) * 2)
        if t >= 4.8:
            p = tramo(t, 4.8, 5.5)
            con_sombra(lienzo, C["miedo"], W / 2 + 60 + (1 - p) * 800, 1080, 5 - (1 - p) * 20)
    else:
        con_sombra(lienzo, C["comida"], W / 2 - 40, 1040, -6, alfa=0.55)
        con_sombra(lienzo, C["miedo"], W / 2 + 60, 1080, 5, alfa=0.55)
        a1 = tramo(t, 6.6, 7.1)
        texto(d, "SI NO ADIVINA…", 300, BUNGEE(76), PAPEL, a1)
        texto(d, "…LE TOCA UN RETO", 400, BUNGEE(76), CELESTE, tramo(t, 7.8, 8.3))
        p = tramo(t, 7.0, 7.8)
        con_sombra(lienzo, C["reto"], W / 2 + (1 - p) * 900, 1100, -4 + (1 - p) * 25, escala=1.05)
    return lienzo


def escena_caja(t, caja):
    """10 a 13,5 s, sobre papel."""
    lienzo = fondo(PAPEL)
    d = ImageDraw.Draw(lienzo, "RGBA")
    a = tramo(t, 10.2, 10.8)
    texto(d, "90 PREGUNTAS", 300, BUNGEE(92), TINTA, a)
    texto(d, "30 RETOS", 410, BUNGEE(92), VIVO, tramo(t, 10.5, 11.1))
    esc = 0.8 + 0.2 * tramo(t, 10.0, 11.0) + 0.03 * (t - 10)
    con_sombra(lienzo, caja, W / 2, 1060, -4, escala=esc)
    texto(d, "Match · preguntas y retos para parejas", 1520, KARLA(42), TINTA, tramo(t, 11.0, 11.6))
    return lienzo


def escena_preventa(t):
    """13,5 a 18 s, sobre azul."""
    lienzo = fondo(VIVO)
    d = ImageDraw.Draw(lienzo, "RGBA")
    pop = tramo(t, 13.6, 14.1)
    tam = int(150 * (0.7 + 0.3 * pop))
    texto(d, "PREVENTA", 560 + (150 - tam) / 2, BUNGEE(tam), PAPEL, pop)
    texto(d, "cupos limitados", 760, KARLA(64), TINTA, tramo(t, 14.3, 14.8))
    texto(d, "Llega antes de Navidad 📦".replace(" 📦", ""), 860, KARLA(52), PAPEL, tramo(t, 14.8, 15.3))
    a = tramo(t, 15.4, 15.9)
    if a > 0:
        f = KARLA(56)
        s = "Escribinos por MD"
        ancho = d.textlength(s, font=f) + 120
        x0, y0 = (W - ancho) / 2, 1020
        d.rounded_rectangle((x0, y0, x0 + ancho, y0 + 120), radius=60, fill=PAPEL + (int(255 * a),))
        texto(d, s, y0 + 26, f, TINTA, a)
    firma(lienzo, PAPEL, 1500)
    return lienzo


def cuadro(t, C, caja):
    def base(tt):
        if tt < 10.0:
            return escena_cartas(tt, C)
        if tt < 13.5:
            return escena_caja(tt, caja)
        return escena_preventa(tt)
    for corte in (10.0, 13.5):  # fundido corto entre escenas
        if corte <= t < corte + 0.25:
            return Image.blend(base(corte - 0.001).convert("RGB"), base(t).convert("RGB"), (t - corte) / 0.25)
    return base(t).convert("RGB")


def main():
    C = cargar_cartas()
    caja = Image.open(os.path.join(REDES, "regalito", "caja-match.png")).convert("RGBA")
    caja = caja.resize((560, round(560 * caja.height / caja.width)), Image.LANCZOS)
    tmp = tempfile.mkdtemp()
    try:
        total = int(DURACION * FPS)
        for i in range(total):
            cuadro(i / FPS, C, caja).save(os.path.join(tmp, f"{i:04d}.png"))
        salida = os.path.join(AQUI, "match-preventa.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "%04d.png"),
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", salida], check=True)
        cuadro(2.5, C, caja).save(os.path.join(AQUI, "_vista-1.png"))
        cuadro(5.8, C, caja).save(os.path.join(AQUI, "_vista-2.png"))
        cuadro(9.0, C, caja).save(os.path.join(AQUI, "_vista-3.png"))
        cuadro(12.0, C, caja).save(os.path.join(AQUI, "_vista-4.png"))
        cuadro(17.0, C, caja).save(os.path.join(AQUI, "_vista-5.png"))
        print("ok", os.path.relpath(salida, RAIZ))
    finally:
        shutil.rmtree(tmp)


if __name__ == "__main__":
    main()
