"""Publicaciones fijadas del perfil (carruseles 4:5, 1080 x 1350), pensadas para no envejecer:
no nombran productos puntuales, así sirven aunque la línea crezca.

Uso:  python3 redes/fijadas/generar.py  ->  quienes-1..4.png, proceso-1..5.png

Las tapas de las tres fijadas comparten diseño (fondo papel, número de fijada, título en Bungee)
para que la primera fila del perfil se lea como un conjunto.
"""
import os
import subprocess

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
TINTA, VIVO, PAPEL, CELESTE = "#142A40", "#1C82D9", "#EEE7D8", "#9BD0EF"

HEAD = """<!doctype html><html lang="es"><head><meta charset="utf-8"><style>
  @font-face{font-family:Bungee;src:url('../../fuentes/Bungee-Regular.ttf');}
  @font-face{font-family:Brico;src:url('../../fuentes/BricolageGrotesque[opsz,wdth,wght].ttf');font-weight:200 800;}
  @font-face{font-family:Karla;src:url('../../fuentes/Karla[wght].ttf');font-weight:200 800;}
  @font-face{font-family:Marker;src:url('../../fuentes/PermanentMarker-Regular.ttf');}
  html,body{margin:0;width:1080px;height:1350px;overflow:hidden;}
  body{position:relative;font-family:Karla;}
  .abs{position:absolute;}
  .bungee{font-family:Bungee;line-height:1;}
  .kick{font-family:Brico;font-weight:700;font-size:30px;letter-spacing:6px;}
  .txt{font-size:40px;font-weight:500;line-height:1.35;}
  .pill{display:inline-block;border-radius:50px;padding:18px 46px;font-family:Brico;font-weight:700;font-size:34px;}
  .sombra{filter:drop-shadow(0 22px 26px rgba(20,42,64,.28));}
</style></head>"""


def mira(tam, color=TINTA):
    return f"""<svg width="{tam}" height="{tam}" viewBox="-4 -4 108 108">
  <defs><filter id="r{tam}" x="-10%" y="-10%" width="120%" height="120%">
    <feTurbulence type="fractalNoise" baseFrequency="0.06 0.08" numOctaves="2" seed="7" result="t"/>
    <feDisplacementMap in="SourceGraphic" in2="t" scale="3.2" xChannelSelector="R" yChannelSelector="G"/></filter></defs>
  <g filter="url(#r{tam})"><circle cx="50" cy="50" r="35.5" fill="none" stroke="{color}" stroke-width="10"/>
  <line x1="50" y1="1" x2="50" y2="99" stroke="{color}" stroke-width="10"/><line x1="1" y1="50" x2="99" y2="50" stroke="{color}" stroke-width="10"/>
  <circle cx="50" cy="50" r="11" fill="#3B7FD0"/></g></svg>"""


def marco(fondo, texto, pagina, total, cuerpo):
    marcas = f"""<svg class="abs" style="left:0;top:0" width="1080" height="1350"><g stroke="{texto}" stroke-width="3" opacity=".4">
  <path d="M40 70H90M70 40V90M1040 70H990M1010 40V90M40 1280H90M70 1310V1260M1040 1280H990M1010 1310V1260"/></g></svg>"""
    firma = f"""<div class="abs" style="left:112px;top:92px;display:flex;align-items:center;gap:12px;font-family:Marker;font-size:30px;color:{texto};">
  {mira(40, texto)}Oficina Gráfica</div>"""
    num = f'<div class="abs bungee" style="right:112px;top:98px;font-size:30px;color:{VIVO if fondo != VIVO else CELESTE};">{pagina}/{total}</div>'
    grano = """<svg class="abs" style="left:0;top:0;pointer-events:none" width="1080" height="1350"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch"/>
<feColorMatrix values="0 0 0 0 0.08  0 0 0 0 0.16  0 0 0 0 0.25  0 0 0 0.5 0"/></filter><rect width="1080" height="1350" filter="url(#g)" opacity=".22"/></svg>"""
    return f'{HEAD}<body style="background:{fondo};color:{texto};">{marcas}{firma}{num}{cuerpo}{grano}</body></html>'


def tapa(numero, titulo, bajada):
    """Tapa común a las tres fijadas."""
    return f"""
<div class="abs" style="left:112px;right:112px;top:250px;">
  <div class="bungee" style="font-size:300px;color:{CELESTE};line-height:.8;">{numero}</div>
  <div class="bungee" style="font-size:112px;margin-top:40px;">{titulo}</div>
  <div class="txt" style="margin-top:34px;max-width:780px;">{bajada}</div>
</div>
<div class="abs" style="left:112px;bottom:120px;">
  <span class="pill" style="background:{TINTA};color:{PAPEL};">deslizá →</span></div>"""


