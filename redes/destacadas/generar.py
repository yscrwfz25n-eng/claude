"""Portadas de historias destacadas de Oficina Gráfica (1080 x 1920).

Uso:  python3 redes/destacadas/generar.py  ->  juegos.png, libros.png, … y vista-perfil.png

Ícono de línea en tinta, con un punto azul (el del centro de la mira del logo) como acento,
sobre papel. Todo dentro del círculo central que muestra Instagram.
"""
import os
import subprocess

from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
TINTA, VIVO, PAPEL = "#142A40", "#1C82D9", "#EEE7D8"

# íconos dibujados alrededor de (0, 0), unos 440 px de ancho
ICONOS = {
    "juegos": f"""
      <g transform="rotate(-14) translate(-70 0)"><rect x="-95" y="-135" width="190" height="270" rx="24"/></g>
      <g transform="rotate(12) translate(70 -10)"><rect x="-95" y="-135" width="190" height="270" rx="24" fill="{PAPEL}"/>
        <path d="M0 -40C-22 -78 -72 -60 -60 -20C-50 10 -10 30 0 50C10 30 50 10 60 -20C72 -60 22 -78 0 -40Z"/></g>
      <circle cx="58" cy="128" r="17" fill="{VIVO}" stroke="none"/>""",
    "libros": f"""
      <path d="M0 -110C-60 -150 -150 -150 -210 -120V140C-150 110 -60 110 0 150Z"/>
      <path d="M0 -110C60 -150 150 -150 210 -120V140C150 110 60 110 0 150Z"/>
      <path d="M0 -110V150"/>
      <path d="M-160 -60C-120 -75 -80 -75 -45 -60M-160 -10C-120 -25 -80 -25 -45 -10M45 -60C80 -75 120 -75 160 -60"/>
      <circle cx="102" cy="0" r="17" fill="{VIVO}" stroke="none"/>""",
    "pedidos": f"""
      <path d="M-190 -120H190Q210 -120 210 -100V80Q210 100 190 100H-40L-120 160V100H-190Q-210 100 -210 80V-100Q-210 -120 -190 -120Z"/>
      <circle cx="-90" cy="-10" r="17" fill="{TINTA}" stroke="none"/><circle cx="0" cy="-10" r="17" fill="{TINTA}" stroke="none"/>
      <circle cx="90" cy="-10" r="17" fill="{VIVO}" stroke="none"/>""",
    "envios": f"""
      <path d="M-190 -70L0 -150L190 -70V110L0 190L-190 110Z"/>
      <path d="M-190 -70L0 10L190 -70M0 10V190"/>
      <path d="M-95 -110L95 -30V30"/>
      <circle cx="-95" cy="95" r="17" fill="{VIVO}" stroke="none"/>""",
    "proceso": f"""
      <path d="M-120 -60V-160H120V-60"/>
      <rect x="-200" y="-60" width="400" height="190" rx="30"/>
      <path d="M-120 60H120V190H-120Z" fill="{PAPEL}"/>
      <path d="M-70 105H70M-70 145H30"/>
      <circle cx="140" cy="0" r="17" fill="{VIVO}" stroke="none"/>""",
    "tips": f"""
      <path d="M-70 90C-70 40 -130 10 -130 -60C-130 -135 -70 -185 0 -185C70 -185 130 -135 130 -60C130 10 70 40 70 90Z"/>
      <path d="M-60 140H60M-40 185H40"/>
      <path d="M-30 90V20L0 -10L30 20V90"/>
      <path d="M190 -170V-110M160 -140H220M-190 -140V-100M-210 -120H-170"/>
      <circle cx="0" cy="-10" r="17" fill="{VIVO}" stroke="none"/>""",
    "clientes": f"""
      <path d="M0 -60C-50 -160 -200 -130 -195 -20C-190 70 -60 130 0 185C60 130 190 70 195 -20C200 -130 50 -160 0 -60Z"/>
      <path d="M-80 10L-20 70L95 -50"/>
      <circle cx="0" cy="185" r="17" fill="{VIVO}" stroke="none"/>""",
    "eventos": f"""
      <rect x="-190" y="-140" width="380" height="320" rx="30"/>
      <path d="M-190 -50H190M-100 -185V-100M100 -185V-100"/>
      <path d="M-110 30H-70M-20 30H20M70 30H110M-110 110H-70M-20 110H20"/>
      <circle cx="90" cy="110" r="38" fill="{PAPEL}"/><circle cx="90" cy="110" r="17" fill="{VIVO}" stroke="none"/>
      <path d="M196 -186L216 -220M228 -146L264 -156M-208 -182L-228 -214" stroke-width="18"/>""",
}
NOMBRES = {"juegos": "Juegos", "libros": "Libros", "pedidos": "Pedidos", "envios": "Envíos",
           "proceso": "Proceso", "tips": "Tips", "clientes": "Clientes",
           "eventos": "Eventos"}


