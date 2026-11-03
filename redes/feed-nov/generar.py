"""Tres publicaciones para el feed (4:5, 1080 x 1350), cada una con la identidad de su producto.

Uso:  python3 redes/feed-nov/generar.py
  -> debate-1..6.png   Opinólogos: «¿A favor o en contra?», 4 temas para votar en comentarios
  -> match-1..6.png    Match: 4 preguntas para hacerle a tu pareja esta noche
  -> antes-del-31.png  The Dating List: 8 citas para tachar antes de fin de año (para guardar)

Fondos, tipografías y colores son los de Oficina Gráfica (a tono con el feed); las cartas se dibujan
en HTML con el diseño de su producto, así el texto se lee nítido a cualquier tamaño.
"""
import os
import subprocess

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
REDES = os.path.dirname(AQUI)
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

CSS = """<style>
  @font-face{font-family:DMSerif;src:url('../../fuentes/DMSerifDisplay-Regular.ttf');}
  @font-face{font-family:DMSerifIt;src:url('../../fuentes/DMSerifDisplay-Italic.ttf');}
  @font-face{font-family:Pop;src:url('../../fuentes/Poppins-Regular.ttf');font-weight:400;}
  @font-face{font-family:Pop;src:url('../../fuentes/Poppins-Medium.ttf');font-weight:500;}
  @font-face{font-family:Pop;src:url('../../fuentes/Poppins-SemiBold.ttf');font-weight:600;}
  @font-face{font-family:Pop;src:url('../../fuentes/Poppins-Bold.ttf');font-weight:700;}
  @font-face{font-family:Pop;src:url('../../fuentes/Poppins-Black.ttf');font-weight:900;}
  @font-face{font-family:Marker;src:url('../../fuentes/PermanentMarker-Regular.ttf');}
  @font-face{font-family:Bungee;src:url('../../fuentes/Bungee-Regular.ttf');}
  @font-face{font-family:Brico;src:url('../../fuentes/BricolageGrotesque[opsz,wdth,wght].ttf');font-weight:200 800;}
  @font-face{font-family:Karla;src:url('../../fuentes/Karla[wght].ttf');font-weight:200 800;}
  .bungee{font-family:Bungee;line-height:1;}
  .kick{font-family:Brico;font-weight:700;font-size:30px;letter-spacing:6px;}
  .brand-pill{display:inline-block;border-radius:50px;padding:18px 48px;font-family:Brico;font-weight:700;font-size:34px;}
  html,body{margin:0;width:1080px;height:1350px;overflow:hidden;}
  body{position:relative;font-family:Pop;}
  .abs{position:absolute;}
  .pill{display:inline-block;border-radius:50px;padding:18px 48px;font-weight:700;font-size:34px;}
</style>"""


def firma(color, top=70, left=None):
    pos = f"left:{left}px;" if left is not None else "left:0;right:0;justify-content:center;"
    return f"""<div class="abs" style="{pos}top:{top}px;display:flex;align-items:center;gap:10px;
  font-family:Marker;font-size:28px;color:{color};"><svg width="34" height="34" viewBox="-4 -4 108 108">
  <circle cx="50" cy="50" r="35.5" fill="none" stroke="currentColor" stroke-width="10"/>
  <line x1="50" y1="1" x2="50" y2="99" stroke="currentColor" stroke-width="10"/>
  <line x1="1" y1="50" x2="99" y2="50" stroke="currentColor" stroke-width="10"/>
  <circle cx="50" cy="50" r="11" fill="#3B7FD0"/></svg>Oficina Gráfica</div>"""


# ---------------- MARCO DE OFICINA GRÁFICA ----------------
# Fondos, tipografías y colores de la marca para que las publicaciones queden a tono con el feed;
# las cartas mantienen el diseño de su producto (es lo que se vende).
PAPEL, TINTA, VIVO, CELESTE = "#EEE7D8", "#142A40", "#1C82D9", "#9BD0EF"


