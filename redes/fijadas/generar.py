"""Publicaciones fijadas del perfil (carruseles 4:5, 1080 x 1350), pensadas para no envejecer:
no nombran productos puntuales, así sirven aunque la línea crezca.

Uso:  python3 redes/fijadas/generar.py  ->  quienes-1..3.png, regalos-1..6.png, idea-1..2.png

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
    """pagina/total arriba a la derecha; en una publicación suelta (total = 1) no se muestra."""
    marcas = f"""<svg class="abs" style="left:0;top:0" width="1080" height="1350"><g stroke="{texto}" stroke-width="3" opacity=".4">
  <path d="M40 70H90M70 40V90M1040 70H990M1010 40V90M40 1280H90M70 1310V1260M1040 1280H990M1010 1310V1260"/></g></svg>"""
    firma = f"""<div class="abs" style="left:112px;top:92px;display:flex;align-items:center;gap:12px;font-family:Marker;font-size:30px;color:{texto};">
  {mira(40, texto)}Oficina Gráfica</div>"""
    num = (f'<div class="abs bungee" style="right:112px;top:98px;font-size:30px;color:{VIVO if fondo != VIVO else CELESTE};">{pagina}/{total}</div>'
           if total > 1 else "")
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
]

IDEA = [
    (PAPEL, TINTA, tapa("03", "¿TENÉS UNA<br><span style='color:#1C82D9'>IDEA?</span>",
                        "Si se puede imprimir, lo hacemos. Y si es digital, también lo diseñamos.")),
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


def ocasion(kicker, titulo, texto, productos):
    """Slide de la guía de regalos: ocasión arriba, productos sugeridos abajo (se cambian sin tocar el resto)."""
    return f"""
<div class="abs" style="left:112px;right:112px;top:220px;">
  <div class="kick" style="color:{VIVO};">{kicker}</div>
  <div class="bungee" style="font-size:88px;margin-top:20px;">{titulo}</div>
  <div class="txt" style="margin-top:26px;max-width:820px;font-size:36px;">{texto}</div>
</div>
<div class="abs" style="left:0;right:0;top:700px;height:560px;">{productos}</div>"""


def foto(src, x, y, alto, ang):
    return (f'<img src="{src}" style="position:absolute;left:{x}px;top:{y}px;height:{alto}px;transform:rotate({ang}deg);'
            f'border:10px solid #FBF8F1;border-radius:20px;box-shadow:0 22px 30px rgba(20,42,64,.3);">')


def objeto(src, x, y, alto, ang):
    return f'<img class="sombra" src="{src}" style="position:absolute;left:{x}px;top:{y}px;height:{alto}px;transform:rotate({ang}deg);">'


REGALOS = [
    (PAPEL, TINTA, tapa("02", "IDEAS PARA<br><span style='color:#1C82D9'>REGALAR</span>",
                        "Para cuando no sabés qué regalar. Guardala para la próxima.")),
    (PAPEL, TINTA, ocasion("ANIVERSARIO · SAN VALENTÍN", "PARA TU<br>PAREJA",
                           "Algo para hacer juntos, no para guardar en un cajón.",
                           foto("../gemini/match-foto-final.jpg", 150, 30, 470, -5)
                           + objeto("../regalito/libro-dating-list.png", 580, 20, 500, 6))),
    (TINTA, PAPEL, ocasion("CUMPLEAÑOS · LA PREVIA", "PARA TUS<br>AMIGOS",
                           "El regalo que se estrena esa misma noche.",
                           foto("../gemini/opinologos-foto-final.jpg", 300, 20, 500, -4))),
    (PAPEL, TINTA, ocasion("DÍA DEL PADRE · EL QUE TIENE TODO", "PARA EL QUE<br>DISFRUTA",
                           "Para el que siempre dice «este vino estaba buenísimo» y después se olvida cuál era.",
                           objeto("../vinos/libro-tapa.png", 330, 10, 520, -4))),
    (PAPEL, TINTA, ocasion("AMIGO INVISIBLE · UN DETALLE", "ALGO<br>DISTINTO",
                           "Un regalo chico que no termina en el fondo del placard.",
                           objeto("../regalito/album-alfajores.png", 270, 40, 480, -3))),
    (VIVO, PAPEL, f"""
<div class="abs" style="left:0;right:0;top:300px;display:flex;flex-direction:column;align-items:center;text-align:center;">
  {mira(170, PAPEL)}
  <div class="bungee" style="font-size:92px;margin-top:44px;">¿NINGUNO<br>TE CONVENCE?</div>
  <div class="txt" style="margin-top:30px;max-width:820px;">Lo hacemos a medida: con nombres, fechas o la idea que tengas.</div>
  <div style="margin-top:56px;"><span class="pill" style="background:{PAPEL};color:{TINTA};">Escribinos por MD</span></div>
</div>"""),
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
    render("regalos", REGALOS)
    render("idea", IDEA)
    print("ok", len(QUIENES) + len(REGALOS) + len(IDEA), "slides")


if __name__ == "__main__":
    main()
