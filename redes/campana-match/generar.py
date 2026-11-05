"""Creativos de la campaña «Preventa Match» (Meta, objetivo Mensajes), listos para subir.

Uso:  python3 redes/campana-match/generar.py
  -> 1-video-9x16.mp4 / 1-video-4x5.mp4        video con la voz de Cande (anuncio principal)
  -> 2-living-9x16.png / 2-living-4x5.png      foto del living «Esta noche, apagá la tele»
  -> 3-perfume-9x16.png / 3-perfume-4x5.png    «Que no es un perfume»
Las imágenes llevan un sello «PREVENTA $29.900». El video 4:5 se arma del 9:16 rellenando
los costados con el color del borde de cada cuadro (las escenas son de color liso).
"""
import os
import shutil
import subprocess

from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
REDES = os.path.dirname(AQUI)
F = os.path.join(os.path.dirname(REDES), "fuentes")
PRECIO = "$29.900"
ROJO, BEIGE, NEGRO = (200, 16, 46), (230, 213, 184), (15, 13, 13)


def sello(img, cx, cy, r=118, ang=-10):
    """Sello circular rojo «PREVENTA / $29.900», con borde beige."""
    s = 4  # sobremuestreo
    capa = Image.new("RGBA", (2 * r * s + 40, 2 * r * s + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    c = capa.width // 2
    d.ellipse((c - r * s, c - r * s, c + r * s, c + r * s), fill=ROJO + (255,))
    d.ellipse((c - (r - 10) * s, c - (r - 10) * s, c + (r - 10) * s, c + (r - 10) * s), outline=BEIGE + (255,), width=3 * s)
    k = r / 118  # el texto se achica con el sello
    f1 = ImageFont.truetype(os.path.join(F, "Poppins-Bold.ttf"), round(30 * k * s))
    f2 = ImageFont.truetype(os.path.join(F, "DMSerifDisplay-Regular.ttf"), round(54 * k * s))
    for txt, f, dy in (("PREVENTA", f1, -38 * k), (PRECIO, f2, 18 * k)):
        caja = d.textbbox((0, 0), txt, font=f)
        d.text((c - (caja[2] - caja[0]) / 2 - caja[0], c + dy * s - (caja[3] - caja[1]) / 2 - caja[1]), txt, font=f,
               fill=(255, 255, 255, 255))
    capa = capa.rotate(ang, resample=Image.BICUBIC).resize((capa.width // s, capa.height // s), Image.LANCZOS)
    sombra = Image.new("RGBA", capa.size, (0, 0, 0, 0))
    sombra.putalpha(capa.getchannel("A").point(lambda v: int(v * .35)))
    img.alpha_composite(sombra, (cx - capa.width // 2 + 6, cy - capa.height // 2 + 12))
    img.alpha_composite(capa, (cx - capa.width // 2, cy - capa.height // 2))


def con_sello(origen, destino, cx, cy, r=118):
    img = Image.open(os.path.join(REDES, origen)).convert("RGBA")
    sello(img, cx, cy, r)
    img.convert("RGB").save(os.path.join(AQUI, destino))


def videos():
    fuente = os.path.join(REDES, "video-match", "match-preventa-con-audio.mp4")
    shutil.copy(fuente, os.path.join(AQUI, "1-video-9x16.mp4"))
    # fondo: una franja del borde del cuadro estirada a todo el ancho (las escenas son de color liso)
    filtro = ("[0:v]crop=16:ih:24:0,scale=1080:1350,boxblur=8:1[fondo];"
              "[0:v]scale=-2:1350[frente];[fondo][frente]overlay=(W-w)/2:0")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", fuente, "-filter_complex", filtro, "-c:v", "libx264",
                    "-preset", "slow", "-tune", "animation", "-pix_fmt", "yuv420p", "-crf", "15", "-c:a", "copy", "-movflags", "+faststart",
                    os.path.join(AQUI, "1-video-4x5.mp4")], check=True)


def main():
    videos()
    con_sello("ia-feed/posteo.png", "2-living-4x5.png", 900, 560)
    con_sello("ia-feed/historia.png", "2-living-9x16.png", 900, 780)
    con_sello("anuncios/match-feed.png", "3-perfume-4x5.png", 900, 540, 95)
    con_sello("anuncios/match-historia.png", "3-perfume-9x16.png", 880, 720)
    print("ok")


if __name__ == "__main__":
    main()