def marca(fondo, cuerpo, pagina=None, total=None):
    texto = TINTA if fondo == PAPEL else PAPEL
    num = (f'<div class="abs bungee" style="right:112px;top:98px;font-size:30px;color:{VIVO if fondo != VIVO else CELESTE};">'
           f'{pagina}/{total}</div>') if total else ""
    return f"""<body style="background:{fondo};color:{texto};font-family:Karla;">
<svg class="abs" style="left:0;top:0" width="1080" height="1350"><g stroke="{texto}" stroke-width="3" opacity=".4">
  <path d="M40 70H90M70 40V90M1040 70H990M1010 40V90M40 1280H90M70 1310V1260M1040 1280H990M1010 1310V1260"/></g></svg>
{firma(texto, 92, 112)}{num}{cuerpo}
<svg class="abs" style="left:0;top:0;pointer-events:none" width="1080" height="1350"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch"/>
<feColorMatrix values="0 0 0 0 0.08  0 0 0 0 0.16  0 0 0 0 0.25  0 0 0 0.5 0"/></filter><rect width="1080" height="1350" filter="url(#g)" opacity=".2"/></svg></body>"""


# ---------------- OPINÓLOGOS ----------------
NIVEL = {"calentamiento": "#2F6FED", "picante": "#F08A24", "profundo": "#D7263D"}
FRANJA = """<div class="abs" style="left:0;right:0;top:0;height:22px;display:flex;"><div style="flex:1;background:#2F6FED"></div>
  <div style="flex:1;background:#F08A24"></div><div style="flex:1;background:#D7263D"></div></div>"""


def carta_op(texto, nivel, ancho=560, ang=0, x=0, y=0):
    color = NIVEL[nivel]
    alto = ancho * 88 / 63
    e = ancho / 560  # escala
    return f"""<div class="abs" style="left:{x}px;top:{y}px;width:{ancho}px;height:{alto}px;background:#FFF;border-radius:{28*e}px;
  transform:rotate({ang}deg);box-shadow:0 {26*e}px {40*e}px rgba(0,0,0,.18);overflow:hidden;">
  <div style="height:{26*e}px;background:{color};"></div>
  <div style="padding:{34*e}px {44*e}px 0;display:flex;justify-content:space-between;font-size:{22*e}px;font-weight:600;color:{color};">
    <span>{nivel}</span><span style="color:#999;">14+</span></div>
  <div style="padding:{60*e}px {44*e}px 0;font-weight:700;font-size:{50*e}px;line-height:1.18;color:#111;">{texto}</div>
  <div style="position:absolute;left:{44*e}px;right:{44*e}px;bottom:{70*e}px;display:flex;justify-content:space-between;
    font-size:{22*e}px;font-weight:600;color:#999;border-top:{2*e}px solid #E3E3E3;padding-top:{16*e}px;">
    <span style="color:#1F9D5C;">✔ a favor</span><span style="color:#D93A3A;">✖ en contra</span></div>
  <div style="position:absolute;left:{44*e}px;bottom:{26*e}px;font-size:{22*e}px;font-weight:700;color:#111;">opinólogos<span style="color:{color}">.</span></div>
</div>"""


DEBATES = [("Un beso con otra persona ya es infidelidad.", "picante"),
           ("En un restaurante, la cuenta se divide en partes iguales aunque hayas pedido menos.", "calentamiento"),
           ("Si un amigo sale con tu ex, se terminó la amistad.", "picante"),
           ("Una infidelidad se puede perdonar.", "picante")]


def debate_tapa():
    return marca(PAPEL, f"""
<div class="abs" style="left:112px;right:112px;top:210px;">
  <div class="kick" style="color:{VIVO};">PARA TU PRÓXIMA PREVIA</div>
  <div class="bungee" style="font-size:112px;margin-top:22px;">¿A FAVOR<br><span style="color:{VIVO}">O EN CONTRA?</span></div>
  <div style="font-size:40px;font-weight:500;margin-top:26px;">4 debates para votar en comentarios.</div>
</div>
{carta_op(DEBATES[1][0], DEBATES[1][1], 290, -10, 210, 820)}
{carta_op(DEBATES[2][0], DEBATES[2][1], 290, 9, 590, 830)}
{carta_op(DEBATES[0][0], DEBATES[0][1], 310, 0, 390, 780)}""", 1, 6)


def debate_slide(i, texto, nivel):
    fondo = TINTA if i % 2 else PAPEL
    return marca(fondo, f"""
<div class="abs kick" style="left:0;right:0;top:175px;text-align:center;color:{CELESTE if fondo == TINTA else VIVO};">DEBATE {i} DE 4</div>
{carta_op(texto, nivel, 580, -2 if i % 2 else 2, 250, 240)}
<div class="abs" style="left:0;right:0;top:1100px;text-align:center;">
  <div class="bungee" style="font-size:58px;">COMENTÁ <span style="color:#1F9D5C">✔</span> O <span style="color:#D93A3A">✖</span></div>
  <div style="font-size:34px;font-weight:500;margin-top:14px;">y defendé tu postura</div>
</div>""", i + 1, 6)


