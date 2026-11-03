"""Tres publicaciones para el feed (4:5, 1080 x 1350), cada una con la identidad de su producto.

Uso:  python3 redes/feed-nov/generar.py
  -> debate-1..6.png   Opinólogos: «¿A favor o en contra?», 4 temas para votar en comentarios
  -> match-1..6.png    Match: 4 preguntas para hacerle a tu pareja esta noche
  -> antes-del-31.png  The Dating List: 8 citas para tachar antes de fin de año (para guardar)

Las cartas se dibujan en HTML con el mismo diseño que las impresas, así el texto se lee
nítido a cualquier tamaño.
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
    return f"""<body style="background:#FFF;color:#111;">{FRANJA}{firma('#111', 80)}
<div class="abs" style="left:90px;right:90px;top:200px;text-align:center;">
  <div style="font-weight:900;font-size:118px;line-height:.98;letter-spacing:-3px;">¿A FAVOR<br>O EN<br>CONTRA?</div>
  <div style="font-size:38px;font-weight:500;margin-top:28px;color:#555;">4 debates para tu próxima previa</div>
</div>
{carta_op(DEBATES[1][0], DEBATES[1][1], 300, -10, 200, 830)}
{carta_op(DEBATES[2][0], DEBATES[2][1], 300, 9, 580, 840)}
{carta_op(DEBATES[0][0], DEBATES[0][1], 320, 0, 380, 790)}
</body>"""


def debate_slide(i, texto, nivel):
    return f"""<body style="background:#F4F4F2;color:#111;">{FRANJA}{firma('#111', 80)}
<div class="abs" style="left:0;right:0;top:150px;text-align:center;font-weight:700;font-size:30px;letter-spacing:6px;color:{NIVEL[nivel]};">DEBATE {i} DE 4</div>
{carta_op(texto, nivel, 600, -2 if i % 2 else 2, 240, 230)}
<div class="abs" style="left:0;right:0;top:1120px;text-align:center;">
  <div style="font-weight:900;font-size:56px;letter-spacing:-1px;">Comentá <span style="color:#1F9D5C">✔</span> o <span style="color:#D93A3A">✖</span></div>
  <div style="font-size:32px;font-weight:500;color:#555;margin-top:8px;">y defendé tu postura</div>
</div></body>"""


def debate_cierre():
    return f"""<body style="background:#111;color:#FFF;">{FRANJA}{firma('#FFF', 80)}
<div class="abs" style="left:90px;right:90px;top:180px;text-align:center;">
  <div style="font-weight:900;font-size:84px;line-height:1;letter-spacing:-2px;">HAY 136<br>DEBATES MÁS</div>
  <div style="font-size:36px;font-weight:500;margin-top:22px;color:#BBB;">Todos opinan. Pocos convencen.</div>
</div>
<img class="abs" src="../gemini/opinologos-foto-final.jpg" style="left:270px;top:470px;height:600px;border-radius:24px;transform:rotate(-3deg);border:10px solid #FFF;">
<div class="abs" style="left:0;right:0;top:1150px;text-align:center;"><span class="pill" style="background:#FFF;color:#111;">Pedilo por MD</span></div>
</body>"""


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
    return f"""<body style="background:{NEGRO};color:{BEIGE};">{firma(BEIGE, 80)}
<div class="abs" style="left:90px;right:90px;top:190px;text-align:center;">
  <div style="font-family:Pop;font-weight:600;font-size:28px;letter-spacing:6px;color:{ROJO};">PARA HACER ESTA NOCHE</div>
  <div style="font-family:DMSerif;font-size:104px;line-height:1.02;margin-top:22px;">4 preguntas<br>para tu pareja</div>
  <div style="font-family:DMSerifIt;font-size:48px;margin-top:18px;opacity:.85;">y ver cuánto te conoce</div>
</div>
{carta_match(PREGUNTAS[0][0], True, BORDO, 330, -9, 230, 760)}
{carta_match(PREGUNTAS[2][0], False, "#1B1717", 330, 8, 530, 770)}
</body>"""


def match_slide(i, texto, pareja):
    fondo = BORDO if i % 2 else NEGRO
    carta = "#1B1717" if i % 2 else BORDO
    abajo = ("Si no adivina, le toca un reto." if pareja else "Responden los dos.")
    return f"""<body style="background:{fondo};color:{BEIGE};">{firma(BEIGE, 80)}