# ---------- 1 · QUIÉNES SOMOS ----------
QUIENES = [
    (PAPEL, TINTA, tapa("01", "QUIÉNES<br><span style='color:#1C82D9'>SOMOS</span>",
                        "Un taller gráfico que diseña e imprime su propia línea de juegos, libros y papelería.")),
    (TINTA, PAPEL, f"""
<div class="abs" style="left:112px;right:112px;top:260px;">
  <div class="kick" style="color:{CELESTE};">CÓMO EMPEZÓ</div>
  <div class="bungee" style="font-size:92px;margin-top:22px;">DEL BOCETO<br><span style="color:{CELESTE}">AL PAPEL</span></div>
  <div class="txt" style="margin-top:40px;">Todo lo que hacemos nace acá: lo pensamos, lo diseñamos y lo imprimimos nosotros.</div>
  <div class="txt" style="margin-top:28px;opacity:.85;">Nada de catálogo genérico: cada pieza tiene una idea detrás y alguien que la revisó hoja por hoja.</div>
</div>
<div class="abs" style="left:112px;bottom:130px;transform:rotate(-3deg);">{mira(160, PAPEL)}</div>"""),
    (PAPEL, TINTA, f"""
<div class="abs" style="left:112px;right:112px;top:250px;">
  <div class="kick" style="color:{VIVO};">LO QUE NOS MUEVE</div>
  <div class="bungee" style="font-size:84px;margin-top:22px;">COSAS PARA<br>USAR, NO PARA<br>GUARDAR</div>
</div>
<div class="abs" style="left:112px;right:112px;top:690px;display:flex;flex-direction:column;gap:46px;">
  <div style="display:flex;gap:30px;align-items:flex-start;"><div class="bungee" style="font-size:56px;color:{VIVO};width:90px;">01</div>
    <div><div style="font-family:Brico;font-weight:700;font-size:42px;">Para jugar sin pantallas</div><div class="txt" style="font-size:34px;opacity:.8;">Juegos que arman charla de verdad.</div></div></div>
  <div style="display:flex;gap:30px;align-items:flex-start;"><div class="bungee" style="font-size:56px;color:{VIVO};width:90px;">02</div>
    <div><div style="font-family:Brico;font-weight:700;font-size:42px;">Para regalar y recordar</div><div class="txt" style="font-size:34px;opacity:.8;">Libros que se llenan con tu historia.</div></div></div>
  <div style="display:flex;gap:30px;align-items:flex-start;"><div class="bungee" style="font-size:56px;color:{VIVO};width:90px;">03</div>
    <div><div style="font-family:Brico;font-weight:700;font-size:42px;">Hechos con oficio</div><div class="txt" style="font-size:34px;opacity:.8;">Si no está en registro, no sale.</div></div></div>
</div>"""),
    (VIVO, PAPEL, f"""
<div class="abs" style="left:0;right:0;top:215px;display:flex;flex-direction:column;align-items:center;text-align:center;">
  {mira(150, PAPEL)}
  <div class="bungee" style="font-size:96px;margin-top:36px;">¿TENÉS UNA<br>IDEA?</div>
  <div class="txt" style="margin-top:26px;max-width:820px;">Si se puede imprimir, lo hacemos.<br>Y si es digital, también lo diseñamos.</div>
  <div style="display:flex;gap:28px;margin-top:46px;text-align:left;">
    <div style="background:rgba(238,231,216,.14);border:3px solid {PAPEL};border-radius:28px;padding:26px 30px;width:330px;">
      <div class="bungee" style="font-size:40px;">IMPRESO</div>
      <div style="font-size:28px;font-weight:500;line-height:1.35;margin-top:12px;">Juegos, libros, invitaciones, etiquetas, papelería para eventos…</div></div>
    <div style="background:rgba(238,231,216,.14);border:3px solid {PAPEL};border-radius:28px;padding:26px 30px;width:330px;">
      <div class="bungee" style="font-size:40px;">DIGITAL</div>
      <div style="font-size:28px;font-weight:500;line-height:1.35;margin-top:12px;">Logos, posteos, invitaciones digitales, plantillas…</div></div>
  </div>
  <div style="margin-top:48px;"><span class="pill" style="background:{PAPEL};color:{TINTA};">Contanos tu idea por MD</span></div>
</div>"""),
]


