"""Piezas para anuncios pagos de Meta (no van al feed): 3 anuncios en 4:5 (1080 x 1350) y 9:16 (1080 x 1920).

Uso:  python3 redes/anuncios/generar.py  ->  NOMBRE-feed.png y NOMBRE-historia.png

1 · match: regalo para la pareja · 2 · opinologos: la previa · 3 · libros: álbumes para completar.
Los juegos usan las fotos de producto finales de Gemini (redes/gemini/); los libros, las maquetas.
En 9:16 los textos quedan entre y = 250 y y = 1580 (arriba y abajo Instagram pone su interfaz).
"""
import os
import subprocess

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

CSS = """<style>
  @font-face{font-family:Bungee;src:url('../../fuentes/Bungee-Regular.ttf');}
  @font-face{font-family:Brico;src:url('../../fuentes/BricolageGrotesque[opsz,wdth,wght].ttf');font-weight:200 800;}
  @font-face{font-family:Karla;src:url('../../fuentes/Karla[wght].ttf');font-weight:200 800;}
  @font-face{font-family:Marker;src:url('../../fuentes/PermanentMarker-Regular.ttf');}
  html,body{margin:0;width:1080px;height:ALTOpx;overflow:hidden;}
  body{position:relative;font-family:Karla;display:flex;flex-direction:column;align-items:center;
       justify-content:center;gap:GAPpx;text-align:center;box-sizing:border-box;padding:PADpx 90px;}
  .firma{display:flex;align-items:center;gap:12px;font-family:Marker;font-size:30px;}
  .kicker{font-family:Brico;font-weight:700;font-size:32px;letter-spacing:6px;}
  .tit{font-family:Bungee;font-size:92px;line-height:1.02;}
  .sub{font-size:40px;font-weight:500;line-height:1.3;}
  .prods{position:relative;width:900px;height:PRODpx;}
  .prods img{position:absolute;filter:drop-shadow(0 26px 30px rgba(0,0,0,.35));}
  .cta{display:inline-block;border-radius:60px;padding:24px 60px;font-family:Brico;font-weight:700;font-size:40px;}
</style>"""


def firma(color):
    return f"""<div class="firma" style="color:{color};"><svg width="40" height="40" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="34" fill="none" stroke="currentColor" stroke-width="10"/>
  <line x1="50" y1="2" x2="50" y2="98" stroke="currentColor" stroke-width="10"/>
  <line x1="2" y1="50" x2="98" y2="50" stroke="currentColor" stroke-width="10"/>
  <circle cx="50" cy="50" r="12" fill="#1C82D9"/></svg>Oficina Gráfica</div>"""


ANUNCIOS = {
    "match": dict(
        fondo="#5C0F1E", texto="#EFE3D0", acento="#F2B8C6",
        kicker="REGALO PARA TU PAREJA", tit="QUE NO ES<br>UN PERFUME",
        sub="120 preguntas y retos para conocerse<br>(y animarse) un poco más.",
        prods=[("../gemini/match-foto-final.jpg", "left:FXpx;top:0;height:FHpx;border-radius:28px;transform:rotate(-3deg);"),
               ("_match-pregunta.png", "left:Lpx;top:Tpx;height:H2px;transform:rotate(8deg);")],
        cta="Pedilo por MD", cta_fondo="#EFE3D0", cta_texto="#5C0F1E"),
    "opinologos": dict(
        fondo="#FFFFFF", texto="#111111", acento="#2F6FED",
        kicker="PARA LA PREVIA", tit="TODOS OPINAN.<br>POCOS CONVENCEN.",
        sub="El juego de debate que termina<br>con alguien diciendo «me convenciste».",
        prods=[("../gemini/opinologos-foto-final.jpg", "left:FXpx;top:0;height:FHpx;border-radius:28px;transform:rotate(-3deg);"),
               ("_opinologos-tema.png", "left:Lpx;top:Tpx;height:H2px;transform:rotate(8deg);")],
        cta="Pedilo por MD", cta_fondo="#111111", cta_texto="#FFFFFF", franja=True),
    "libros": dict(
        fondo="#EEE7D8", texto="#142A40", acento="#1C82D9",
        kicker="PARA LOS QUE ANOTAN TODO", tit="LIBROS PARA<br>COMPLETAR",
        sub="Citas, vinos y alfajores:<br>uno por página, hasta llenarlo.",
        prods=[("../regalito/libro-dating-list.png", "left:30px;top:0;height:HLpx;transform:rotate(-7deg);"),
               ("../vinos/libro-tapa.png", "left:Vpx;top:0;height:HLpx;transform:rotate(6deg);"),
               ("../regalito/album-alfajores.png", "left:Apx;top:TApx;width:Wpx;transform:rotate(-2deg);")],
        cta="Pedilo por MD", cta_fondo="#142A40", cta_texto="#EEE7D8"),
}