def debate_cierre():
    return marca(VIVO, f"""
<div class="abs" style="left:112px;right:112px;top:200px;text-align:center;">
  <div class="bungee" style="font-size:84px;">HAY 136<br><span style="color:{TINTA}">DEBATES MÁS</span></div>
  <div style="font-size:38px;font-weight:500;margin-top:22px;">Opinólogos: todos opinan, pocos convencen.</div>
</div>
<img class="abs" src="../gemini/opinologos-foto-final.jpg" style="left:290px;top:520px;height:560px;border-radius:24px;transform:rotate(-3deg);border:10px solid {PAPEL};box-shadow:0 26px 34px rgba(20,42,64,.35);">
<div class="abs" style="left:0;right:0;top:1150px;text-align:center;"><span class="brand-pill" style="background:{PAPEL};color:{TINTA};">Pedilo por MD</span></div>""", 6, 6)


# ---------------- MATCH ----------------
BORDO, NEGRO, BEIGE, ROJO = "#5C0F1E", "#0F0D0D", "#E6D5B8", "#C8102E"


def carta_match(texto, pareja, fondo, ancho=600, ang=0, x=0, y=0):
    alto = ancho * 88 / 63
    e = ancho / 600
    pill = (f'<div style="display:inline-block;background:{BEIGE};color:{BORDO};border-radius:{30*e}px;padding:{8*e}px {22*e}px;'
            f'font-size:{22*e}px;font-weight:600;">responde tu pareja</div>') if pareja else ""
    return f"""<div class="abs" style="left:{x}px;top:{y}px;width:{ancho}px;height:{alto}px;background:{fondo};border-radius:{30*e}px;
  transform:rotate({ang}deg);box-shadow:0 {30*e}px {46*e}px rgba(0,0,0,.45);">
  <div style="position:absolute;inset:{24*e}px;border:{2.5*e}px solid {BEIGE};border-radius:{22*e}px;padding:{36*e}px {40*e}px;box-sizing:border-box;">
    {pill}
    <div style="position:absolute;left:{40*e}px;right:{40*e}px;top:42%;transform:translateY(-50%);font-family:DMSerif;font-size:{58*e}px;
      line-height:1.12;color:{BEIGE};">{texto}</div>
    <div style="position:absolute;left:{40*e}px;bottom:{30*e}px;font-family:DMSerifIt;font-size:{30*e}px;color:{BEIGE};">match<span style="color:{ROJO}">o</span></div>
  </div></div>"""


PREGUNTAS = [("¿Cuál es mi mayor miedo?", True),
             ("Contá en qué momento te diste cuenta de que te gustaba.", False),
             ("Contá qué te pone celoso o celosa de verdad.", False),
             ("¿Qué cosa mía nunca dejaría de hacer, aunque me lo pidas?", True)]


def match_tapa():
    return marca(TINTA, f"""
<div class="abs" style="left:112px;right:112px;top:210px;">
  <div class="kick" style="color:{CELESTE};">PARA HACER ESTA NOCHE</div>
  <div class="bungee" style="font-size:104px;margin-top:22px;">4 PREGUNTAS<br><span style="color:{CELESTE}">PARA TU PAREJA</span></div>
  <div style="font-size:40px;font-weight:500;margin-top:26px;">y ver cuánto te conoce.</div>
</div>
{carta_match(PREGUNTAS[0][0], True, BORDO, 320, -9, 240, 770)}
{carta_match(PREGUNTAS[2][0], False, "#1B1717", 320, 8, 540, 780)}""", 1, 6)


def match_slide(i, texto, pareja):
    fondo = PAPEL if i % 2 else VIVO
    abajo = ("Si no adivina, le toca un reto." if pareja else "Responden los dos.")
    return marca(fondo, f"""
<div class="abs kick" style="left:0;right:0;top:175px;text-align:center;color:{VIVO if fondo == PAPEL else TINTA};">PREGUNTA {i} DE 4</div>
{carta_match(texto, pareja, BORDO if i % 2 else "#1B1717", 580, -2 if i % 2 else 2, 250, 240)}
<div class="abs bungee" style="left:0;right:0;top:1120px;text-align:center;font-size:48px;">{abajo.upper()}</div>""", i + 1, 6)