def paso(n, titulo, texto, icono):
    return f"""
<div class="abs" style="left:112px;right:112px;top:230px;">
  <div class="bungee" style="font-size:230px;color:{CELESTE};line-height:.8;">{n}</div>
  <div class="bungee" style="font-size:104px;margin-top:30px;">{titulo}</div>
  <div class="txt" style="margin-top:34px;max-width:820px;">{texto}</div>
</div>
<svg class="abs" style="right:112px;bottom:110px;" width="380" height="380" viewBox="-200 -200 400 400">
  <defs><filter id="mano"><feTurbulence type="fractalNoise" baseFrequency="0.02 0.03" numOctaves="2" seed="4" result="t"/>
    <feDisplacementMap in="SourceGraphic" in2="t" scale="6" xChannelSelector="R" yChannelSelector="G"/></filter></defs>
  <g fill="none" stroke="{TINTA}" stroke-width="20" stroke-linecap="round" stroke-linejoin="round" filter="url(#mano)">{icono}</g></svg>"""


ICONOS = {
    "lapiz": f"""<g transform="rotate(-40)"><rect x="-160" y="-40" width="260" height="80" rx="10" fill="{CELESTE}"/>
      <path d="M100 -40L170 0L100 40Z" fill="{PAPEL}"/><path d="M150 -12L170 0L150 12Z" fill="{TINTA}" stroke="none"/></g>
      <circle cx="-120" cy="140" r="17" fill="#1C82D9" stroke="none"/>""",
    "impresora": f"""<path d="M-120 -60V-160H120V-60"/><rect x="-200" y="-60" width="400" height="190" rx="30" fill="{PAPEL}"/>
      <path d="M-120 60H120V190H-120Z" fill="#FBF8F1"/><path d="M-70 105H70M-70 145H30"/>
      <circle cx="140" cy="0" r="17" fill="#1C82D9" stroke="none"/>""",
    "tijera": """<circle cx="-110" cy="70" r="55"/><circle cx="-110" cy="-70" r="55"/><path d="M-62 45L170 -90M-62 -45L170 90"/>
      <path d="M-180 -170V-120M-205 -145H-155" stroke-width="14"/><circle cx="20" cy="0" r="17" fill="#1C82D9" stroke="none"/>""",
    "caja": f"""<path d="M-190 -70L0 -150L190 -70V110L0 190L-190 110Z" fill="{PAPEL}"/><path d="M-190 -70L0 10L190 -70M0 10V190"/>
      <path d="M-95 -110L95 -30V30"/><circle cx="-95" cy="95" r="17" fill="#9BD0EF" stroke="none"/>""",
}

PROCESO = [
    (PAPEL, TINTA, tapa("02", "ASÍ LO<br><span style='color:#1C82D9'>HACEMOS</span>",
                        "De la idea al paquete en tu casa: estos son los cuatro pasos de todo lo que sale del taller.")),
    (PAPEL, TINTA, paso("01", "DISEÑAMOS", "Arranca en un boceto. Pensamos el uso, el texto y cada detalle antes de pasarlo a la compu.", ICONOS["lapiz"])),
    (PAPEL, TINTA, paso("02", "IMPRIMIMOS", "Primero una prueba, siempre. Revisamos colores y cortes antes de imprimir la tirada.", ICONOS["impresora"])),
    (PAPEL, TINTA, paso("03", "CORTAMOS<br>Y ARMAMOS", "Cortes, troquelado, anillado y armado: todo pasa por nuestras manos.", ICONOS["tijera"])),
    (VIVO, PAPEL, paso("04", "ENVIAMOS", "Lo embalamos con cuidado y sale a cualquier punto del país.", ICONOS["caja"].replace(f'fill="{PAPEL}"', f'fill="{VIVO}"')).replace(f'stroke="{TINTA}"', f'stroke="{PAPEL}"')
     + f"""<div class="abs" style="left:112px;bottom:130px;"><span class="pill" style="background:{PAPEL};color:{TINTA};">Pedidos por MD</span></div>"""),
]


def render(nombre, slides):
    total = len(slides)
    for i, (fondo, texto, cuerpo) in enumerate(slides, 1):
        ruta = os.path.join(AQUI, f"_{nombre}-{i}.html")
        png = os.path.join(AQUI, f"{nombre}-{i}.png")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(marco(fondo, texto, i, total, cuerpo))
        subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", "--window-size=1080,1550", "--virtual-time-budget=3000",
                        f"--screenshot={png}", "file://" + ruta], check=True, capture_output=True)
        Image.open(png).convert("RGB").crop((0, 0, 1080, 1350)).save(png)
        os.remove(ruta)


def main():
    render("quienes", QUIENES)
    render("proceso", PROCESO)
    print("ok", len(QUIENES) + len(PROCESO), "slides")


if __name__ == "__main__":
    main()