FORMATOS = {"feed": dict(alto=1350, gap=26, pad=70, prod=520, h1=480, h2=300, t=190, w=330, l=560, hl=400, v=600, a=290, ta=230, fx=150, fh=480),
            "historia": dict(alto=1920, gap=34, pad=250, prod=700, h1=560, h2=380, t=280, w=420, l=600, hl=520, v=560, a=250, ta=330, fx=120, fh=650)}


def html(a, f):
    css = (CSS.replace("ALTO", str(f["alto"])).replace("GAP", str(f["gap"])).replace("PAD", str(f["pad"]))
           .replace("PROD", str(f["prod"])))
    def medidas(st):
        for clave in ("TA", "HL", "FX", "FH", "H1", "H2", "T", "W", "L", "V", "A"):  # las claves largas primero
            st = st.replace(f":{clave}px", f":{f[clave.lower()]}px")
        return st
    imgs = "".join(f'<img src="{src}" style="{medidas(st)}">' for src, st in a["prods"])
    franja = ('<div style="position:absolute;left:0;right:0;top:0;height:22px;display:flex;"><div style="flex:1;background:#2F6FED"></div>'
              '<div style="flex:1;background:#F08A24"></div><div style="flex:1;background:#D7263D"></div></div>') if a.get("franja") else ""
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">{css}</head>
<body style="background:{a['fondo']};color:{a['texto']};">{franja}
{firma(a['texto'])}
<div class="kicker" style="color:{a['acento']};">{a['kicker']}</div>
<div class="tit">{a['tit']}</div>
<div class="prods">{imgs}</div>
<div class="sub">{a['sub']}</div>
<div class="cta" style="background:{a['cta_fondo']};color:{a['cta_texto']};">{a['cta']}</div>
</body></html>"""


def preparar():
    import sys
    import tempfile
    sys.path.insert(0, os.path.dirname(AQUI))
    import foto_producto as fp
    raiz = os.path.dirname(os.path.dirname(AQUI))
    with tempfile.TemporaryDirectory() as tmp:
        fp.carta(os.path.join(raiz, "match", "match-cartas.pdf"), 1, 1, tmp).save(os.path.join(AQUI, "_match-pregunta.png"))
        fp.carta(os.path.join(raiz, "opinologos-muestra-imprenta.pdf"), 1, 4, tmp).save(os.path.join(AQUI, "_opinologos-tema.png"))


def main():
    preparar()
    for nombre, a in ANUNCIOS.items():
        for fmt, f in FORMATOS.items():
            ruta = os.path.join(AQUI, f"_{nombre}-{fmt}.html")
            png = os.path.join(AQUI, f"{nombre}-{fmt}.png")
            with open(ruta, "w", encoding="utf-8") as fh:
                fh.write(html(a, f))
            subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                            "--force-device-scale-factor=1", f"--window-size=1080,{f['alto'] + 200}",
                            "--virtual-time-budget=3000", f"--screenshot={png}", "file://" + ruta],
                           check=True, capture_output=True)
            Image.open(png).convert("RGB").crop((0, 0, 1080, f["alto"])).save(png)
            os.remove(ruta)
    print("ok", len(ANUNCIOS) * len(FORMATOS), "piezas")


if __name__ == "__main__":
    main()