<div class="abs" style="left:0;right:0;top:160px;text-align:center;font-weight:600;font-size:28px;letter-spacing:6px;color:{BEIGE};opacity:.75;">PREGUNTA {i} DE 4</div>
{carta_match(texto, pareja, carta, 600, -2 if i % 2 else 2, 240, 240)}
<div class="abs" style="left:0;right:0;top:1130px;text-align:center;font-family:DMSerifIt;font-size:52px;">{abajo}</div>
</body>"""


def match_cierre():
    return f"""<body style="background:{NEGRO};color:{BEIGE};">{firma(BEIGE, 80)}
<div class="abs" style="left:90px;right:90px;top:170px;text-align:center;">
  <div style="font-family:DMSerif;font-size:86px;line-height:1.02;">Quedan 86 preguntas<br><span style="font-family:DMSerifIt;">y 30 retos</span></div>
</div>
<img class="abs" src="../ia-feed/match-ia-corregida.jpg" style="left:240px;top:430px;height:650px;border-radius:24px;transform:rotate(2deg);border:10px solid {BEIGE};">
<div class="abs" style="left:0;right:0;top:1160px;text-align:center;"><span class="pill" style="background:{BEIGE};color:{BORDO};">Pedilo por MD</span></div>
</body>"""


# ---------------- THE DATING LIST ----------------
CITAS = [("23", "Picnic en una plaza o un parque.", True), ("31", "Ver el atardecer desde un mirador.", False),
         ("38", "Tomar un helado y caminar sin rumbo.", True), ("39", "Ir a un cine al aire libre.", False),
         ("34", "Ir a una feria de food trucks.", False), ("44", "Mirar las estrellas lejos de la ciudad.", False),
         ("81", "Recrear su primera cita.", False), ("97", "Un día entero sin celulares.", False)]


def antes_del_31():
    filas = ""
    for n, texto, hecha in CITAS:
        tilde = (f'<svg width="54" height="54" viewBox="0 0 54 54" style="position:absolute;left:-4px;top:-10px;">'
                 f'<path d="M8 28L22 42L50 6" fill="none" stroke="#C8102E" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>') if hecha else ""
        tachado = "text-decoration:line-through;text-decoration-color:#C8102E;text-decoration-thickness:4px;opacity:.6;" if hecha else ""
        filas += f"""<div style="display:flex;align-items:center;gap:22px;padding:14px 0;border-bottom:2px solid rgba(92,15,30,.18);">
  <div style="position:relative;width:44px;height:44px;border:4px solid #5C0F1E;border-radius:8px;flex:none;">{tilde}</div>
  <div style="font-family:DMSerifIt;font-size:28px;color:#5C0F1E;width:96px;white-space:nowrap;">n.º {n}</div>
  <div style="font-family:DMSerif;font-size:37px;color:#2A0A10;{tachado}">{texto}</div></div>"""
    return f"""<body style="background:#EFE3D0;color:#5C0F1E;">{firma('#5C0F1E', 70)}
<div class="abs" style="left:90px;right:90px;top:150px;">
  <div style="font-family:Pop;font-weight:600;font-size:28px;letter-spacing:6px;color:#C8102E;">ANTES DE QUE TERMINE EL AÑO</div>
  <div style="font-family:DMSerif;font-size:92px;line-height:1;margin-top:16px;">8 citas para tachar<br><span style="font-family:DMSerifIt;">antes del 31</span></div>
</div>
<div class="abs" style="left:90px;right:90px;top:420px;">{filas}</div>
<div class="abs" style="left:90px;right:90px;top:1180px;display:flex;align-items:center;justify-content:space-between;">
  <div style="font-family:DMSerifIt;font-size:40px;">Las otras 92, en The Dating List.</div>
  <span class="pill" style="background:#5C0F1E;color:#EFE3D0;font-size:30px;padding:16px 36px;">Guardala</span>
</div></body>"""


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