def match_cierre():
    return marca(TINTA, f"""
<div class="abs" style="left:112px;right:112px;top:200px;text-align:center;">
  <div class="bungee" style="font-size:64px;">QUEDAN 86 PREGUNTAS<br><span style="color:{CELESTE}">Y 30 RETOS</span></div>
  <div style="font-size:38px;font-weight:500;margin-top:22px;">Match: preguntas y retos para parejas.</div>
</div>
<img class="abs" src="../ia-feed/match-ia-corregida.jpg" style="left:270px;top:510px;height:580px;border-radius:24px;transform:rotate(2deg);border:10px solid {PAPEL};box-shadow:0 26px 34px rgba(0,0,0,.35);">
<div class="abs" style="left:0;right:0;top:1160px;text-align:center;"><span class="brand-pill" style="background:{PAPEL};color:{TINTA};">Pedilo por MD</span></div>""", 6, 6)


# ---------------- THE DATING LIST ----------------
CITAS = [("23", "Picnic en una plaza o un parque.", True), ("31", "Ver el atardecer desde un mirador.", False),
         ("38", "Tomar un helado y caminar sin rumbo.", True), ("39", "Ir a un cine al aire libre.", False),
         ("34", "Ir a una feria de food trucks.", False), ("44", "Mirar las estrellas lejos de la ciudad.", False),
         ("81", "Recrear su primera cita.", False), ("97", "Un día entero sin celulares.", False)]


def antes_del_31():
    filas = ""
    for n, texto, hecha in CITAS:
        tilde = (f'<svg width="54" height="54" viewBox="0 0 54 54" style="position:absolute;left:-4px;top:-10px;">'
                 f'<path d="M8 28L22 42L50 6" fill="none" stroke="{VIVO}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>') if hecha else ""
        tachado = f"text-decoration:line-through;text-decoration-color:{VIVO};text-decoration-thickness:4px;opacity:.55;" if hecha else ""
        filas += f"""<div style="display:flex;align-items:center;gap:22px;padding:14px 0;border-bottom:2px solid rgba(20,42,64,.15);">
  <div style="position:relative;width:44px;height:44px;border:4px solid {TINTA};border-radius:8px;flex:none;">{tilde}</div>
  <div style="font-family:Bungee;font-size:26px;color:{VIVO};width:80px;white-space:nowrap;">{n}</div>
  <div style="font-family:Brico;font-weight:600;font-size:36px;color:{TINTA};{tachado}">{texto}</div></div>"""
    return marca(PAPEL, f"""
<div class="abs" style="left:112px;right:112px;top:190px;">
  <div class="kick" style="color:{VIVO};">ANTES DE QUE TERMINE EL AÑO</div>
  <div class="bungee" style="font-size:64px;margin-top:20px;">8 CITAS PARA TACHAR<br><span style="color:{VIVO}">ANTES DEL 31</span></div>
</div>
<div class="abs" style="left:112px;right:112px;top:450px;">{filas}</div>
<div class="abs" style="left:112px;right:112px;top:1150px;display:flex;align-items:center;justify-content:space-between;">
  <div style="font-size:34px;font-weight:600;">Las otras 92, en The Dating List.</div>
  <span class="brand-pill" style="background:{TINTA};color:{PAPEL};font-size:30px;padding:16px 36px;">Guardala</span>
</div>""")


def render(nombre, cuerpo):
    ruta = os.path.join(AQUI, f"_{nombre}.html")
    png = os.path.join(AQUI, f"{nombre}.png")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write('<!doctype html><html lang="es"><head><meta charset="utf-8">' + CSS + "</head>" + cuerpo + "</html>")
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=1080,1550", "--virtual-time-budget=3000",
                    f"--screenshot={png}", "file://" + ruta], check=True, capture_output=True)
    Image.open(png).convert("RGB").crop((0, 0, 1080, 1350)).save(png)
    os.remove(ruta)


def main():
    render("debate-1", debate_tapa())
    for i, (t, n) in enumerate(DEBATES, 1):
        render(f"debate-{i + 1}", debate_slide(i, t, n))
    render("debate-6", debate_cierre())
    render("match-1", match_tapa())
    for i, (t, p) in enumerate(PREGUNTAS, 1):
        render(f"match-{i + 1}", match_slide(i, t, p))
    render("match-6", match_cierre())
    render("antes-del-31", antes_del_31())
    print("ok")


if __name__ == "__main__":
    main()