def html(icono):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;}}</style></head><body>
<svg width="1080" height="1920" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="mano"><feTurbulence type="fractalNoise" baseFrequency="0.02 0.03" numOctaves="2" seed="4" result="t"/>
      <feDisplacementMap in="SourceGraphic" in2="t" scale="6" xChannelSelector="R" yChannelSelector="G"/></filter>
    <filter id="grano"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch"/>
      <feColorMatrix values="0 0 0 0 0.08  0 0 0 0 0.16  0 0 0 0 0.25  0 0 0 0.5 0"/></filter>
  </defs>
  <rect width="1080" height="1920" fill="{PAPEL}"/>
  <g transform="translate(540 960) scale(.95)" fill="none" stroke="{TINTA}" stroke-width="22" stroke-linecap="round"
     stroke-linejoin="round" filter="url(#mano)">{icono}</g>
  <!-- marcas de corte alrededor del círculo visible: firma de imprenta -->
  <g stroke="{TINTA}" stroke-width="5" opacity=".35">
    <path d="M190 610H250M220 580V640M890 610H830M860 580V640M190 1310H250M220 1280V1340M890 1310H830M860 1280V1340"/>
  </g>
  <rect width="1080" height="1920" filter="url(#grano)" opacity=".25"/>
</svg></body></html>"""


def main():
    for nombre, icono in ICONOS.items():
        ruta = os.path.join(AQUI, f"_{nombre}.html")
        png = os.path.join(AQUI, f"{nombre}.png")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(html(icono))
        subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", "--window-size=1080,2100", "--virtual-time-budget=3000",
                        f"--screenshot={png}", "file://" + ruta], check=True, capture_output=True)
        Image.open(png).convert("RGB").crop((0, 0, 1080, 1920)).save(png)
        os.remove(ruta)
    vista_perfil()
    print("ok", len(ICONOS), "portadas + vista-perfil.png")


def vista_perfil():
    """Cómo se ven en el perfil: círculos con el nombre abajo, en modo claro y oscuro."""
    from PIL import ImageFont
    fuente = ImageFont.truetype(os.path.join(os.path.dirname(os.path.dirname(AQUI)), "fuentes", "Poppins-Regular.ttf"), 26)
    d_circ, paso = 170, 220
    w = paso * len(ICONOS) + 40
    hoja = Image.new("RGB", (w, 2 * 280), "white")
    for fila, (fondo, texto) in enumerate((("#FFFFFF", "#000000"), ("#000000", "#F5F5F5"))):
        hoja.paste(fondo, (0, fila * 280, w, (fila + 1) * 280))
        d = ImageDraw.Draw(hoja)
        for i, nombre in enumerate(ICONOS):
            img = Image.open(os.path.join(AQUI, f"{nombre}.png")).crop((165, 645, 915, 1395)).resize((d_circ, d_circ))
            mascara = Image.new("L", (d_circ, d_circ), 0)
            ImageDraw.Draw(mascara).ellipse((0, 0, d_circ, d_circ), fill=255)
            x, y = 40 + i * paso, fila * 280 + 30
            d.ellipse((x - 6, y - 6, x + d_circ + 6, y + d_circ + 6), outline="#C7C7C7", width=2)
            hoja.paste(img, (x, y), mascara)
            ancho = d.textlength(NOMBRES[nombre], font=fuente)
            d.text((x + (d_circ - ancho) / 2, y + d_circ + 16), NOMBRES[nombre], font=fuente, fill=texto)
    hoja.save(os.path.join(AQUI, "vista-perfil.png"))


if __name__ == "__main__":
    main()
